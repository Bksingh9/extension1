# Prompt 2 — New Episode

Paste this at the start of each new video, replacing `<TOPIC>`.

```
New episode: <TOPIC>.

Follow the standard pipeline in CLAUDE.md. Specifically:

1. Use Playwright MCP to:
   - Search YouTube for this topic. Save top 10 titles, view counts,
     thumbnail screenshots to episodes/NNN/competitor-refs/.
   - Pull 5 primary sources (Wikipedia + 2 papers/news + 2 niche-specific
     authoritative sites). Extract key facts.

2. Write episodes/NNN/research.md with cited facts.

3. Identify the angle gap — what are the existing top videos NOT covering?
   Write a one-paragraph positioning memo at the top of research.md.

4. Draft script.md (700–900 words). Structure:
   - Hook (2 sentences, contrarian or surprising)
   - Setup (what's commonly believed)
   - Reveal (the angle gap from step 3)
   - Walk-through (3–5 beats, each ~100 words)
   - Payoff + CTA

5. Build storyboard.md scene-by-scene.

6. Write scene.py for the first 90 seconds only. Render -ql preview.

7. Stop. Show me the preview, the script, and the top 3 candidate titles.
   Wait for my notes before continuing.
```
