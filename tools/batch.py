"""Volume-generation helper for ComfyUI (LTX-Video T2V + Flux text-to-image).

Reads a prompts file (one prompt per line) and runs each through a
workflow against a local ComfyUI instance at 127.0.0.1:8188. Logs
every job to runs.csv. See `tools/setup-comfyui-stack.sh` for
install.

Usage:
    python batch.py --prompts prompts.txt                       # default: LTX T2V
    python batch.py --prompts prompts.txt --workflow flux       # Flux T2I
    python batch.py --prompts prompts.txt --concurrency 1       # ComfyUI is serial; this just queues
    python batch.py --prompts-text "a single prompt"            # for the smoke tests
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import random
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

COMFY_HOST = os.environ.get("COMFY_HOST", "127.0.0.1")
COMFY_PORT = int(os.environ.get("COMFY_PORT", "8188"))
BASE = f"http://{COMFY_HOST}:{COMFY_PORT}"

NEGATIVE_PROMPT_HINTS = (
    "watermark", "low quality", "blurry", "deformed",
    "ugly", "bad anatomy", "worst quality", "logo",
)


# ── ComfyUI HTTP helpers ────────────────────────────────────────────
def post_prompt(workflow: dict, client_id: str) -> str:
    payload = json.dumps({"prompt": workflow, "client_id": client_id}).encode()
    req = urllib.request.Request(
        f"{BASE}/prompt", data=payload,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())["prompt_id"]


def get_history(prompt_id: str) -> dict | None:
    try:
        with urllib.request.urlopen(f"{BASE}/history/{prompt_id}", timeout=10) as r:
            data = json.loads(r.read())
            return data.get(prompt_id)
    except urllib.error.HTTPError:
        return None


def fetch_output(filename: str, subfolder: str, type_: str = "output") -> bytes:
    q = urllib.parse.urlencode({
        "filename": filename, "subfolder": subfolder, "type": type_,
    })
    with urllib.request.urlopen(f"{BASE}/view?{q}", timeout=60) as r:
        return r.read()


# ── workflow mutation ───────────────────────────────────────────────
def find_positive_prompt_node(workflow: dict) -> str | None:
    """Pick the CLIPTextEncode node that holds the positive prompt."""
    candidates = [
        nid for nid, node in workflow.items()
        if node.get("class_type", "").endswith("CLIPTextEncode")
    ]
    if not candidates:
        return None
    if len(candidates) == 1:
        return candidates[0]
    scored = []
    for nid in candidates:
        text = (workflow[nid].get("inputs", {}).get("text") or "").lower()
        neg_score = sum(1 for hint in NEGATIVE_PROMPT_HINTS if hint in text)
        scored.append((neg_score, len(text), nid))
    scored.sort()  # lowest negative-hints first, then shortest text
    return scored[0][2]


def find_seed_node(workflow: dict) -> tuple[str, str] | None:
    """Return (node_id, seed_key) for a sampler-ish node."""
    seed_keys = ("seed", "noise_seed")
    for nid, node in workflow.items():
        for k in seed_keys:
            if k in (node.get("inputs") or {}):
                return nid, k
    return None


def slugify(text: str, n: int = 40) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return (s[:n] or "prompt").rstrip("-")


# ── job runner ──────────────────────────────────────────────────────
def run_one(workflow: dict, prompt: str, seed: int, *,
            timeout_s: int = 600, poll_s: float = 2.0) -> list[dict]:
    """Submit one job, wait for output, return the list of output file refs."""
    wf = json.loads(json.dumps(workflow))  # deep copy
    pnode = find_positive_prompt_node(wf)
    if not pnode:
        raise RuntimeError("no CLIPTextEncode node found in workflow")
    wf[pnode].setdefault("inputs", {})["text"] = prompt
    seed_loc = find_seed_node(wf)
    if seed_loc:
        nid, key = seed_loc
        wf[nid]["inputs"][key] = seed

    client_id = f"batch-{int(time.time()*1000)}-{random.randint(1000,9999)}"
    pid = post_prompt(wf, client_id)

    deadline = time.time() + timeout_s
    while time.time() < deadline:
        h = get_history(pid)
        if h and h.get("status", {}).get("completed"):
            outputs = []
            for node_outputs in (h.get("outputs") or {}).values():
                for key in ("images", "gifs", "videos", "files"):
                    for ref in node_outputs.get(key) or []:
                        outputs.append(ref)
            return outputs
        time.sleep(poll_s)
    raise TimeoutError(f"job {pid} did not finish in {timeout_s}s")


# ── main ────────────────────────────────────────────────────────────
WORKFLOWS = {
    "ltx": "ltx_video_t2v.json",
    "ltxi2v": "ltx_video_i2v.json",
    "flux": "flux_schnell_t2i.json",
}


def resolve_workflow_path(name: str, root: Path) -> Path:
    if name in WORKFLOWS:
        p = root / WORKFLOWS[name]
        if not p.exists():
            # fuzzy match — pull whichever ltx*/flux* file we have
            stem = name.replace("ltxi2v", "i2v").replace("ltx", "ltx")
            for c in sorted(root.glob("*.json")):
                if stem in c.name.lower():
                    return c
        return p
    p = Path(name)
    if p.is_file():
        return p
    raise SystemExit(f"workflow not found: {name}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--prompts", type=Path,
                    help="text file, one prompt per line")
    ap.add_argument("--prompts-text",
                    help="inline single prompt (for smoke tests)")
    ap.add_argument("--workflow", default="ltx",
                    help=f"one of {list(WORKFLOWS)} or a path to a .json")
    ap.add_argument("--workflows-dir", type=Path,
                    default=Path.home() / "ai-video" / "workflows")
    ap.add_argument("--out", type=Path,
                    default=Path.home() / "ai-video" / "outputs")
    ap.add_argument("--runs-csv", type=Path,
                    default=Path.home() / "ai-video" / "runs.csv")
    ap.add_argument("--concurrency", type=int, default=1,
                    help="(serial queue; ComfyUI is one job/process)")
    ap.add_argument("--seed", type=int, default=-1,
                    help="-1 = random per prompt")
    ap.add_argument("--tag", default="",
                    help="optional tag prepended to output filenames")
    args = ap.parse_args()

    if args.prompts and args.prompts_text:
        sys.exit("pass --prompts OR --prompts-text, not both")
    if args.prompts:
        prompts = [ln.strip() for ln in args.prompts.read_text().splitlines() if ln.strip() and not ln.startswith("#")]
    elif args.prompts_text:
        prompts = [args.prompts_text]
    else:
        sys.exit("need --prompts or --prompts-text")

    wf_path = resolve_workflow_path(args.workflow, args.workflows_dir)
    workflow = json.loads(wf_path.read_text())
    args.out.mkdir(parents=True, exist_ok=True)
    args.runs_csv.parent.mkdir(parents=True, exist_ok=True)
    new_csv = not args.runs_csv.exists()

    with args.runs_csv.open("a", newline="") as f:
        w = csv.writer(f)
        if new_csv:
            w.writerow(["ts", "tag", "workflow", "seed", "prompt", "duration_s", "output"])
        for idx, prompt in enumerate(prompts, start=1):
            seed = args.seed if args.seed >= 0 else random.randint(0, 2**31 - 1)
            t0 = time.time()
            try:
                outs = run_one(workflow, prompt, seed)
            except Exception as e:
                print(f"[err {idx}] {e}", file=sys.stderr)
                w.writerow([time.strftime("%FT%T"), args.tag, args.workflow, seed, prompt, f"{time.time()-t0:.1f}", f"ERROR: {e}"])
                continue
            duration = time.time() - t0
            saved = []
            for j, ref in enumerate(outs):
                blob = fetch_output(ref["filename"], ref.get("subfolder", ""), ref.get("type", "output"))
                ext = Path(ref["filename"]).suffix or ".bin"
                tag = (args.tag + "_") if args.tag else ""
                slug = slugify(prompt)
                name = f"{tag}{idx:03d}_{slug}_{j}{ext}"
                dest = args.out / name
                dest.write_bytes(blob)
                saved.append(str(dest))
                print(f"[ok  {idx}/{len(prompts)}] {duration:.1f}s · {dest.name}")
            w.writerow([time.strftime("%FT%T"), args.tag, args.workflow, seed, prompt, f"{duration:.1f}", ";".join(saved)])

    print(f"\ndone. log → {args.runs_csv}")


if __name__ == "__main__":
    main()
