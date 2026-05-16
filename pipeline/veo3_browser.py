"""Drive Google Vids' Veo 3 generator from your laptop via Playwright.

This script **must run from your own machine**, not from the dev
sandbox — every Google domain is firewalled here. It reuses your
already-signed-in Chrome profile so no credentials live in this repo.

One-time setup (on your laptop):

    python -m pip install playwright
    python -m playwright install chromium

Sign in to Google in your normal Chrome at least once. Find the
profile path:

    macOS   ~/Library/Application Support/Google/Chrome
    Linux   ~/.config/google-chrome
    Windows %LOCALAPPDATA%\\Google\\Chrome\\User Data

Then run:

    python pipeline/veo3_browser.py episodes/003-hormuz/ \\
        --chrome-profile "/Users/you/Library/Application Support/Google/Chrome" \\
        --profile-name "Default"

The script reads `episodes/NNN/veo3-runbook.md`, extracts the 7 prompt
blocks (### N · SceneName · Xs followed by a blockquote), and for
each: opens Vids → VO tool → pastes prompt → clicks Generate → waits
→ Insert → downloads → renames to episodes/NNN/broll/<SceneName>.mp4.

Idempotent: existing MP4s are skipped. Re-runs only re-generate the
missing ones.

**Heads up:** Google Vids' DOM selectors are not documented. This
scaffold uses ARIA roles + visible text, which is the most stable
strategy, but the first run may still need selector tweaks. Use
--manual to pause before each click for human confirmation.
"""
from __future__ import annotations

import argparse
import re
import sys
import time
from pathlib import Path

def _require_playwright():
    """Import playwright lazily so the parser can be unit-tested without it."""
    try:
        from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout  # noqa: F401
    except ImportError:
        sys.exit("playwright not installed. Run: pip install playwright && "
                 "python -m playwright install chromium")
    return sync_playwright, PWTimeout


VIDS_URL = "https://vids.google.com/"

# Generation can take 30–120s on Veo 3. We poll for the Insert button.
GEN_TIMEOUT_MS = 240_000

HEADER_RE = re.compile(
    r"^###\s+\d+\s+·\s+(?P<scene>\S+)\s+·\s+(?P<seconds>\d+(?:\.\d+)?)s\s*$",
    re.MULTILINE,
)


def parse_runbook(path: Path) -> list[dict]:
    """Parse veo3-runbook.md into a list of generation tasks.

    Block format:
        ### N · SceneName · Xs

        > prompt body line 1
        > prompt body line 2
    """
    text = path.read_text()
    blocks: list[dict] = []
    matches = list(HEADER_RE.finditer(text))
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end]
        lines = [
            line.lstrip("> ").rstrip()
            for line in body.splitlines()
            if line.strip().startswith(">")
        ]
        prompt = " ".join(lines).strip()
        if not prompt:
            continue
        blocks.append({
            "scene": m["scene"],
            "seconds": float(m["seconds"]),
            "prompt": prompt,
        })
    return blocks


def confirm(msg: str, manual: bool) -> None:
    if manual:
        input(f"  [pause] {msg} — press Enter to continue ")


def generate_one(page, task: dict, out_dir: Path, *, manual: bool, PWTimeout) -> Path | None:
    """One Vids generation cycle. Selectors are best-effort."""
    out_path = out_dir / f"{task['scene']}.mp4"
    if out_path.exists():
        print(f"[skip] {out_path.name} exists")
        return out_path

    print(f"[gen ] {task['scene']} · {task['seconds']}s")
    print(f"       {task['prompt'][:90]}{'…' if len(task['prompt']) > 90 else ''}")

    # 1. Make sure we are on a blank Vid + VO panel is visible.
    page.goto(VIDS_URL, wait_until="domcontentloaded")
    confirm("Vids loaded — open a Blank vid and click the VO tool", manual)

    # 2. Find the prompt textarea by accessibility role.
    #    Vids uses a role=textbox with a placeholder mentioning "Describe".
    textbox = page.get_by_role("textbox").filter(has_text="").first
    try:
        textbox.wait_for(timeout=15_000)
    except PWTimeout:
        sys.exit("Could not find Veo 3 prompt textbox. Open Vids → blank vid → "
                 "click 'VO' in the right toolbar manually, then re-run with "
                 "--manual to step through.")
    textbox.click()
    page.keyboard.press("Control+A")
    page.keyboard.press("Delete")
    page.keyboard.insert_text(task["prompt"])
    confirm("Prompt typed", manual)

    # 3. Click Generate (button by visible text).
    page.get_by_role("button", name=re.compile(r"^Generate$", re.I)).click()
    confirm("Generate clicked — waiting for clip", manual)

    # 4. Wait for the Insert button to appear (means generation finished).
    insert_btn = page.get_by_role("button", name=re.compile(r"^Insert$", re.I))
    insert_btn.wait_for(timeout=GEN_TIMEOUT_MS)
    confirm("Clip ready — click Insert", manual)
    insert_btn.click()

    # 5. File → Download → MP4. Capture the download to our broll dir.
    with page.expect_download(timeout=120_000) as dl_info:
        page.get_by_role("menuitem", name=re.compile(r"^File$", re.I)).click()
        page.get_by_role("menuitem", name=re.compile(r"^Download$", re.I)).click()
        page.get_by_role("menuitem", name=re.compile(r"MP4", re.I)).click()
    download = dl_info.value
    download.save_as(str(out_path))
    print(f"[ok  ] saved {out_path}")
    return out_path


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("episode_dir", type=Path,
                    help="e.g. episodes/003-hormuz/")
    ap.add_argument("--chrome-profile", required=True,
                    help="Path to your Chrome user-data dir (see top of file).")
    ap.add_argument("--profile-name", default="Default",
                    help="Which profile inside the user-data dir to use.")
    ap.add_argument("--headed", default=True,
                    help="Launch with a visible browser (default true).")
    ap.add_argument("--manual", action="store_true",
                    help="Pause after each automated step for confirmation.")
    args = ap.parse_args()

    episode_dir = args.episode_dir.resolve()
    runbook = episode_dir / "veo3-runbook.md"
    if not runbook.exists():
        sys.exit(f"missing: {runbook}")

    out_dir = episode_dir / "broll"
    out_dir.mkdir(exist_ok=True)

    tasks = parse_runbook(runbook)
    if not tasks:
        sys.exit(f"no prompt blocks found in {runbook}")

    print(f"[plan] {len(tasks)} clip(s) → {out_dir}")
    for t in tasks:
        print(f"       {t['scene']:>12s} · {t['seconds']}s")

    print(f"[chrome] profile {args.chrome_profile!r} / {args.profile_name!r}")

    sync_playwright, PWTimeout = _require_playwright()
    with sync_playwright() as pw:
        ctx = pw.chromium.launch_persistent_context(
            user_data_dir=args.chrome_profile,
            channel="chrome",
            headless=False,
            args=[f"--profile-directory={args.profile_name}"],
            accept_downloads=True,
        )
        try:
            page = ctx.pages[0] if ctx.pages else ctx.new_page()
            for t in tasks:
                try:
                    generate_one(page, t, out_dir, manual=args.manual,
                                 PWTimeout=PWTimeout)
                except KeyboardInterrupt:
                    print("\n[abort] keyboard interrupt — stopping cleanly.")
                    break
                except Exception as e:
                    print(f"[err ] {t['scene']}: {e}")
                    print("       skipping and continuing; re-run later.")
                    time.sleep(2)
        finally:
            ctx.close()
    print("[done]")


if __name__ == "__main__":
    main()
