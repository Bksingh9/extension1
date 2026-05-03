# The Long Light — Edit workflow

> Phase 7 deliverable. End-to-end production workflow per episode.
> Two paths documented: the **lean image-+-CapCut path** (recommended
> for The Long Light's image-driven format) and the **Manim path**
> (used by The Dossier; documented here for cross-channel reuse).

## TL;DR — 7 steps from script to upload

1. **Generate visuals** — 40 images per `episodes/NNN/image-prompts.md`.
2. **Record VO** — read `episodes/NNN/script.md` per `voice-notes.md` cues.
3. **Edit** — drop images + VO into CapCut, set durations, add Ken-Burns motion, captions, music.
4. **Master** — colour grade, audio mix, fade ends.
5. **Thumbnail** — pick A/B/C from `thumbnail-prompts.md`, finish in Canva.
6. **Upload** — title, description, tags, end-screen, schedule.
7. **Post-launch** — track CTR / retention / watch time over the first 48h.

---

## Path 1 — Image + CapCut (recommended for The Long Light)

The Long Light's visuals are pre-generated stills, not coded animations.
CapCut Free (cross-platform, GPL/free) handles the edit faster than
custom Python.

### 1.1 — Generate visuals

```bash
# Pick one generator. Stay with it for the whole episode.
# Recommended: Imagen 3 (best for archival/photographic).
# Alternatives: Flux Pro, Midjourney v6.
```

For each numbered prompt in `episodes/NNN/image-prompts.md`:

1. Paste the **style anchor** at the top of the session (or append to every prompt).
2. Paste the per-prompt sentence.
3. Generate 4 candidates. Pick the one that best matches the script beat AND keeps the *single warm light source* discipline.
4. Save as `episodes/NNN/visuals/{NN}-<slug>.png` at 4K (3840×2160). Upscale via Topaz Video AI / Real-ESRGAN if the generator caps out at 2K.

Time budget: ~2 hours for 40 prompts.

### 1.2 — Record VO

Read `script.md` per `voice-notes.md`. Three takes per scene, scene by scene. Save raw to `episodes/NNN/audio/raw-takes/`.

**Recording stack (free):**

| Tool | Use | License |
|---|---|---|
| Audacity | record + edit | GPL |
| **OR** Reaper free trial | record + edit + better effects | non-commercial free |
| Piper TTS via `pipeline/voiceover.py` | placeholder VO before you record real takes | MIT |
| eSpeak NG | last-resort placeholder when offline | GPL |

Edit your best take per scene into a single WAV (`episodes/NNN/audio/voiceover.wav`). Keep all breaths. Remove only saliva clicks. **Do not compress** — The Long Light's dynamic range *is* the show.

Time budget: ~1.5 hours for a 9-minute script (record + edit).

### 1.3 — Edit in CapCut

CapCut Free is the right tool. Steps:

1. **New project** → 16:9, 4K (or 1080p if your machine struggles), 30 fps.
2. **Import** all 40 visuals + voiceover.wav + (optional) background music.
3. **Layout the VO track first** — drag voiceover.wav to the audio track. This sets the timeline length.
4. **Drop visuals in script order.** Default duration: 13.5s each (`540s ÷ 40`).
   - For long static scenes (e.g. Memoir, Andreotti EU card analogues), allow up to 20s per image with stronger Ken-Burns motion.
   - For montage scenes (Scene 6 — Vladivostok, Donetsk, Tashkent, Tbilisi), shorten to 5–7s each.
5. **Add Ken-Burns motion to every image.** CapCut: select clip → Animation → Slow zoom in OR slow pan right. Vary the direction across consecutive clips so it doesn't feel mechanical.
6. **Captions.** CapCut → Text → Auto-captions. Set font to **Inter Bold**, size ~64, colour cream `#f5e8d3`, drop shadow at 0px (clean, no shadow). Position at vertical 80%.
   - Edit auto-captions for accuracy — Whisper / Auto-caption tools mishear proper nouns (Borispol, Lemnitzer, Andreotti).
7. **Background music.**
   - Free sources: YouTube Audio Library (filter: "Cinematic"), Pixabay Music (CC0), `freemusicarchive.org`, AShamaluevMusic (free for non-monetised; license per-use otherwise).
   - For The Long Light specifically: search "ambient orchestral", "minimalist piano", "drone". Avoid percussion-led tracks.
   - Drop music to **−18 dB to −22 dB** (about 8–12% of VO level). It must never compete with the voice.
   - Fade music IN at 0:18 (end of cold open). Fade OUT to silence by 7:30. Voice carries the end card alone.
8. **Transitions.** Default: hard cut. For the act breaks (between scenes 3→4 and 5→6), use a 0.6s **Fade to black** — this gives the audience a beat to process.
9. **Cold-open frame.** Scene 1 opens on 4 seconds of black. Add a black-frame image at position 0:00:00 with duration 4s, then fade-in (1s) to the first generated image.

Time budget: ~3 hours for a 9-minute video (first time; ~2h once you have a CapCut template saved).

### 1.4 — Master

1. **Colour grade.** All images are pre-graded by the generator with our brand palette. In CapCut: apply a *very* subtle warm grade across the whole timeline (Filters → Cinematic → reduce intensity to 30%) to lock everything to the same warmth.
2. **Audio mix.**
   - VO target: peak −6 dB, average −18 dB LUFS.
   - Music target: −20 dB LUFS, ducked under VO.
   - Add a **gentle de-esser** if your VO has sibilance.
   - Final: bus-compress at 2:1 ratio with −8 dB threshold, then limiter at −1 dB ceiling.
3. **Fade ends.** Last 2 seconds: video fades to black, audio fades to silence in parallel.
4. **Export.** MP4, H.264, **3840×2160** if your machine handles it; otherwise 1920×1080. Bitrate 25–40 Mbps for 4K, 12–18 Mbps for 1080p. AAC audio at 192 kbps.
5. Save final as `episodes/NNN/render/<slug>-final.mp4`.

Time budget: ~30 min mastering + 15–60 min export.

### 1.5 — Thumbnail

1. Pick one composition from `episodes/NNN/thumbnail-prompts.md`.
2. Generate 4 candidates of the chosen composition. Pick the cleanest.
3. Open in Canva. Add overlay text per the prompt's spec.
4. Add the channel mark `THE LONG LIGHT` in JetBrains Mono caps, lower-right, ~24px, MUTED grey (consistency anchor across the channel page).
5. Export as `1280x720` PNG.

Time budget: ~30 min.

### 1.6 — Upload

YouTube Studio:

- **Title:** pull from one of the title formulas in `branding-assets.md` § 5. For the pilot: *"The Last Pilot at Borispol"* or *"December 25, 1991: A Quiet Evening at Borispol"*.
- **Description:** structured as below.
- **Tags:** 10–15 relevant tags. For the Borispol pilot: `cold war, soviet union, dissolution, gorbachev, aeroflot, ukraine independence, december 1991, history, documentary, faceless, dark history, geopolitics, sealed records, the long light, narrative documentary`.
- **Thumbnail:** upload the Canva PNG.
- **End screen:** add subscribe + watch-next + the channel-mark frame.
- **Cards:** one card at 1:30 linking to `channel/about`, one at 5:00 linking to a related video (use The Dossier's Gladio episode for now since it's the only sibling content live).
- **Category:** Education.
- **Visibility:** Schedule. **First three episodes:** publish immediately (need data). **Episode 4 onward:** schedule for Tuesday 6:00 PM viewer time zone.

**Description template:**

```
Today on The Long Light: [one-sentence hook from script Scene 1].

[Three-sentence summary of the episode arc.]

— Sources —
[Numbered list of 5–10 sources from research.md, with URLs where the source is online.]

— Chapters —
00:00  Cold Open
00:18  The Day Before
01:30  The Speech
02:55  Borispol
04:30  The Question
06:00  The Long Light
07:30  …and that's where we leave it.

— Subscribe —
The Long Light publishes one new story every 10 days.
[Channel handle URL]

#documentary #ColdWar #SovietUnion #history #faceless
```

### 1.7 — Post-launch monitoring (first 48 hours)

- **At +6h:** check CTR. Below 4% = thumbnail isn't working; swap to alternate composition.
- **At +24h:** check 30-second retention. Below 60% = cold open isn't holding; flag for next-episode revision.
- **At +48h:** check overall watch-time / impressions ratio. Above industry average (~5–7% for a small channel) = the topic + craft are landing.
- Log all numbers in `the-long-light/post-launch-log.md` (create as needed).

---

## Path 2 — Manim path (when applicable)

The Dossier uses Manim because its visuals are coded animations — title cards, animated maps with pin reveals, year tickers, document overlays. The Long Light's visuals are pre-generated images, so Manim is mostly out of scope here.

Use the Manim path **only** for episodes where you need procedurally-animated content:

- A timeline that ticks year by year with synchronized labels.
- A chart or graph that builds itself.
- A document overlay where specific lines highlight in sync with VO.

For those cases:

```bash
./pipeline/render.sh the-long-light/episodes/NNN-slug/scene.py SceneName -ql   # preview
./pipeline/render.sh the-long-light/episodes/NNN-slug/scene.py SceneName       # 4K final
```

Then `pipeline/voiceover.py the-long-light/episodes/NNN-slug` to mux audio + SRT.

When mixing both paths inside one episode (some scenes are Manim, some are CapCut-edited stills), render the Manim scenes as MP4s, then **import them as clips** in the CapCut timeline alongside the still images. Match aspect (16:9) and frame rate (30 fps).

---

## File layout per episode (final state, after edit)

```
the-long-light/episodes/NNN-slug/
├── research.md
├── script.md
├── storyboard.md           (optional for image-driven episodes)
├── voice-notes.md
├── image-prompts.md
├── thumbnail-prompts.md
├── audio/
│   ├── raw-takes/          (gitignored)
│   └── voiceover.wav       (gitignored)
├── visuals/
│   └── {01..40}-slug.png   (gitignored)
├── render/
│   ├── thumbnail.png
│   └── <slug>-final.mp4    (gitignored — push 480p shareable to git only)
└── competitor-refs/        (gitignored)
```

The audio, visuals, and 4K final renders are all gitignored. Only the source-of-truth markdown files + the small thumbnail and any compressed shareable preview are tracked.

---

## Recurring weekly cadence (reminder from `niche.md`)

The Long Light publishes **every 10 days**. That cadence allows:

- 3 days: research + script + voice-notes + image-prompts + thumbnail-prompts (this is what Phases 1–5 deliver).
- 2 days: image generation (40 prompts × 4 candidates × ~30s each = ~80 min compute, plus selection).
- 2 days: VO record + edit.
- 2 days: CapCut edit + master.
- 1 day: thumbnail finalize + upload + buffer.

If any phase blocks, **publish on time anyway** with the best available state. Cadence > polish for the first 12 episodes.
