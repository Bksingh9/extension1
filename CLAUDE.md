# CLAUDE.md — Project rules for Claude Code

These rules apply to every Claude Code session in this repo. Read once at session start.

## Pipeline rules

- **Preview with `-ql`** during iteration. Render finals with `-qk` (4K). Never iterate at 4K.
- **Cite every factual claim.** Each fact in a script must have a source URL in `episodes/NNN/research.md`. No citation, no claim.
- **Use `shared/styles.py`** for every color, font, title card, and lower-third. Never hardcode colors anywhere else.
- **Playwright MCP first.** Before writing any script, run niche/topic research via Playwright MCP and save findings to `episodes/NNN/research.md` (with screenshots under `episodes/NNN/competitor-refs/` and `channel/research-screenshots/`).
- **Script length:** ≤ 900 words for a 6-minute video. Hook in the first 2 sentences. Mark scenes with `[SCENE 1 — 0:00–0:08]`.
- **Render output:** 4K, 60fps, background `#0e0e10`. Default media dir is `media/` (configured in `manim.cfg`).
- **Per-episode order:** write `research.md` → `script.md` → `storyboard.md` → `scene.py`. Do not skip ahead.

## File structure

See `STRATEGY.md` for the full layout and rationale. Quick map:

- `channel/` — brand, niche, competitors. Stable across episodes.
- `episodes/NNN-slug/` — one folder per video.
- `shared/styles.py`, `shared/intros.py` — reusable Manim primitives.
- `pipeline/` — render + research helpers; reusable prompts in `pipeline/prompts/`.

## Workflow prompts

- New episode: `pipeline/prompts/new-episode.md`
- Weekly trend scan: `pipeline/prompts/weekly-trend-scan.md`

## Rendering

Use the helper rather than calling `manim` directly:

```bash
./pipeline/render.sh episodes/001-pilot/scene.py Hook -ql   # preview
./pipeline/render.sh episodes/001-pilot/scene.py Hook       # 4K final (default -qk)
```

## Branch policy

- Develop on `claude/setup-youtube-production-GYo4W` (or whatever branch the user assigns).
- Commit with descriptive messages. Push with `-u origin <branch>`.
- Never push to `main` without explicit permission.
