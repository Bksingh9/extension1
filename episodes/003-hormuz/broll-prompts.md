# Episode 003 — B-roll prompt sheet (LTX-Video)

> Generated for `pipeline/broll.py`. Edit prompts to taste; the
> header line is the contract — `## <SceneName> · <seconds>s · <W>x<H>`.
> SceneName must match the Manim Scene class in `scene.py` so the
> clip composites in cleanly as a background layer.
>
> All prompts are tuned for The Dossier's voice: cinematic, measured,
> document-aware. No people on camera. No on-screen text in the
> generated clip — text is added in Manim on top. Aspect 16:9.
> Default resolution 1280x720 keeps VRAM bounded on a 24 GB GPU and
> upscales cleanly to the 4K Manim render.

---

## Hook · 5s · 1280x720

A slow, cinematic top-down satellite shot of the Strait of Hormuz
at dawn. Glassy water in deep blue-grey, the Iranian coast on the
upper half of the frame in muted ochre, the Omani coast on the
lower half. A single tanker silhouette in the very center, almost
imperceptibly drifting from left to right. Subtle film grain.
Volumetric haze. No text. No people. No camera shake. Static,
ambient, slow. Color palette: charcoal `#0e0e10`, ochre, pale blue.

---

## Chokepoint · 4s · 1280x720

Aerial wide shot of the Strait of Hormuz from 30,000 feet. Iran
on top of the frame, the Musandam Peninsula on the bottom. The
narrow blue channel between them runs east-west. Three tanker
silhouettes follow each other through the channel at long
intervals, moving slowly right to left. Late afternoon light, low
sun casting long shadows on the water. Subtle parallax drift on
the cloud layer. Cinematic. Document-aware. No text. No people.

---

## Cables · 5s · 1280x720

Underwater shot, sea floor at moderate depth. Three parallel
subsea fiber-optic cables run across the frame from left to right,
lying on a dim, silt-covered seabed. Faint particulate matter
drifts through the water column. Cold blue-green color grade.
Slow forward camera drift over the cables. No fish, no light
shafts, no surface visible. Industrial, quiet, ominous. No text.

---

## Closure · 6s · 1280x720

Night-time aerial of an empty oil terminal at the head of the
Persian Gulf. A row of dormant supertankers moored along a long
pier, deck lights amber against deep navy water. No movement on
the pier. Long lens compression. Drone slowly pulling backward and
upward, revealing more empty berths. Cold cinematic palette. No
text. No people on deck. Quiet, suspended, post-event.

---

## Pipelines · 4s · 1280x720

Aerial shot of a desert oil pipeline running through pale Saudi
Arabian dune fields, late afternoon. The pipeline is a long thin
silver line cutting diagonally across the frame from lower-left
to upper-right, partially buried, occasional pump-station nodes.
Sparse, geometric, no vehicles, no people. Static camera, very
slow zoom in. Hot ochre and bone-white palette.

---

## Successor · 5s · 1280x720

Wide, slow aerial of an empty assembly hall in Tehran at night,
ornate ceiling, rows of empty wooden seats lit from above by a
single overhead light. Camera dollies in extremely slowly toward
the central podium. The podium is empty. No people, no banners,
no text. Cinematic, patient, civic. Cold tungsten lighting.

---

## Filed · 5s · 1280x720

Macro shot of a single manila document folder closing slowly on a
dark wooden desk. The folder corner has a single red rubber stamp
mark partially visible — only the bottom edge of the stamp is in
frame, deliberately unreadable. Shallow depth of field, ambient
desk-lamp light from camera-left. Camera locked off, no movement
except the folder closing. No text, no hands, no people.

---

## Notes for the operator

- **Quality preset:** start with `configs/ltxv-13b-0.9.8-distilled.yaml`
  for a 24 GB VRAM budget. Switch to `ltxv-13b-0.9.8-dev.yaml` for
  the highest quality on 48 GB+ GPUs.
- **Per-clip cost (estimated):** ~$0.50–$1.50 each on rented H100,
  total budget under $10 for the seven clips above.
- **Mapping into scene.py:** for each clip, the corresponding Manim
  Scene class becomes a layered composite — the AI clip plays as a
  background `VideoMobject` at 30 % opacity, and the typography,
  citations, and source captions sit on top in full opacity. This
  preserves The Dossier's document-first identity while gaining the
  cinematic quality of AI B-roll.
- **Re-roll:** if a generated clip is wrong, delete it from
  `episodes/003-hormuz/broll/` and re-run; the pipeline skips
  existing files.
