# Veo 3 runbook — Hormuz B-roll

> Adapted from Farhan Rakhangi's guide *"How to Access and Use Veo 3
> AI Video Generation for Free via Google Vids"*. **Free tier: 10 AI
> clips / month.** The seven Hormuz cutaways below fit inside that
> quota with three clips to spare. Each prompt is tuned to The
> Dossier's voice — measured, document-aware, no on-screen text, no
> people on camera. Aspect 16:9.

## Where to run this

This runbook is for **your own browser**, not the dev sandbox.
`vids.google.com`, `workspace.google.com`, `gemini.google.com`,
and `labs.google` are all firewalled off here, so Playwright
cannot drive them from inside the repo. Open Google Vids in your
regular signed-in browser session.

## One-time setup

1. Sign in to Google Workspace with the account that has Vids
   access (a free personal Google account works).
2. Click the apps grid → **Vids**. If it isn't there, go to
   `https://vids.google.com/` directly.
3. Open a new blank Vid. Click the **VO** (video output) tool in
   the right-hand toolbar — that's the Veo 3 panel.

## Per-clip workflow (for each of the 7 prompts below)

1. **Generation type:** *Create a clip from scratch*.
2. Paste the entire prompt block.
3. Click **Generate**. Wait ~30–90 seconds.
4. When satisfied, click **Insert** to add to timeline.
5. **File → Download → MP4 video** to grab just that clip.
6. Rename to `<SceneName>.mp4` and drop in:
   `episodes/003-hormuz/broll/`.
7. If the output is wrong, click *regenerate* — costs another
   monthly credit. Budget for 1 re-roll per clip; you've still got
   margin in the 10-credit quota.

## Scenes longer than 8s — the bypass

Veo 3's free tier caps each clip at 8 seconds. Two scenes in this
episode exceed that:

- **Closure** (target 6s — fits)
- **Successor** (target 5s — fits)
- **Filed** (target 5s — fits)
- *Long cuts* if you re-plan a 10–15s scene later: use the
  Rakhangi bypass — take a screenshot of the last frame, crop, run
  again in *Animate an image* mode with a prompt that picks up the
  story, and stitch.

For this episode, every clip is ≤6s and fits in one generation.

## "Ingredients" — when to use it

If you want a specific object in-frame (e.g. a specific manila
folder design for the **Filed** scene), upload an image of it via
the **Ingredients** button before clicking Generate. Up to 3
images per generation. Useful for brand consistency if you ever
want, say, a recurring document prop across episodes.

For Hormuz: not needed. Skip.

---

## The 7 prompts (paste each into the VO field)

### 1 · Hook · 5s

> Slow cinematic top-down satellite shot of the Strait of Hormuz at
> dawn. Glassy water, deep blue-grey. Iranian coast on the upper
> half in muted ochre tones, Omani coast on the lower half. A
> single tanker silhouette in the very center of the frame,
> imperceptibly drifting from left to right. Subtle volumetric
> haze. Film grain. Locked-off static camera, no shake. No text, no
> people, no on-screen graphics. Cold, ambient, measured. Color
> palette: charcoal, ochre, pale blue. Documentary style, Roger
> Deakins lighting.

### 2 · Chokepoint · 4s

> Aerial wide shot of the Strait of Hormuz from 30,000 feet,
> looking straight down. Iran on the top edge of frame, the
> Musandam Peninsula on the bottom. Narrow blue channel between
> them runs left to right. Three tanker silhouettes, well-spaced,
> moving slowly right to left. Late afternoon light, low sun, long
> shadows on the water. Subtle parallax drift on the cloud layer
> above. Cinematic anamorphic look. Documentary, observational. No
> text, no people, no logos. Slight grain.

### 3 · Cables · 5s

> Underwater shot, sea floor at moderate depth. Three parallel
> subsea fiber-optic cables run across the frame from left to right,
> resting on a dim, silt-covered seabed. Faint particulate matter
> drifts through the water column. Cold blue-green color grade,
> like the ROV footage from a cable maintenance operation. Slow
> forward camera drift over the cables, gentle parallax. No fish,
> no light shafts breaking through, no surface visible. Industrial,
> quiet, ominous. No text.

### 4 · Closure · 6s

> Night-time aerial of an empty oil terminal at the head of the
> Persian Gulf. A row of dormant supertankers moored along a long
> concrete pier, deck lights glowing amber against deep navy water.
> Nothing moving on the pier. Long-lens compression flattens the
> ships against the dark. Drone slowly pulling backward and upward,
> revealing more empty berths in the distance. Cold cinematic
> palette, halation around the deck lights. Quiet, suspended,
> post-event. No text. No people on deck. Cinéma vérité tone.

### 5 · Pipelines · 4s

> Aerial shot of a desert oil pipeline crossing pale Saudi Arabian
> dune fields in late afternoon. The pipeline is a long thin silver
> line cutting diagonally across the frame from lower-left to
> upper-right, partially buried, occasional pump-station nodes
> bumping above the sand. Sparse, geometric, no vehicles, no
> people, no buildings except the pipeline itself. Locked-off
> camera, very slow zoom-in. Hot ochre and bone-white palette,
> deep blue sky above.

### 6 · Successor · 5s

> Wide, slow aerial dolly inside an empty, ornate assembly hall in
> Tehran at night. Rows of empty wooden seats lit from above by a
> single overhead chandelier-style light. Camera moves extremely
> slowly forward toward the central podium. The podium is empty,
> no flags, no banners, no microphone, no text. Cold tungsten
> light spill, mahogany interior tones. Cinematic, patient,
> civic, post-event. No people, no decorations.

### 7 · Filed · 5s

> Macro shot of a single manila document folder closing slowly on
> a dark wooden desk. Only the closing motion is visible — the
> spine of the folder dominates the lower third of frame. A red
> rubber stamp mark is partially visible on the front, but only
> the bottom edge of the stamp is in shot, deliberately
> unreadable. Shallow depth of field, ambient warm desk-lamp light
> from camera-left, the rest of the room in shadow. Camera locked
> off — nothing moves except the folder. No hands, no people, no
> readable text. Cinematic, intimate, quiet finality.

---

## Drop-in convention

Save the 7 outputs (renamed) to:

```
episodes/003-hormuz/broll/
├── Hook.mp4
├── Chokepoint.mp4
├── Cables.mp4
├── Closure.mp4
├── Pipelines.mp4
├── Successor.mp4
└── Filed.mp4
```

Once they're there, the next pipeline step (composite into Manim
via `VideoMobject`) is a single edit to `scene.py` per scene.
Tell me when the MP4s are in the folder; I'll wire the composites
and re-render at 1080p60.

## Monthly credit budget

| Plan | Free / mo | Hormuz needs | Margin |
|---|---|---|---|
| Free | 10 | 7 + 1–2 re-rolls | OK |
| Pro | 50 | 7 + many re-rolls | comfortable |

If you blow the free quota mid-episode, the LTX-Video path in
`tools/video-gen.md` is the fallback — same prompts work, just
slower and lower fidelity.

## Source attribution

This workflow was adapted from:
*Farhan Rakhangi — "How to Access and Use Veo 3 AI Video Generation
for Free via Google Vids"* (PDF, provided by the project owner).
The prompts above are written by the project; only the access
procedure (Vids → VO tool → 8s bypass → Ingredients) is taken
from Rakhangi's guide.
