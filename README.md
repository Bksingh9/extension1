# Animated YouTube Channel — Production Repo

Stack: **Claude Code + Manim + Playwright MCP**, with FFmpeg, Piper TTS, Audacity/Kdenlive.

## Quick start

```bash
# 1. System deps (Ubuntu 24.04)
sudo apt update
sudo apt install -y ffmpeg build-essential python3-dev libcairo2-dev \
  libpango1.0-dev libffi-dev pkg-config texlive texlive-latex-extra \
  texlive-fonts-extra texlive-science dvisvgm

# 2. Python env + Manim
python3 -m venv .venv && source .venv/bin/activate
pip install manim manim-voiceover[piper]

# 3. Playwright MCP for Claude Code
claude mcp add playwright npx '@playwright/mcp@latest'
```

## Layout

```
.
├── CLAUDE.md                # Rules for Claude Code (read first)
├── STRATEGY.md              # End-to-end channel strategy
├── manim.cfg                # 4K, 60fps, BG #0e0e10
├── channel/                 # Brand, niche, competitor research
├── episodes/NNN-slug/       # One folder per video
├── shared/                  # Reusable Manim styles + intros
└── pipeline/                # render.sh, research.py, reusable prompts/
```

## Day-to-day commands

```bash
# Preview a scene (low quality, fast)
./pipeline/render.sh episodes/001-pilot/scene.py Hook -ql

# Final render (4K, 60fps)
./pipeline/render.sh episodes/001-pilot/scene.py Hook
```

See `STRATEGY.md` for the full pipeline and `CLAUDE.md` for project rules.
