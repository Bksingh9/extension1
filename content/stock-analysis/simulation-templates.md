# Stock Simulation Templates

Ready-to-paste simulation prompts for MiroFish. Copy, modify the [BRACKETS], and run.

---

## Template 1: Earnings Reaction

```
SEED DATA NEEDED: 3 recent articles about the company + last earnings report summary

QUERY:
Simulate the market reaction when [COMPANY NAME] reports [Q1/Q2/Q3/Q4] earnings
that [BEAT/MISS] analyst expectations by [X]%. Revenue came in at $[X] billion
versus $[X] billion expected. The company also announced [SECONDARY NEWS -- e.g.,
"a 10% workforce reduction" or "a new AI product line" or "raised full-year guidance"].

Create 1,000 agents:
- 400 retail investors (mix of long-term holders, swing traders, and new buyers)
  - 150 conservative (hold through volatility)
  - 150 moderate (react to sentiment)
  - 100 aggressive (trade momentum)
- 250 institutional investors
  - 100 long-only funds (evaluate fundamentals)
  - 100 hedge funds (look for alpha and mispricing)
  - 50 index funds (rebalance mechanically)
- 150 day traders (trade on volume and momentum, use options)
- 100 financial media agents (TV anchors, bloggers, Twitter finance)
- 50 sell-side analysts (publish ratings: buy, hold, sell)
- 50 company employees (insider perspective on company health)

Simulate 30 trading days. Track:
- Stock price sentiment (bullish/bearish ratio per round)
- Volume of buying vs selling by agent type
- Media narrative shifts
- Analyst rating changes
- Key turning points
```

---

## Template 2: Sector Event Impact

```
SEED DATA NEEDED: 5 articles about the event + sector overview data

QUERY:
Simulate the impact of [DESCRIBE EVENT -- e.g., "new US tariffs of 25% on all
semiconductor imports from China"] on the [SECTOR] sector over 60 days.

Create 2,000 agents:
- 500 investors holding [SECTOR] stocks
  - 200 retail (emotional, news-driven)
  - 200 institutional (data-driven, rebalancing)
  - 100 sector-specialist funds
- 400 investors in competing/adjacent sectors
- 300 consumer agents (represent real economy demand)
- 300 company agents (20 companies in the sector, 15 agents each)
  - Each company agent has: revenue exposure to [EVENT], supply chain dependency,
    pricing power, cash reserves
- 200 media agents (financial news, social media, industry press)
- 200 sell-side analysts covering the sector
- 100 government/regulatory agents (policy response modeling)

Simulate 40 rounds. Focus on:
- Which specific companies benefit vs suffer
- Timeline: immediate panic vs gradual repricing
- Second-order effects (supply chain, consumer behavior, M&A activity)
- Where "smart money" starts buying
- Which companies agents identify as long-term winners
```

---

## Template 3: Company vs Company Competition

```
SEED DATA NEEDED: Product info for both companies + market share data + recent news

QUERY:
[COMPANY A] just launched [PRODUCT/SERVICE] that directly competes with
[COMPANY B]'s [PRODUCT/SERVICE]. [COMPANY A]'s version is [PRICE] vs
[COMPANY B]'s [PRICE], with [KEY DIFFERENTIATOR].

Simulate how this affects both companies' stock prices and market position
over 90 days.

Create 1,500 agents:
- 400 consumers
  - 150 [COMPANY B] loyalists
  - 100 [COMPANY A] loyalists
  - 100 price-sensitive switchers
  - 50 early adopters (try everything new)
- 300 [COMPANY A] investors (mix of retail/institutional)
- 300 [COMPANY B] investors (mix of retail/institutional)
- 200 neutral market observers (analysts, media)
- 150 employees of both companies (75 each)
- 100 competitor company agents (other players in the space)
- 50 advertiser/partner agents (shift budgets based on market share)

Simulate 30 rounds. Track:
- Consumer switching behavior (who actually moves?)
- Investor sentiment for both stocks
- Does the market see this as zero-sum or growing the pie?
- Media narrative: which company "wins" the coverage?
- Partner/advertiser budget shifts
```

---

## Template 4: Black Swan / Stress Test

