# Brand — The Dossier

## Identity
- **Channel name:** The Dossier
- **Tagline:** *Declassified history, dark-world economics, and geopolitical power plays — every claim sourced.*
- **Recurring framing device:** Each video opens "Today's dossier: …" and closes "Filed."
- **Logo concept:** A manila-folder corner with a red `CLASSIFIED` stamp turning into `DECLASSIFIED`.

## Voice (3 adjectives)
**Measured. Forensic. Cinematic.**

Sample paragraph (read aloud, 15s):
> *"In 1990, an Italian Prime Minister did something prime ministers don't do.  He stood up in parliament and admitted his government had been running a secret army for forty-five years. Not a metaphorical secret army. A real one — with weapons, codenames, and orders. They called it Gladio. Today's dossier is how it stayed hidden, what it actually did, and why almost no one in your country was ever told."*

Voice rules:
- Short sentences. Subject-verb-object. No throat-clearing.
- One adjective per sentence, max.
- Numbers stated, not adjectives. ("400,000 dead" not "many dead.")
- Never say "shocking", "insane", "wild", "you won't believe". Trust the facts.
- One contraction per minute, max — keeps the gravitas.

## Visual identity
Source of truth: `shared/styles.py`. Never hardcode colors elsewhere.

| Slot | Hex | Use |
|------|-----|-----|
| `BG` | `#0e0e10` | Background. Always. |
| `FG` | `#e8e8ea` | Body text, primary lines. |
| `MUTED` | `#6b6b76` | Secondary text, citations. |
| `ACCENT` | `#d63b2f` | Brand red. Damning facts, redaction bars, classified stamps. |
| `SUPPORTING` | `#e3a72f` | Archive amber. Claims, developing, "alleged". |
| `VERIFIED` | `#3aa7a0` | Teal-green. Cross-checked, primary-source-confirmed. |
| `REDACTED` | `#000000` | Pure black redaction overlay. |

**Color grammar (visual signal system):**
- Red = the verb the document used.
- Amber = the claim, not yet verified by us.
- Teal = we have the primary source, link in description.

## Typography
- **Title + body:** Inter (system fallback: Helvetica, Arial)
- **Mono / document overlays:** JetBrains Mono (fallback: IBM Plex Mono, Menlo)

## Lower-third format
`shared/styles.py:lower_third(label, source)` — accent bar + label + tiny muted citation.

## Stamps & redactions
- `shared/styles.py:classification_stamp("DECLASSIFIED")` — top-right tilted red stamp.
- `shared/styles.py:redaction_bar(width, height)` — solid black overlay for redacting names/lines.
- `shared/styles.py:source_caption("ICIJ FinCEN Files, 2020")` — bottom-right muted citation.

## Channel art TODO
- Banner: 2560×1440 manila folder, redaction-red CLASSIFIED stamp, channel name in mono.
- Avatar: 800×800 of the stamp alone.
- End-screen: dark folder closing.
