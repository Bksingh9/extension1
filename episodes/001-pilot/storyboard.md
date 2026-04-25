# Pilot — Storyboard

> All ten scenes detailed. Time targets are nominal — render passes
> tune them. Visual signal grammar (red/amber/teal) per `channel/brand.md`.

| # | Scene | Time | Visual | Text on screen | Animation | Audio cue |
|---|-------|------|--------|----------------|-----------|-----------|
| 1 | Hook | 0:00–0:08 | Black → title `OPERATION GLADIO` + subtitle in mono → red `DECLASSIFIED 24·X·1990` stamp tilted top-right. | Title + subtitle | Title fades in shifting down; stamp scales in tilted, fade. | "On the 24th of October, 1990…" |
| 2 | Doctrine | 0:08–0:25 | Centered `STAY-BEHIND` in mono bold → 3 attribute lines fade in below: *cells with weapons / codenames / orders*. Lower-third red bar: "NATO doctrine, 1947". | Headline + 3 lines | Write headline, fade in attributes one at a time at 0.4s intervals. Hold to scene end. | "The story does not start in Italy…" |
| 3 | Network | 0:25–0:45 | Pins drop on stylised Western Europe positions. Italy: large red, with caption "622 members · 127 arms caches". 13 confirmed pins fade in white in batches of 3. Sweden + Finland appear last in teal. Source caption bottom-right. | Country names beside each pin | Italy first with thud, others in batches, Sweden + Finland last. | "In Italy alone, when the network was finally disclosed…" |
| 4 | Pivot | 0:45–1:00 | Big red `1947 — 1990` typed in. Two body lines below — first FG, second amber: *"What they actually did is the rest of this dossier."* | Date range + 2 lines | Dates type-on; first line fade; second line fade after pause. | "Officially, they were there to fight Soviets…" |
| 5 | Memoir | 1:00–1:45 | Mock book cover left ("HONORABLE MEN / WILLIAM E. COLBY / 1978") with dotted border. Right side: pull-quote in mono with citation caption "src: Colby, *Honorable Men*, 1978". | Book + quote pull | Book draws in; quote types on after; citation fades in. | "It began with a CIA officer named William Colby…" |
| 6 | Andreotti | 1:45–2:45 | Date `24 · X · 1990` red mono → quote pull (paraphrased): *"a structure of information, response and safeguard"* in italics → reveal "**622** members · **127** arms caches" with each number animating up via ValueTracker → dissolve to `22 · XI · 1990` + `EU Parliament Resolution OJ C 324/201`. | Quote + numbers + EU citation | Quote types on; numbers tick up; transition card to EU date. | "Forty-five years went by before any government talked about it…" |
| 7 | Bologna | 2:45–3:45 | Date `2 · VIII · 1980` + time `10:25 a.m.` → death counter ticks 0 → 85 in red. Then split-column: LEFT (red) "CONVICTED — Italian Supreme Court" listing Fioravanti, Mambro, Ciavardini, Cavallini, Bellini. RIGHT (red) "2021 — Court of Appeal: 'una strage di Stato'" listing Gelli (P2), D'Amato (Stay-Behind/Gladio links), Ortolani, Tedeschi. Source caption: "src: ANSA, 8 Jan 2021". | Date + counter + 2-column lists | Counter tick; columns slide in left-then-right. | "On the second of August, 1980…" |
| 8 | Belgium | 3:45–4:45 | Codename `SDRA-VIII` mono large → expansion below in muted: "Service de Documentation, de Renseignements et d'Action VIII" → date `7 · XI · 1990` red → Brabant timeline: years 1982–1985 stretched horizontally, dot markers along it, death count `28` in red appears at end. AMBER caption: "Belgian parliamentary inquiry: no substantive evidence linking SDRA-VIII to the killings." | Codename + timeline + caption | Codename writes, expansion types under, timeline draws, amber caption fades last. | "And not only Italy. Belgium had its own network…" |
| 9 | Disclosed | 4:45–5:30 | Year ticker top-center: 1990 → 2014, animating up via ValueTracker. As year passes thresholds, country labels light up below: 1990 (Italy, Belgium, Switzerland), 1991 (France, Denmark, Greece), 1996 (Norway), 2000 (Pellegrino Report — quote pull), 2014 (Sweden — Sveaborg). Source caption mid-scene: "src: Commissione Stragi, *Relazione finale*, 2000". | Year ticker + country list | Year ticker scrubs forward; countries fade in at thresholds; quote pull mid-scene. | "Country by country, the disclosures came…" |
| 10 | Filed | 5:30–6:00 | All previous content fades. Manila-folder rectangle slides up from bottom covering frame. Stamp text changes from `DECLASSIFIED` to `FILED`. Below in mono muted: "Next dossier: OPERATION NORTHWOODS · *the false flag the Pentagon wrote down*". | Folder close + stamp swap + tease | Folder slides; stamp morphs colour; tease types on. | "What we still do not know…" |

## Visual rules (this episode)
- Every dated claim shown on screen is also in `research.md` with a verified source.
- Court findings / convictions / declassified facts: **red** (`ACCENT`).
- Inquiry allegations / unresolved / open cases: **amber** (`SUPPORTING`).
- Cross-checked against primary source: **teal** (`VERIFIED`).
- Source caption visible bottom-right whenever a hard number or name is on screen.
- No LaTeX rendering. Use only `Text` (we are not on a TeX-installed host).
