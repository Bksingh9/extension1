# Pro Animated YouTube Channel — End-to-End Strategy
**Stack: Claude Code + Manim + Playwright MCP**

---

## 1. The Verdict — Why Manim Wins

Out of every open-source option (Manim, Motion Canvas, Revideo, Blender, OpenToonz, Synfig, Pencil2D), **Manim is the optimal core engine for a solo creator using Claude Code**.

| Criterion | Manim | Why it matters |
|---|---|---|
| Truly open source (MIT) | Yes | No license traps |
| Native 4K / HD / 60fps | Yes | YouTube-grade output |
| Pure code (Python) | Yes | Claude Code drives it perfectly |
| Proven channel quality | 3Blue1Brown, Reducible, Vcubingx | Top-tier YT content |
| LaTeX + math + graphs built-in | Yes | Instant credibility for explainers |
| Headless rendering | Yes | Run on any laptop, no GUI needed |
| Active community | ManimCE on GitHub | Fast answers, lots of examples |

**Supporting tools (all open source / free):**
- **Audio:** Audacity (editing) + Piper TTS (free voice synthesis) or your own mic
- **Final cut:** Kdenlive (or DaVinci Resolve free tier)
- **Thumbnails:** GIMP or Krita
- **Vector assets:** Inkscape
- **Browser automation:** Playwright MCP (research, scraping, upload, monitoring)

---

## 2. Full Stack — Install Commands

```bash
# Core: Python + Manim Community Edition
brew install python@3.11 ffmpeg pkg-config cairo pango          # macOS
# Linux: sudo apt install python3.11 ffmpeg libcairo2-dev libpango1.0-dev

python3 -m venv .venv && source .venv/bin/activate
pip install manim manim-voiceover[piper]

# LaTeX (for equations, beautiful text)
brew install --cask mactex-no-gui                               # macOS
# Linux: sudo apt install texlive texlive-latex-extra

# Editing + audio
brew install --cask kdenlive
brew install --cask audacity

# Voice synthesis (open source, runs locally)
pip install piper-tts

# Claude Code
npm install -g @anthropic-ai/claude-code

# Playwright MCP (browser automation for Claude Code)
claude mcp add playwright npx '@playwright/mcp@latest'
```

After install, run `claude` in your project folder. Claude Code picks up the Playwright MCP automatically.

---

## 3. Project Structure

```
my-yt-channel/
├── CLAUDE.md                    # Persistent instructions for Claude Code
├── channel/
│   ├── brand.md                 # Voice, tone, visual identity, colors
│   ├── niche.md                 # Topics, angles, do/don't list
│   └── competitors.md           # 5–10 channels you study
├── episodes/
│   ├── 001-topic-name/
│   │   ├── research.md          # Sources, facts, claims (Playwright-gathered)
│   │   ├── script.md            # Voiceover-ready script with scene markers
│   │   ├── storyboard.md        # Scene-by-scene visual descriptions
│   │   ├── scene.py             # Manim code (Claude Code writes this)
│   │   ├── audio/               # VO files
│   │   ├── render/              # Output mp4s
│   │   └── thumbnail.png
│   └── 002-...
├── shared/
│   ├── styles.py                # Reusable Manim mobjects, colors, fonts
│   ├── intros.py                # Standard intro/outro animations
│   └── assets/                  # Logos, recurring SVGs
├── pipeline/
│   ├── render.sh                # `manim -qk -p scene.py SceneName` (4K)
│   ├── upload.py                # Playwright/YT API upload script
│   └── thumbnail-research.py    # Playwright competitor thumbnail scraper
└── manim.cfg                    # 4K, 60fps, transparent bg defaults
```

`manim.cfg` for YouTube-grade output:
```ini
[CLI]
quality = fourk_quality
frame_rate = 60
background_color = "#0e0e10"
```

---

## 4. The 10-Step Production Pipeline

### Step 1 — Topic discovery
- **Claude Code:** Reads `channel/niche.md`, brainstorms 10 candidates.
- **Playwright MCP:** Pulls YouTube search, trending, Google Trends, Reddit, HN, X. Returns titles, view counts, recency. Claude ranks them by demand-vs-supply.

### Step 2 — Competitive research
- **Playwright MCP:** Visits the top 5 videos on the topic. Scrapes titles, descriptions, thumbnails, top comments, length. Saves screenshots of each thumbnail to `episodes/NNN/competitor-refs/`.
- **Claude Code:** Identifies the angle gap nobody's covering, writes a positioning memo.

### Step 3 — Deep research
- **Playwright MCP:** Wikipedia, primary sources, papers, news (within site ToS).
- **Claude Code:** Synthesizes into `research.md` with citations. You spot-check.

### Step 4 — Script writing
- **Claude Code:** Writes `script.md` based on research + voice in `brand.md`. Hook in first 8 seconds, payoff every 30s.
- You: edit ruthlessly. Read aloud. Cut 20%.

### Step 5 — Storyboard
- **Claude Code:** Converts each script paragraph into one scene description in `storyboard.md`. Format: `[Scene 1, 0:00–0:08] Visual | Text | Animation`.

### Step 6 — Animate
- **Claude Code:** Writes `scene.py` using Manim, pulling reusable components from `shared/styles.py`. One Python class per scene.
- Iteration loop: `manim -ql scene.py Scene1` → review → fix → repeat. Render in 4K only at the end.

