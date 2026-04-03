# Quick Start Checklist: Running Your First Stock Simulation

## Setup (One-Time)

- [ ] **Get Zep Cloud API key** (free)
  - Go to https://app.getzep.com/
  - Sign up / log in
  - Create a project
  - Copy your API key

- [ ] **Add Zep key to MiroFish config**
  ```bash
  cd /home/user/MiroFish
  nano .env
  # Replace "your_zep_api_key_here" with your actual Zep key
  ```

- [ ] **Verify MiroFish starts**
  ```bash
  cd /home/user/MiroFish
  npm run dev
  ```
  - Frontend should be at: http://localhost:3000
  - Backend should be at: http://localhost:5001

## Running Your First Stock Simulation (15 Minutes)

### Step 1: Gather Seed Data (5 min)
- [ ] Pick a stock you're interested in (e.g., NVDA, AAPL, TSLA)
- [ ] Copy 3-5 recent news articles about it
- [ ] Note the latest earnings/financial data

### Step 2: Choose a Template (1 min)
- [ ] Open `simulation-templates.md` in this folder
- [ ] Pick the most relevant template
- [ ] Fill in the [BRACKETS] with your specific data

### Step 3: Run the Simulation (5-10 min)
- [ ] Open MiroFish at http://localhost:3000
- [ ] Paste your seed data
- [ ] Paste your filled-in query
- [ ] Start with small settings first: 200 agents, 10 rounds
- [ ] Click Run and wait

### Step 4: Analyze Results (5 min)
- [ ] Read the automated report
- [ ] Check: What did institutional agents do vs retail agents?
- [ ] Check: Where did media narrative diverge from fundamentals?
- [ ] Check: What was the timeline of key events?
- [ ] Chat with 2-3 agents to understand their reasoning

### Step 5: Document & Compare (2 min)
- [ ] Screenshot the results
- [ ] Write down your key takeaway in 1-2 sentences
- [ ] Note what you'd change for next time
- [ ] Compare to actual market behavior over coming days

## Your First 5 Simulations (Do These in Order)

| # | Simulation | Purpose |
|---|---|---|
| 1 | Any stock + recent news (200 agents, 10 rounds) | Learn the tool, see how it works |
| 2 | Same stock, more agents (500 agents, 20 rounds) | See how scale changes results |
| 3 | A stock you actually own + upcoming earnings | Real personal value |
| 4 | A sector event (Fed rates, regulation, etc.) | Multi-stock analysis |
| 5 | Your full portfolio stress test | Practical portfolio insight |

## Estimated Costs

| Simulation | Agents | Rounds | Approx Cost |
|---|---|---|---|
| First test run | 200 | 10 | ~$0.15 |
| Standard run | 500 | 20 | ~$1.00 |
| Deep analysis | 1,000 | 30 | ~$2.50 |
| Full portfolio test | 2,000 | 40 | ~$6.00 |
| **Total for first 5 sims** | | | **~$10-15** |

## After Your First 5 Simulations

1. **Pick your niche**: Which type of simulation gave you the best insights?
2. **Start your track record**: Document predictions vs outcomes
3. **Create content**: Every simulation is a YouTube video, blog post, or paid report
4. **Build your newsletter**: Share weekly simulation results
5. **Scale up**: More agents, more scenarios, more revenue streams

## Troubleshooting

| Problem | Fix |
|---|---|
| "Cannot connect to backend" | Make sure `npm run dev` is running |
| "API key invalid" | Check .env file -- no extra spaces, correct key |
| "Zep connection error" | Verify Zep API key at app.getzep.com |
| Simulation times out | Reduce agents (try 100) and rounds (try 5) |
| Results seem random | Add better seed data -- more articles = better simulation |
| High API costs | Use fewer agents and rounds. Start with 200/10 |

## Next Steps After Mastering the Basics

- Read `stock-simulation-guide.md` for the full SPAR method
- Check `simulation-templates.md` for 6 ready-to-use frameworks
- Watch the YouTube scripts in `../youtube-scripts/` for video ideas
- Start your newsletter with your first simulation results