```
SEED DATA NEEDED: Historical examples of similar events + current portfolio data

QUERY:
A [BLACK SWAN EVENT -- e.g., "major US bank announces insolvency due to
commercial real estate exposure"] has just occurred. Simulate the market-wide
reaction and how these specific stocks are affected:
[LIST YOUR PORTFOLIO: AAPL, MSFT, NVDA, GOOGL, AMZN, etc.]

Create 2,000 agents:
- 600 panic sellers (retail investors liquidating positions)
- 400 institutional portfolio managers (rebalancing, risk-off)
- 300 value hunters (looking for oversold opportunities)
- 200 algorithmic trading agents (momentum + mean-reversion strategies)
- 200 financial media agents (amplifying fear vs calling for calm)
- 150 Federal Reserve / government agents (policy response)
- 100 corporate treasury agents (companies managing cash, buybacks)
- 50 credit market agents (bond yields, credit spreads)

Simulate 60 rounds. Focus on:
- Which stocks in the portfolio fall hardest?
- Which stocks recover fastest?
- When does panic selling peak?
- When do value buyers step in?
- What policy response do government agents take, and how does it help?
- Portfolio drawdown at worst point
- 60-day recovery trajectory
```

---

## Template 5: IPO First 90 Days

```
SEED DATA NEEDED: S-1/prospectus summary + comparable company data + market conditions

QUERY:
[COMPANY] just IPO'd at $[X]/share, valuing the company at $[X] billion.
The company has $[X] in annual revenue, growing at [X]% YoY, and is
[profitable/unprofitable] with [X]% margins. The IPO was [oversubscribed/
undersubscribed].

Simulate the first 90 trading days including the 90-day lockup expiry.

Create 1,000 agents:
- 250 IPO allocation holders (banks, institutions who got shares at IPO price)
  - 100 quick flippers (sell in first week)
  - 150 hold for evaluation (sell based on performance)
- 200 retail FOMO buyers (buy in first week based on hype)
- 200 long-term growth investors (evaluate fundamentals over 30+ days)
- 100 short sellers (looking for overvaluation signals)
- 100 financial media agents (hype cycle coverage)
- 50 company insiders (can't sell until lockup expires at day 90)
- 50 sell-side analysts (initiate coverage at day 25-30)
- 50 comparable company investors (monitor valuation gap)

Simulate 60 rounds (representing 90 calendar days). Key events:
- Round 1-3: IPO pop dynamics
- Round 5-10: First pullback
- Round 15-20: Analyst coverage initiation
- Round 30-40: Secondary offering rumors
- Round 55-60: Lockup expiry (insiders can sell)
```

---

## Template 6: Dividend/Buyback Announcement

```
SEED DATA NEEDED: Company financials + dividend history + sector comparisons

QUERY:
[COMPANY] announces a [NEW/INCREASED] dividend of $[X]/share (yield of [X]%)
and/or a $[X] billion stock buyback program. The company has $[X]B in cash
and $[X]B in debt.

Simulate how different investor types react over 30 days.

Create 800 agents:
- 200 income investors (dividend-focused, evaluate yield attractiveness)
- 200 growth investors (view dividend as "company has no growth ideas")
- 150 institutional (evaluate capital allocation efficiency)
- 100 index fund agents (mechanical rebalancing)
- 100 media agents
- 50 analysts

Simulate 20 rounds. Track:
- Does income investor buying offset growth investor selling?
- Net sentiment shift
- Comparison to sector peers
```

---

## Quick Reference: Agent Count Guidelines

| Simulation Complexity | Agents | Rounds | Est. Cost (GPT-4o) | Time |
|---|---|---|---|---|
| Quick test | 100-200 | 10 | $0.10-0.30 | 2-3 min |
| Standard analysis | 500 | 20 | $0.50-1.50 | 5-8 min |
| Deep analysis | 1,000 | 30 | $1.00-3.00 | 10-15 min |
| Full simulation | 2,000 | 40 | $3.00-8.00 | 20-30 min |
| Enterprise-grade | 5,000+ | 40+ | $10.00-25.00 | 45-60 min |

**Tip**: Start with "Quick test" to validate your prompt design, then scale up.

---

## Reading Simulation Results for Trading Insights

### What to pay attention to:

1. **Institutional vs Retail divergence** -- When institutions buy while retail sells (or vice versa), follow the institutions. They have more information and longer time horizons.

2. **Media narrative lag** -- If media agents are still bearish but institutional agents have already started buying, the market is likely near a bottom.

3. **Sentiment clustering** -- If 80%+ of agents agree on direction, the move is likely overdone. Contrarian opportunity.

4. **Speed of recovery** -- Fast recovery in simulation = strong fundamental support. Slow recovery = real structural problem.

5. **Second-order effects** -- Which companies BENEFIT from another company's bad news? These are the hidden trades.

### Building Your Track Record

For every simulation you run:

| Field | Record |
|---|---|
| Date | When you ran it |
| Scenario | What you simulated |
| Prediction | What the simulation suggested |
| Actual Outcome | What actually happened |
| Accuracy | How close was it? (qualitative) |
| Lesson | What would you change next time? |

After 20+ simulations with tracked outcomes, you'll know which frameworks produce the best insights for your trading style.