### Step 7 — Voiceover
- **A (free):** Piper TTS via `manim-voiceover`. Auto-syncs VO to animation.
- **B (paid, better):** ElevenLabs.
- **C (best long-term):** Your own voice via Audacity, then Claude Code generates SRT timing.

### Step 8 — Final edit
- **Kdenlive** or **DaVinci Resolve:** combine 4K Manim renders + VO + background music (YouTube Audio Library or Pixabay Music) + sound effects (Freesound.org).
- **Claude Code:** writes a Kdenlive XML or generates an FFmpeg one-liner if the edit is simple.

### Step 9 — Thumbnail + metadata
- **Playwright MCP:** Re-scrapes top-10 thumbnails for your topic.
- **Claude Code:** Drafts 5 title variants (CTR-optimized), description, tags, end-screen text. Generates SVG thumbnail draft you finish in GIMP.

### Step 10 — Upload + monitor
- **Playwright MCP:** Logs into YouTube Studio, uploads, sets thumbnail, schedules. (YT Data API is more reliable for upload itself; Playwright shines for things the API doesn't expose.)
- **Playwright MCP** post-launch: checks views/CTR/retention every 6 hours for the first 48 hours; scrapes top comments. Claude Code clusters audience reaction → feeds into next episode's research.

---

## 5. Playwright MCP — The Force Multiplier

Why it matters specifically for a YT channel: every successful animated channel runs on *research velocity*. Playwright MCP turns Claude Code into a research analyst.

High-leverage uses:
1. **Trend mining** — daily YT trending scrape; Claude flags rising topics before they peak.
2. **Title/thumbnail intel** — historical title changes via VidIQ/Social Blade.
3. **Source verification** — for any claim, Playwright fetches 3 independent sources; Claude flags unsupported claims.
4. **Comment intelligence** — your own + competitors' comments clustered into FAQ → next-video ideas.
5. **Auto-publish** — schedule uploads, set thumbnails, edit metadata, post community tab.
6. **Asset gathering** — reference images, charts, stock footage links, Wikipedia diagrams.
7. **Distribution** — auto-cross-post to X, Reddit, LinkedIn after upload.

`CLAUDE.md` snippet to enable this workflow:
```markdown
- Before writing any script, use Playwright MCP to:
  1. Search YouTube for the topic; capture top 10 video titles + view counts.
  2. Read the top 3 video descriptions.
  3. Save findings to episodes/NNN/research.md with sources.
- Never claim a fact in a script without a cited source in research.md.
- Render previews in -ql, finals in -qk (4K). Default 60fps.
- Use shared/styles.py for all colors and fonts.
```

---

## 6. Niche Selection — Pick Once, Commit Hard

Animated channels win when **format = the moat**. Best-fit niches for Manim/code-animation:

- **Tier S (animation is essential):** math, physics, computer science, cryptography, AI concepts, statistics, economics, finance fundamentals.
- **Tier A (animation is a strong differentiator):** history with maps, geopolitics, biology/evolution, psychology, philosophy, "how things work," product breakdowns.
- **Tier B (works but crowded):** news recaps, tech reviews, business case studies.
- **Avoid:** vlog-style, talking head, react content, anything where face/personality drives engagement.

**Selection rule:** Pick a niche where you can plausibly publish 50 videos without running out of ideas. Sub-niche aggressively (not "finance" → "Indian retail investor mistakes," not "history" → "forgotten engineering disasters").

---

## 7. First 90 Days — Realistic Roadmap

- **Week 1:** Install full stack. Render the Manim sample gallery. Read 3 channels in your target niche; write `competitors.md`. Lock niche + visual identity.
- **Week 2:** Ship Episode 001 (4–6 minutes, not 15). Use it to debug your pipeline.
- **Weeks 3–4:** Episodes 002, 003. By now `shared/styles.py` is reusable; Episode 4 takes half the time.
- **Months 2–3:** Weekly cadence. 12 videos shipped. By video 10 you'll know your CTR, retention, and which thumbnail style works.

**Targets at 90 days:** 12 videos, 1k subscribers (achievable in Tier S/A niches with consistent quality), one breakout video (>10× your average views).

---

## 8. Monetization Path

- **0–1k subs:** $0. Building.
- **1k subs + 4k watch hours:** YouTube Partner Program; ad revenue starts (~$1–5 RPM in Tier S/A).
- **5k–10k subs:** Sponsorships start coming inbound; $200–800 per integration.
- **20k+ subs:** Course, Patreon, or product. This is where animated educators actually make money — not ads.

Don't optimize for ads. Optimize for the email list and the eventual product.

---

## 9. Critical Don'ts

- Don't render in 4K during iteration — use `-ql`. 4K only for finals.
- Don't put all scenes in one Python file beyond ~300 lines; split per scene.
- Don't skip the script-aloud read; bad scripts kill animated videos faster than bad animation.
- Don't use Playwright MCP to scrape sites that block it / violate ToS. YouTube Data API is the right tool for upload/analytics.
- Don't publish without watching the final on a phone screen first. Most viewers are mobile.

---

## 10. Day-1 Action List

1. Install the stack (Section 2).
2. Create the project folder (Section 3).
3. Drop this strategy file into the project root.
4. Write `channel/niche.md` (one paragraph: who it's for, what they'll learn, why they'll come back).
5. Run `claude` in the folder. Tell it: *"Read CLAUDE.md and STRATEGY.md. Use Playwright MCP to research the top 10 channels in my niche and write competitors.md."*
6. Ship Episode 001 within 14 days. Quality is iteration, not preparation.

---

*Last updated 2026-04-26.*
