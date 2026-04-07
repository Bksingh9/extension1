# YouTube Content Schedule — AI Render Lab (Geopolitics)

## Channel Strategy
- **Niche**: Animated geopolitics conspiracy/explainer (sarcastic, data-driven)
- **Tone**: Sharp sarcasm + real facts. "The Daily Show meets a Wikipedia rabbit hole."
- **Format**: Animated data visualizations + cartoon characters + AI B-roll
- **Upload cadence**: 3x/week (Mon full video, Wed + Fri Shorts)
- **Target**: 1M views in 90 days via Shorts algorithm

---

## 4-Week Launch Calendar

### Week 1: THE DOLLAR
| Day | Title | Format | Duration | Source |
|-----|-------|--------|----------|--------|
| Mon | "Who Actually Runs This Planet?" | Full 16:9 | 3:25 | Full GeoPoliticsDoc |
| Wed | "The Dollar is Backed by Vibes" | Short 9:16 | 55s | Ch1 Bretton Woods |
| Fri | "Every Country That Ditched the Dollar Got Invaded" | Short 9:16 | 58s | Ch1 Rebels |

### Week 2: THE CHIP WAR
| Day | Title | Format | Duration | Source |
|-----|-------|--------|----------|--------|
| Mon | "The $52.7B Chip War Nobody Talks About" | Full 16:9 | 2:00 | Ch2 Full |
| Wed | "One Island Makes 90% of All Chips" | Short 9:16 | 45s | Ch2 Taiwan |
| Fri | "They Said It Was Impossible. Huawei Did It Anyway." | Short 9:16 | 50s | Ch2 Huawei |

### Week 3: ENERGY & ALLIANCES
| Day | Title | Format | Duration | Source |
|-----|-------|--------|----------|--------|
| Mon | "Who Blew Up Nord Stream? Nobody's Talking." | Full 16:9 | 2:00 | Ch3 Full |
| Wed | "Sanctions Created the World's Biggest Bromance" | Short 9:16 | 50s | Ch3 Pivot |
| Fri | "BRICS: The Anti-Dollar Group Chat" | Full 16:9 | 1:40 | Ch4 Full |

### Week 4: SURVEILLANCE & WAR
| Day | Title | Format | Duration | Source |
|-----|-------|--------|----------|--------|
| Mon | "Your Phone Knows More Than Your Therapist" | Full 16:9 | 2:00 | Ch6 Full |
| Wed | "The $886B War Machine" | Short 9:16 | 55s | Ch7 Spending |
| Fri | "FULL DOCUMENTARY — Remastered" | Full 16:9 | 3:25 | Remastered Doc |

---

## SEO Strategy

### Primary Keywords (put in title):
```
geopolitics explained, conspiracy facts, petrodollar system,
chip war, BRICS 2024, who runs the world, dollar collapse
```

### Secondary Keywords (description + tags):
```
de-dollarization, nord stream sabotage, military industrial complex,
surveillance state, OPEC oil manipulation, huawei chip war,
animated explainer, AI documentary, data visualization
```

### Hashtags (every video):
```
#geopolitics #conspiracy #documentary #AI #shorts
```

---

## YouTube Description Template

```
🔴 [VIDEO TITLE] — The facts they don't want you to know.

Every claim is sourced. Every number is real.
This is not conspiracy — it's public record.

📊 Sources: Brown University, IMF, World Bank, SIPRI, BIS, OECD
🎬 Made with: Remotion + Open-Source AI (Wan 2.2 / Piper TTS)
💻 Code: github.com/bksingh9/extension1

⏱️ Chapters:
0:00 — Hook
0:05 — The Facts
0:45 — Why It Matters
1:00 — The Pattern

👁️ More uncomfortable truths every Monday, Wednesday, Friday.

🔔 Subscribe → AI Render Lab
🔗 Full documentary: [LINK]

#geopolitics #conspiracy #documentary #AI

⚠️ For entertainment & educational purposes.
All facts are publicly available and independently verifiable.
Always do your own research.
```

---

## Thumbnail Strategy

### Text Rules:
- MAX 4 words on thumbnail
- Font: Bold sans-serif, white with black outline
- Add red/yellow accent for urgency

### Proven Formulas:
- "THEY LIED" + shocked face
- "$X TRILLION" + red arrow
- "Who REALLY..." + question mark
- Country flag + "vs" + country flag
- "EXPOSED" + redacted document look

### Color Palette:
- Background: Dark blue/black
- Accent: Red (#ef4444) or Gold (#eab308)
- Text: White with 3px black stroke

---

## Monetization Path

### Phase 1 (Months 1-3): Growth
- 3 uploads/week (free content)
- Focus on Shorts algorithm for subscriber growth
- Target: 1,000 subscribers + 4,000 watch hours

### Phase 2 (Months 3-6): Monetization
- YouTube Partner Program (ad revenue)
- Patreon/Ko-fi for early access
- Affiliate links (VPN sponsors love conspiracy channels)

### Phase 3 (Months 6-12): Scale
- Sponsor integrations ($500-2000/video at 50K+ subs)
- Merchandise (sarcastic geopolitics merch)
- Premium deep-dive episodes (members-only)
- Template marketplace (sell Remotion components)

### Revenue Projections (conservative):
| Milestone | Monthly Revenue |
|-----------|----------------|
| 10K subs | $200-500 (ads) |
| 50K subs | $1,500-3,000 (ads + sponsors) |
| 100K subs | $5,000-10,000 (ads + sponsors + merch) |
| 500K subs | $20,000-50,000 (full monetization) |

---

## Open-Source AI Pipeline

### Video Generation (GPU required):
```bash
# Generate cinematic B-roll per chapter
python scripts/ai-video-gen.py --chapter all --model wan2.2

# Available models:
#   wan2.2    — 8GB VRAM minimum (consumer GPU)
#   ltx2      — 10GB+ VRAM, 4K output with audio
#   open-sora — 12GB+, most flexible
#   hunyuan   — 14GB+, highest visual quality
#   mochi     — 22GB+, best motion
```

### Narration (CPU or GPU):
```bash
# Install Piper TTS (runs locally, no API key)
pip install piper-tts

# Generate voiceover
bash scripts/generate-narration.sh
```

### Upload Automation:
```bash
# Upload to YouTube via Data API
node scripts/youtube-upload.mjs --schedule "Mon 9:00 AM EST"
```

### Full Pipeline (one command):
```bash
# 1. Generate AI B-roll clips
python scripts/ai-video-gen.py --chapter all --model auto

# 2. Generate narration
bash scripts/generate-narration.sh

# 3. Render all compositions
npx remotion render src/index.ts GeoPoliticsDoc out/documentary.mp4

# 4. Render all Shorts
for i in Petrodollar ChipWar NordStream BRICS Oil Surveillance WarMachine; do
  npx remotion render src/index.ts Short_$i out/short-$(echo $i | tr '[:upper:]' '[:lower:]').mp4
done

# 5. Upload to YouTube
node scripts/youtube-upload.mjs --all
```
