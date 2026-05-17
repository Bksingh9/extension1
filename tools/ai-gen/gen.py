"""Free batch video + image generation via Hugging Face ZeroGPU Spaces.

No local GPU. No payment. Drives Spaces over `gradio_client`. Reads
config from ~/ai-gen/config/spaces.yaml, writes outputs to
~/ai-gen/outputs/YYYY-MM-DD/, logs every run to ~/ai-gen/logs/runs.csv.

Subcommands:
    gen.py image --prompt "..." --space evalstate/flux1_schnell --n 4
    gen.py video --prompt "..." --space Lightricks/ltx-video-distilled
    gen.py batch --file prompts/clips.txt --kind video --space auto
    gen.py list-spaces
    gen.py probe <space_id>
    gen.py health
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import random
import shutil
import sys
import time
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("missing pyyaml. Run setup.sh or `pip install pyyaml`.")

try:
    from gradio_client import Client
except ImportError:
    sys.exit("missing gradio_client. Run setup.sh or `pip install gradio_client`.")

try:
    from slugify import slugify
except ImportError:  # python-slugify
    def slugify(text: str) -> str:
        import re
        return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "prompt"

try:
    from rich.console import Console
    from rich.table import Table
    _console = Console()
    def info(msg: str) -> None: _console.print(msg)
except ImportError:
    _console = None
    def info(msg: str) -> None: print(msg)

# ── paths ────────────────────────────────────────────────────────────
ROOT = Path(os.environ.get("AI_GEN_ROOT", Path.home() / "ai-gen"))
CFG_DIR = ROOT / "config"
SPACES_YAML = CFG_DIR / "spaces.yaml"
LOGS_DIR = ROOT / "logs"
OUT_DIR = ROOT / "outputs"
RUNS_CSV = LOGS_DIR / "runs.csv"
ENV_FILE = ROOT / ".env"

VIDEO_EXTS = {".mp4", ".webm", ".mov", ".gif"}
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}

PROMPT_ARG_HINTS = (
    "prompt", "text", "input_text", "description", "caption",
    "user_prompt", "positive_prompt",
)
SEED_ARG_HINTS = ("seed", "noise_seed", "random_seed")
NEG_ARG_HINTS = ("negative_prompt", "negative")

QUEUE_TIMEOUT_S = 600        # 10 min — per spec
INTER_SUBMIT_DELAY_S = 5     # per spec
MAX_RETRIES = 3              # per spec


# ── env / token ─────────────────────────────────────────────────────
def load_env() -> None:
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def hf_login() -> str | None:
    token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_HUB_TOKEN")
    if not token:
        info("[yellow]no HF_TOKEN in env or .env — running anonymously (quota will be tighter)[/]"
             if _console else "no HF_TOKEN — running anonymously")
        return None
    try:
        from huggingface_hub import login
        login(token=token, add_to_git_credential=False)
        return token
    except Exception as e:
        info(f"hf login failed: {e}")
        return None


# ── config helpers ──────────────────────────────────────────────────
def load_spaces() -> dict[str, list[dict]]:
    if not SPACES_YAML.exists():
        sys.exit(f"missing config: {SPACES_YAML}")
    data = yaml.safe_load(SPACES_YAML.read_text()) or {}
    return {k: v or [] for k, v in data.items()}


def schema_cache_path(space_id: str) -> Path:
    safe = space_id.replace("/", "__")
    return CFG_DIR / f"{safe}.json"


def load_schema(space_id: str) -> dict | None:
    p = schema_cache_path(space_id)
    return json.loads(p.read_text()) if p.exists() else None


def save_schema(space_id: str, schema: dict) -> None:
    p = schema_cache_path(space_id)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(schema, indent=2, default=str))


def fetch_schema(space_id: str, *, hf_token: str | None) -> dict:
    cached = load_schema(space_id)
    if cached:
        return cached
    info(f"  probing API of {space_id} …")
    client = Client(space_id, hf_token=hf_token)
    api = client.view_api(return_format="dict")
    if not isinstance(api, dict):
        api = {"named_endpoints": {}, "unnamed_endpoints": {}, "raw": str(api)}
    fn, prompt_arg, seed_arg, neg_arg, extras = pick_endpoint(api)
    schema = {
        "space_id": space_id,
        "fn": fn,
        "prompt_arg": prompt_arg,
        "seed_arg": seed_arg,
        "neg_arg": neg_arg,
        "extras": extras,
        "api_raw": api,
    }
    save_schema(space_id, schema)
    return schema


def pick_endpoint(api: dict) -> tuple[str, str | None, str | None, str | None, dict]:
    """Heuristically pick the predict endpoint and locate prompt/seed args."""
    named = api.get("named_endpoints") or {}
    unnamed = api.get("unnamed_endpoints") or {}
    candidates: list[tuple[str, list[dict]]] = []
    for name, ep in named.items():
        candidates.append((name, ep.get("parameters") or []))
    for idx, ep in unnamed.items():
        candidates.append((f"#{idx}", ep.get("parameters") or []))

    best = None
    for fn, params in candidates:
        names = [(p.get("parameter_name") or p.get("label") or "").lower() for p in params]
        score = sum(1 for n in names if any(h in n for h in PROMPT_ARG_HINTS))
        score += 1 if any("image" in n or "file" in n for n in names) else 0
        if score and (best is None or score > best[0]):
            best = (score, fn, params, names)

    if best is None:
        fn = next(iter(named), next(iter(unnamed), "/predict"))
        return fn, None, None, None, {}

    _, fn, params, names = best
    prompt_arg = seed_arg = neg_arg = None
    extras: dict = {}
    for p, n in zip(params, names):
        pname = p.get("parameter_name") or p.get("label") or n
        if not pname:
            continue
        if prompt_arg is None and any(h in n for h in PROMPT_ARG_HINTS):
            prompt_arg = pname; continue
        if seed_arg is None and any(h in n for h in SEED_ARG_HINTS):
            seed_arg = pname; continue
        if neg_arg is None and any(h in n for h in NEG_ARG_HINTS):
            neg_arg = pname; continue
        # collect example/default for extras
        default = p.get("parameter_default", p.get("python_type", {}).get("description"))
        if default not in (None, "", "Any"):
            extras[pname] = default
    return fn, prompt_arg, seed_arg, neg_arg, extras


# ── space dispatch ──────────────────────────────────────────────────
def call_space(space_id: str, prompt: str, *, hf_token: str | None,
               seed: int | None = None, extras: dict | None = None,
               negative: str | None = None) -> list[Path]:
    schema = fetch_schema(space_id, hf_token=hf_token)
    fn = schema.get("fn") or "/predict"
    prompt_arg = schema.get("prompt_arg")
    seed_arg = schema.get("seed_arg")
    neg_arg = schema.get("neg_arg")
    base_extras = dict(schema.get("extras") or {})
    if extras:
        base_extras.update(extras)

    kwargs: dict = {}
    if prompt_arg:
        kwargs[prompt_arg] = prompt
    if seed is not None and seed_arg:
        kwargs[seed_arg] = seed
    if negative and neg_arg:
        kwargs[neg_arg] = negative
    for k, v in base_extras.items():
        kwargs.setdefault(k, v)

    client = Client(space_id, hf_token=hf_token)
    if kwargs:
        result = client.predict(**kwargs, api_name=fn) if fn.startswith("/") else client.predict(**kwargs, fn_index=int(fn.lstrip("#")))
    else:
        # last-ditch: positional prompt as first arg
        result = client.predict(prompt, api_name=fn) if fn.startswith("/") else client.predict(prompt, fn_index=int(fn.lstrip("#")))

    return _collect_paths(result)


def _collect_paths(result) -> list[Path]:
    """gradio_client returns either str, dict, list, tuple. Find file paths."""
    paths: list[Path] = []
    def walk(x):
        if x is None:
            return
        if isinstance(x, (list, tuple)):
            for y in x:
                walk(y)
            return
        if isinstance(x, dict):
            for k in ("path", "file", "name", "video", "image"):
                v = x.get(k)
                if isinstance(v, str) and Path(v).exists():
                    paths.append(Path(v)); return
            for v in x.values():
                walk(v)
            return
        if isinstance(x, str) and (x.startswith("/") or x.startswith("./")) and Path(x).exists():
            paths.append(Path(x))
    walk(result)
    return paths


# ── output saving / logging ─────────────────────────────────────────
def save_outputs(srcs: list[Path], *, idx: int, prompt: str, tag: str = "") -> list[Path]:
    today = OUT_DIR / date.today().isoformat()
    today.mkdir(parents=True, exist_ok=True)
    saved = []
    slug = slugify(prompt)[:50]
    for j, src in enumerate(srcs):
        ext = src.suffix or ".bin"
        tag_p = (tag + "_") if tag else ""
        dest = today / f"{tag_p}{idx:03d}_{slug}_{j}{ext}"
        shutil.copy2(src, dest)
        saved.append(dest)
    return saved


def append_run(row: dict) -> None:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    new = not RUNS_CSV.exists()
    with RUNS_CSV.open("a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["ts", "space", "prompt", "seed", "duration_sec", "output_path", "status"])
        w.writerow([row["ts"], row["space"], row["prompt"], row["seed"],
                    row["duration_sec"], row["output_path"], row["status"]])


def run_one(space_id: str, prompt: str, *, hf_token: str | None,
            seed: int | None, idx: int, tag: str = "") -> tuple[bool, list[Path], str]:
    t0 = time.time()
    try:
        srcs = call_space(space_id, prompt, hf_token=hf_token, seed=seed)
    except Exception as e:
        dur = time.time() - t0
        append_run({
            "ts": time.strftime("%FT%T"), "space": space_id, "prompt": prompt,
            "seed": seed if seed is not None else "", "duration_sec": f"{dur:.1f}",
            "output_path": "", "status": f"ERROR: {e}",
        })
        return False, [], f"{type(e).__name__}: {e}"
    dur = time.time() - t0
    saved = save_outputs(srcs, idx=idx, prompt=prompt, tag=tag)
    append_run({
        "ts": time.strftime("%FT%T"), "space": space_id, "prompt": prompt,
        "seed": seed if seed is not None else "", "duration_sec": f"{dur:.1f}",
        "output_path": ";".join(str(p) for p in saved), "status": "ok",
    })
    return True, saved, "ok"


# ── auto / health ───────────────────────────────────────────────────
def health_check(space_id: str, *, hf_token: str | None, timeout_s: int = 30) -> tuple[bool, str]:
    """Quick health check — try to view_api with short timeout."""
    try:
        url = f"https://huggingface.co/api/spaces/{space_id}"
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {hf_token}"} if hf_token else {})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
        runtime = (data.get("runtime") or {}).get("stage") or data.get("stage")
        if runtime and runtime.upper() not in ("RUNNING", "RUNNING_BUILDING", "RUNNING_APP_STARTING"):
            return False, f"stage={runtime}"
    except urllib.error.HTTPError as e:
        return False, f"http {e.code}"
    except Exception as e:
        return False, f"{type(e).__name__}"
    # Verify gradio_client can reach it
    try:
        Client(space_id, hf_token=hf_token, verbose=False)
        return True, "running"
    except Exception as e:
        return False, f"client: {type(e).__name__}"


def pick_auto_space(kind: str, spaces: dict, *, hf_token: str | None) -> str | None:
    for entry in spaces.get(kind, []):
        sid = entry["id"]
        ok, msg = health_check(sid, hf_token=hf_token)
        info(f"  {sid:50s} → {'✅' if ok else '❌'} {msg}")
        if ok:
            return sid
    return None


# ── subcommands ─────────────────────────────────────────────────────
def cmd_image(args, spaces, token):
    kind = "image"
    space_id = resolve_space(args.space, spaces, kind, token)
    if not space_id: return 1
    seed_pool = [random.randint(0, 2**31 - 1) for _ in range(args.n)]
    for i, seed in enumerate(seed_pool, 1):
        info(f"[{i}/{args.n}] {space_id} · seed={seed}")
        ok, saved, msg = run_one(space_id, args.prompt, hf_token=token, seed=seed, idx=i, tag=args.tag or "")
        info(f"  {'✅' if ok else '❌'} {msg} · {[str(p) for p in saved]}")
        time.sleep(INTER_SUBMIT_DELAY_S)
    return 0


def cmd_video(args, spaces, token):
    kind = "video"
    space_id = resolve_space(args.space, spaces, kind, token)
    if not space_id: return 1
    n = args.n
    for i in range(1, n + 1):
        seed = random.randint(0, 2**31 - 1)
        info(f"[{i}/{n}] {space_id} · seed={seed}")
        ok, saved, msg = run_one(space_id, args.prompt, hf_token=token, seed=seed, idx=i, tag=args.tag or "")
        info(f"  {'✅' if ok else '❌'} {msg} · {[str(p) for p in saved]}")
        time.sleep(INTER_SUBMIT_DELAY_S)
    return 0


def cmd_batch(args, spaces, token):
    prompts = [ln.strip() for ln in Path(args.file).read_text().splitlines() if ln.strip() and not ln.startswith("#")]
    if not prompts: sys.exit("no prompts in file")
    kind = args.kind
    space_ids = [e["id"] for e in spaces.get(kind, [])] if args.space == "auto" else [args.space]
    if not space_ids: sys.exit(f"no spaces configured for kind={kind}")
    info(f"plan: {len(prompts)} prompts · kind={kind} · candidates={space_ids}")
    for i, prompt in enumerate(prompts, 1):
        seed = random.randint(0, 2**31 - 1)
        success = False
        for attempt, sid in enumerate(space_ids[:MAX_RETRIES], 1):
            if attempt > 1: info(f"  retrying via {sid}")
            ok, saved, msg = run_one(sid, prompt, hf_token=token, seed=seed, idx=i, tag=args.tag or "")
            info(f"  [{i}/{len(prompts)}] {sid:40s} {'✅' if ok else '❌'} {msg}")
            if ok:
                success = True; break
        if not success:
            info(f"  ⚠️  all candidates failed for prompt {i}")
        time.sleep(INTER_SUBMIT_DELAY_S)
    return 0


def cmd_list_spaces(args, spaces, token):
    if _console:
        for kind, entries in spaces.items():
            table = Table(title=f"{kind} spaces", show_lines=False)
            table.add_column("id"); table.add_column("note")
            for e in entries:
                table.add_row(e["id"], e.get("note", ""))
            _console.print(table)
    else:
        for kind, entries in spaces.items():
            print(f"\n{kind}:")
            for e in entries:
                print(f"  {e['id']:50s} {e.get('note','')}")
    return 0


def cmd_probe(args, spaces, token):
    sid = args.space_id
    schema_cache_path(sid).unlink(missing_ok=True)
    schema = fetch_schema(sid, hf_token=token)
    print(json.dumps({
        "space_id": sid,
        "fn": schema["fn"],
        "prompt_arg": schema["prompt_arg"],
        "seed_arg": schema["seed_arg"],
        "neg_arg": schema["neg_arg"],
        "extras": schema["extras"],
    }, indent=2))
    return 0


def cmd_health(args, spaces, token):
    for kind, entries in spaces.items():
        info(f"\n[{kind}]")
        for e in entries:
            ok, msg = health_check(e["id"], hf_token=token)
            info(f"  {e['id']:50s} {'✅' if ok else '❌'} {msg}")
    if token:
        try:
            from huggingface_hub import HfApi
            who = HfApi().whoami(token=token)
            info(f"\nuser: {who.get('name')} (plan: {who.get('plan', 'free')})")
        except Exception as e:
            info(f"\nwhoami failed: {e}")
    info("\nZeroGPU quota: visible at https://huggingface.co/settings/billing — "
         "free accounts get ~5 min/day of ZeroGPU compute, varies by Space.")
    return 0


def resolve_space(arg: str, spaces: dict, kind: str, token: str | None) -> str | None:
    if arg and arg != "auto":
        return arg
    info(f"selecting auto space for kind={kind}…")
    sid = pick_auto_space(kind, spaces, hf_token=token)
    if not sid:
        info("❌ no healthy space found")
    return sid


# ── main ────────────────────────────────────────────────────────────
def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_img = sub.add_parser("image"); p_img.add_argument("--prompt", required=True)
    p_img.add_argument("--space", default="auto"); p_img.add_argument("--n", type=int, default=1)
    p_img.add_argument("--tag", default="")

    p_vid = sub.add_parser("video"); p_vid.add_argument("--prompt", required=True)
    p_vid.add_argument("--space", default="auto"); p_vid.add_argument("--n", type=int, default=1)
    p_vid.add_argument("--tag", default="")

    p_b = sub.add_parser("batch"); p_b.add_argument("--file", required=True)
    p_b.add_argument("--kind", choices=["image", "video"], default="video")
    p_b.add_argument("--space", default="auto"); p_b.add_argument("--tag", default="")

    sub.add_parser("list-spaces")
    p_pr = sub.add_parser("probe"); p_pr.add_argument("space_id")
    sub.add_parser("health")

    args = ap.parse_args()
    load_env()
    spaces = load_spaces()
    token = hf_login()

    handler = {
        "image": cmd_image, "video": cmd_video, "batch": cmd_batch,
        "list-spaces": cmd_list_spaces, "probe": cmd_probe, "health": cmd_health,
    }[args.cmd]
    sys.exit(handler(args, spaces, token) or 0)


if __name__ == "__main__":
    main()
