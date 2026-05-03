# Episode 001 — Thumbnail prompts (3 compositions)

> Three distinct compositions for A/B-testing CTR. All paste-ready for
> Imagen / Flux / Midjourney. Each uses **the same style anchor as
> `image-prompts.md`** (deep navy + warm gold + film grain + faceless).
> Overlay text added in Canva / GIMP after generation.

---

## Composition A — Object-anchor (the safe play)

**Hook:** The aircraft alone in the dark.
**Why it works:** Mirrors the cold open. Brand-consistent. Object thumbnails reliably outperform abstract ones in Harris-lane content. CTR baseline.

**Generation prompt:**

> A cinematic documentary thumbnail in 16:9 widescreen. A single Tupolev Tu-134 Soviet medium-range jet sits on a dark airport apron at night, side view, slightly low angle. The aircraft is rendered as a near-black silhouette against deep navy sky (`#0a0e1a`). A single horizontal beam of warm amber-gold light (`#ffb627`) crosses the lower third, catching only the leading edge of the wing and the runway lights. Visible film grain. Snow drifts faintly across the foreground. **Composition:** aircraft right-of-center; large negative space left for title text. **No people.** Style: archival cinematic, Christopher Nolan low-key palette. `--ar 16:9 --style raw --quality 2`.

**Overlay text (add in Canva, top-left of negative space):**

```
THE LAST PILOT
                                  (serif caps, warm cream #f5e8d3)

December 25, 1991. Borispol.
                                  (mono, muted #7a8294, smaller)
```

---

## Composition B — Time-anchor (the dramatic play)

**Hook:** A specific, untold moment in a known event.
**Why it works:** "December 25, 1991" is recognizable to anyone who knows the date the USSR ended. The contrast — *that specific moment, but at a runway* — creates curiosity. Stronger CTR potential, slightly riskier on click-through.

**Generation prompt:**

> A cinematic documentary thumbnail in 16:9. The frame is split visually but not literally: left two-thirds — the Soviet flag (red, hammer and sickle) descending halfway down a Kremlin Senate Tower flagpole at night, lit from below by warm gold floodlights against snow-flecked dark sky. Right one-third — empty deep navy sky for title overlay. The flag is in mid-descent — not yet down, not still flying. Slight film grain. **Composition:** flag occupies left + center; right negative space holds text. **No people.** Style: archival photojournalism, single-source warm key light. `--ar 16:9 --style raw --quality 2`.

**Overlay text (add in Canva, right negative space):**

```
DECEMBER 25, 1991.
                                  (mono caps, warm cream)

A QUIET EVENING
AT BORISPOL.
                                  (serif caps, signal yellow #ffb627)
```

---

## Composition C — Number-anchor (the curiosity-gap play)

**Hook:** A specific number in isolation.
**Why it works:** Numbers in thumbnails consistently lift CTR (Harris uses this — "0.1%", "33 km", "1.4 million km"). "17 minutes" begs the question *what 17 minutes?* Highest-variance bet — could outperform A and B by 30%, or underperform if the number reads as arbitrary.

**Generation prompt:**

> A cinematic documentary thumbnail in 16:9. Tight interior shot of a Tupolev Tu-134 cockpit at night. Both pilot seats empty, one foreground (in slight focus), one background (out of focus). Dim instrument lights — small green and amber dials glowing. Two unfilled coffee cups on the center console. A flight clipboard rests on the captain's seat. Warm amber-gold light enters through the cockpit windows from screen-right, catching the rim of the captain's chair. Visible film grain. **Composition:** cockpit fills the frame; the empty captain's seat is visually centered. **No people.** Style: archival, low-key, single-source warm key light. `--ar 16:9 --style raw --quality 2`.

**Overlay text (add in Canva, centered over the empty seat):**

```
17 MINUTES
                                  (serif caps, signal yellow, very large)

He waited longer than expected.
                                  (mono, warm cream, small, below)
```

---

## A/B/C testing protocol

1. Generate one variant per composition. Pick the best image of each.
2. Add the overlay text in Canva using the channel's serif (Source Serif Pro or Tiempos Headline) for headlines and JetBrains Mono for captions.
3. Export each at exactly `1280x720` PNG.
4. Upload all three to YouTube as separate thumbnails over the first 14 days post-publish, swapping every 4 days. Note CTR per variant in `the-long-light/thumbnail-test-log.md` (create as needed).
5. The winner becomes the template style for episode 2's thumbnail.

## Cross-thumbnail consistency rules

- **Aspect:** always 16:9 (1280x720 final).
- **Background:** always deep navy (`#0a0e1a`) where not occupied by subject.
- **Light source:** always *one* warm-gold edge light. Never symmetric lighting.
- **Faces:** never. The Long Light is faceless across the channel page too.
- **Channel mark:** small `THE LONG LIGHT` wordmark in mono caps, lower-right corner, in `MUTED` grey at ~24px. Same position every thumbnail. (This is the channel-page consistency anchor.)
- **No emoji.** No arrows. No reaction cues.
- **Negative prompt** (every generator): `--no faces, smiles, modern logos, neon, anime, cartoon, lens flare, sticker, emoji`.
