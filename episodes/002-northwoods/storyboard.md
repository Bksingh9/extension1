# Episode 002 — Storyboard

> **Status:** Hook detailed. Scenes 2–10 one-line for now; fill in after
> Playwright captures the document PDF.

## First 60 seconds (detailed)

| # | Scene | Time | Visual | Animation | Audio cue |
|---|-------|------|--------|-----------|-----------|
| 1 | Hook | 0:00–0:08 | Title `OPERATION NORTHWOODS` + subtitle "The False Flag the Pentagon Wrote Down" + red `TOP SECRET — DECLASSIFIED 18·XI·1997` stamp tilted top-right. | Title fades in shifting down; stamp scales in tilted; subtle vignette. | "On the 13th of March, 1962…" |
| 2 | Mongoose | 0:08–0:30 | Centered name `OPERATION MONGOOSE` mono → portrait card "Brig. Gen. Edward Lansdale, USAF" → quote pull: "pretexts which would provide justification for U.S. military intervention in Cuba". | Type-on; quote reveals; source caption. | "It started with a different operation…" |
| 3 | Memo | 0:30–1:10 | Document overlay (rectangle styled as a typewritten page) with: `JUSTIFICATION FOR U.S. MILITARY INTERVENTION IN CUBA` + date `13 March 1962` + `Lyman L. Lemnitzer, Chairman, JCS` + classification stamp `TOP SECRET`. | Document slides in; lines underline as the VO names them. | "On the 13th of March, 1962…" |
| 4 | Pretexts | 1:10–2:30 | Five pretexts revealed sequentially with line numbers from the document. Each in red mono on its own row. Source caption: "src: NSArchive, Northwoods document, p. ___". | Each pretext fades in; brief pause; red highlight on document line. | "What was inside, point by point…" |
| 5 | NoEvent | 2:30–3:00 | Big mono `REJECTED` in red over a dimmed document. Below: "John F. Kennedy / The White House / 1962". | Stamp `REJECTED` slams in; document dims. | "The Joint Chiefs approved it…" |
| 6 | Lemnitzer | 3:00–3:45 | Date timeline: `13 · III · 1962` (memo) → `1962, late summer` (not reappointed) → `1 · I · 1963` (SACEUR appointment). No editorialising arrows. | Timeline draws; markers fade in by date. | "Three months later…" |
| 7 | Buried | 3:45–4:30 | Stack of folders animating taller and taller, then a calendar tearing 1962 → 1997. Then `1992 — JFK Assassination Records Act`, `1997 — ARRB release`, `30 April 2001 — NSArchive publication`. | Folders stack; calendar tears; date markers fade in. | "The document stayed classified for 35 years…" |
| 8 | McNamara | 4:30–5:00 | Two side-by-side quote cards. LEFT (red): "completely insane". RIGHT (amber): "absolutely zero recollection". Both attributed. Caption between: "Let the audience hold both." | Both cards slide in simultaneously. | "Robert McNamara, asked about it later…" |
| 9 | Misuse | 5:00–5:40 | Two columns. LEFT (red): "what Northwoods proves". RIGHT (amber): "what Northwoods does not prove" — list of contested invocations. | Columns reveal item by item. | "Northwoods is sometimes invoked…" |
| 10 | Filed | 5:40–6:00 | Manila folder closes. Stamp swap from `DECLASSIFIED` to `FILED`. Tease: "Next dossier: MKULTRA". | Folder slides up; stamp morphs; tease types on. | "Next dossier: MKUltra…" |

## Visual rules (this episode)
- The document overlay is the visual signature. Use it in scenes 3, 4, 5, 7.
- Reuse the `classification_stamp` helper with text variants: `TOP SECRET`, `DECLASSIFIED`, `REJECTED`, `FILED`.
- Every pretext on screen must have a document line/paragraph reference once the Playwright pass extracts the page numbers from the PDF.
