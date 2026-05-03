# The Long Light — Channel branding assets

> Phase 6 deliverables. Generation prompts for the three permanent
> channel-page assets, plus the locked-in channel descriptions copied
> from `brand.md` for one-stop YouTube setup.

---

## 1. Profile picture (avatar) — 800×800

**Spec:** square, 800×800px (YouTube renders at 98×98 in headers, so it must read at 32×32 thumb size). High contrast, no text.

**Generation prompt:**

> A square 800×800 minimal cinematic icon. The frame is deep navy-black (`#0a0e1a`). A single horizontal beam of warm amber-gold light (`#ffb627`) crosses the lower third of the frame, fading from full saturation on the right to nothing on the left. Subtle film grain throughout. Faint vignette at the corners. Composition is clean and centered. **No text. No symbols. No people.** Just the light beam and the dark. Style: cinematic, archival, single-source warm key light. `--ar 1:1 --style raw --quality 2`.

**Negative prompt:** `--no text, faces, logos, ornaments, gradients-other-than-light, color-noise`

**Post-process in GIMP / Canva:**
1. Export at 800×800 PNG.
2. Sanity-check: shrink preview to 32×32 and 98×98 — the warm-light beam should still read clearly.
3. If it doesn't, regenerate with `light beam thicker` added.

---

## 2. YouTube banner (channel art) — 2560×1440

**Spec:** 2560×1440 PNG. The "safe zone" — the 1546×423 area that displays on all devices including phones — is centered. Channel name and tagline must sit inside it. Anything outside the safe zone displays only on TVs and big screens.

**Generation prompt:**

> A wide cinematic banner in 2560×1440 format. The full frame is deep navy-black (`#0a0e1a`) with a subtle vignette toward the corners. A long horizontal beam of warm amber-gold light (`#ffb627`) sweeps across the entire width of the frame at vertical mid-height, brightest at screen-right and fading toward screen-left. Above and below the light beam: pure dark navy with faint film grain and vintage paper texture. **Composition:** the warm light beam is the only visual element — no aircraft, no people, no objects. Pure mood frame, ready for centered text overlay. `--ar 16:9 --style raw --quality 2`.

**Post-process in Canva — text overlay (placed inside the safe zone, vertical center):**

```
                    THE LONG LIGHT
                    (Source Serif Pro caps, ~120px, warm cream #f5e8d3)

                    stories told slowly
                    (Inter italic, ~36px, muted #7a8294)
```

The text sits above the warm light beam. The beam itself acts as a horizontal divider beneath the wordmark.

**Sanity-check:** preview at 1546×423 (the mobile-safe area). The wordmark should be fully readable. If cut off, scale text down by 10% and re-export.

---

## 3. End-screen template — 1920×1080

**Spec:** 20-second template added at the end of every episode. Two slots — one for "Subscribe", one for "Watch next" — and the closing line.

**Generation prompt (for the static background frame):**

> A cinematic 1920×1080 end-screen frame. Pure deep navy-black background (`#0a0e1a`). Subtle film grain. A single very dim horizontal warm gold light beam (`#ffb627`) across the lower third — visible but understated, about 30% the intensity of the main banner. **No subjects. No text. Empty composition** ready for end-screen elements to be placed by YouTube Studio. `--ar 16:9 --style raw --quality 2`.

**Composition (assembled in YouTube Studio after upload):**

- **Top-center text** (added in Canva on top of the background, then exported as PNG used as end-screen image):
  ```
  …and that's where we leave it. For now.
  (Source Serif Pro italic, ~64px, warm cream)
  ```
- **Lower-left:** YouTube Subscribe element (channel logo + "Subscribe" button).
- **Lower-right:** YouTube Watch-next element (next video thumbnail card).
- **Bottom-center under the light beam:**
  ```
  THE LONG LIGHT  ·  STORIES TOLD SLOWLY  ·  NEW EVERY 10 DAYS
  (JetBrains Mono caps, ~22px, muted #7a8294)
  ```

---

## 4. Channel descriptions (locked, copy-paste ready)

### Long version (≤ 1,000 chars — for the YouTube About box)

> A patient, cinematic documentary channel about small moments inside the world's biggest secrets.
>
> Each episode walks slowly through one true story from the dark world — a defector, a decommissioned facility, a sealed file, a lost recording — built around place, time, and the people who were in the room. Every fact is sourced; sources are in the description.
>
> No on-camera presenter. No sponsorship reads. No filler. New episode every 10 days.

**Char count:** ~470. Well under 1,000.

### Short version (≤ 200 chars — for the channel handle blurb)

> One true story per episode. People, places, files. Sources in the description. New every 10 days.

**Char count:** ~99. Under 200.

### One-liner (≤ 80 chars — for cross-posts and tags)

> *Stories told slowly.*

**Char count:** 22.

---

## 5. Title formulas (use for every episode title)

Pull from this list when titling new episodes; alternate to keep the channel-page mosaic varied.

- **Person-anchored:** *"The [role] Who [verb]"* — e.g. "The Pilot Who Waited", "The Codebreaker Who Lived on a Boat".
- **Place-anchored:** *"The [thing] at [place]"* — e.g. "The Last Pilot at Borispol", "The Light at Vela".
- **Object-anchored:** *"The [object] that [verb]"* — e.g. "The Submarine That Refused to Sink", "The Camera That Ended a War".
- **Time-anchored:** *"[Date]: A [adjective] Evening at [place]"* — e.g. "December 25, 1991: A Quiet Evening at Borispol".
- **Number-anchored** (use sparingly): *"[N] Minutes at [place]"* — e.g. "17 Minutes at Borispol".

**Avoid:** clickbait punctuation (??? !!! ☠️), all-caps in the actual title, any pronoun-led phrasing ("How I…", "Why You…").

---

## 6. Watermark / outro logo lockup

For episode-end cards, lower thirds, and any cross-posted clips:

```
THE LONG LIGHT
   stories told slowly
```

- Wordmark: Source Serif Pro caps, letter-spaced ~50.
- Tagline below in Inter italic, half the wordmark height, in `MUTED` grey.
- Always sits left-aligned in the lower-left, never centered, never with a drop shadow.

## 7. Channel art TODO checklist

Generation order, since each step depends on the previous:

- [ ] Run prompt #1 → save as `the-long-light/assets/avatar-800.png`
- [ ] Run prompt #2 → save background as `the-long-light/assets/banner-bg-2560.png`
- [ ] In Canva: overlay banner text → export as `the-long-light/assets/banner-final-2560.png`
- [ ] Run prompt #3 → save background as `the-long-light/assets/endscreen-bg-1920.png`
- [ ] In Canva: overlay end-screen text → export as `the-long-light/assets/endscreen-final-1920.png`
- [ ] Upload all four to YouTube Studio: avatar, banner, end-screen template (re-used per episode).
- [ ] Update YouTube About-box description to long version above.
- [ ] Set the channel handle blurb to short version above.
