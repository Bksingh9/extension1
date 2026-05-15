"""Generate AI B-roll for an episode using LTX-Video.

This script is **a wrapper, not a worker**. It cannot run from this
sandbox (no GPU, no Hugging Face access). Run it on a GPU host:
your own machine, RunPod, Modal, or Colab Pro. See
`tools/video-gen.md` for the full runbook.

Usage:
    python pipeline/broll.py episodes/003-hormuz/

It looks for `<episode_dir>/broll-prompts.md`, which must contain
blocks of the form:

    ## SCENE_NAME · duration_seconds · width x height
    prompt text on one or more lines until the next blank line.

For each block, it calls LTX-Video inference and writes the MP4 to
`<episode_dir>/broll/<scene>.mp4`. Existing files are skipped so
re-runs are idempotent.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
LTX_REPO = REPO_ROOT / "tools" / "LTX-Video"
DEFAULT_CONFIG = LTX_REPO / "configs" / "ltxv-13b-0.9.8-distilled.yaml"


def parse_prompts(path: Path) -> list[dict]:
    """Parse a broll-prompts.md into a list of generation tasks.

    Block format:
        ## <scene> · <seconds>s · <width>x<height>
        <prompt body, can span multiple lines>
        <blank line ends the block>
    """
    text = path.read_text()
    blocks: list[dict] = []
    header_re = re.compile(
        r"^##\s+(?P<scene>\S+)\s+·\s+(?P<seconds>\d+(?:\.\d+)?)s\s+·\s+"
        r"(?P<w>\d+)x(?P<h>\d+)\s*$",
        re.MULTILINE,
    )
    for m in header_re.finditer(text):
        end = text.find("\n##", m.end())
        body = text[m.end():end if end != -1 else len(text)].strip()
        if not body:
            continue
        # Strip leading blank lines.
        body = re.sub(r"\A\s+", "", body)
        blocks.append({
            "scene": m["scene"],
            "seconds": float(m["seconds"]),
            "width": int(m["w"]),
            "height": int(m["h"]),
            "prompt": body,
        })
    return blocks


def run_ltx(
    task: dict,
    out_dir: Path,
    *,
    pipeline_config: Path,
    seed: int,
    fps: int = 24,
    dry_run: bool = False,
) -> Path | None:
    """Invoke LTX-Video inference.py for one B-roll clip."""
    out_path = out_dir / f"{task['scene']}.mp4"
    if out_path.exists():
        print(f"[skip] {out_path.name} exists")
        return out_path

    num_frames = max(1, int(round(task["seconds"] * fps)))
    cmd = [
        sys.executable, str(LTX_REPO / "inference.py"),
        "--prompt", task["prompt"],
        "--output_path", str(out_path),
        "--pipeline_config", str(pipeline_config),
        "--seed", str(seed),
        "--height", str(task["height"]),
        "--width", str(task["width"]),
        "--num_frames", str(num_frames),
    ]
    print(f"[gen ] {task['scene']} · {task['seconds']}s · {task['width']}x{task['height']}")
    print(f"       prompt: {task['prompt'][:80]}{'…' if len(task['prompt']) > 80 else ''}")
    if dry_run:
        print(f"       cmd: {' '.join(cmd)}")
        return None
    subprocess.run(cmd, check=True)
    return out_path


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("episode_dir", type=Path,
                    help="e.g. episodes/003-hormuz/")
    ap.add_argument("--pipeline_config", type=Path, default=DEFAULT_CONFIG,
                    help="LTX-Video pipeline config yaml")
    ap.add_argument("--seed", type=int, default=0xD05512)
    ap.add_argument("--fps", type=int, default=24,
                    help="output fps used to compute num_frames")
    ap.add_argument("--dry-run", action="store_true",
                    help="print the commands without executing")
    args = ap.parse_args()

    episode_dir = args.episode_dir.resolve()
    prompts_path = episode_dir / "broll-prompts.md"
    if not prompts_path.exists():
        sys.exit(f"missing: {prompts_path}")

    out_dir = episode_dir / "broll"
    out_dir.mkdir(exist_ok=True)

    tasks = parse_prompts(prompts_path)
    if not tasks:
        sys.exit(f"no prompt blocks found in {prompts_path}")

    print(f"[plan] {len(tasks)} clip(s) → {out_dir}")
    for t in tasks:
        run_ltx(
            t, out_dir,
            pipeline_config=args.pipeline_config,
            seed=args.seed,
            fps=args.fps,
            dry_run=args.dry_run,
        )
    print("[done]")


if __name__ == "__main__":
    main()
