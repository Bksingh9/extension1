# MiroFish: The Complete Beginner's Guide (2026)

> **SEO Target Keywords**: mirofish tutorial, mirofish guide, mirofish ai simulation, how to use mirofish, mirofish setup
> **Meta Description**: Learn how to use MiroFish, the open-source AI prediction engine with 48k+ GitHub stars. Complete setup guide, first simulation walkthrough, and real-world use cases.
> **Estimated Reading Time**: 15 minutes
> **Publish On**: Blog, Medium, Dev.to, Hashnode

---

What if you could test your biggest decisions before making them -- without any real-world consequences?

That's exactly what **MiroFish** does. It's an open-source AI prediction engine that simulates real-world scenarios using thousands of autonomous AI agents. Feed it data, ask a question, and watch thousands of digital agents interact, react, and produce outcomes you never would have predicted.

In this guide, I'll walk you through everything: what MiroFish is, how to set it up, how to run your first simulation, and how people are already using it to make better decisions.

---

## What Is MiroFish?

MiroFish is a **multi-agent prediction engine** built by a team backed by [Shanda Group](https://en.wikipedia.org/wiki/Shanda), one of China's largest internet companies.

Here's the simple explanation: You describe a scenario in plain English -- "What happens if Company X raises prices by 20%?" -- and MiroFish builds a digital world populated by AI agents representing consumers, competitors, media outlets, regulators, and more. These agents interact with each other, make decisions, and produce outcomes.

Think of it as **SimCity meets ChatGPT**, but for predicting real-world events.

### Key Stats
- **48,500+ GitHub stars** (and growing fast)
- **7,000+ forks**
- **260+ commits** with active development
- **v0.1.2** released March 2026
- **AGPL-3.0** open-source license
- **Backed by Shanda Group** (billion-dollar Chinese internet conglomerate)

### What Makes It Different?

Unlike ChatGPT or Claude, which give you a single AI's opinion, MiroFish creates **thousands of independent agents** that interact with each other. Each agent has:

- Its own personality and decision-making style
- Persistent memory (it remembers previous interactions)
- The ability to influence and be influenced by other agents
- Role-specific behavior (a "media agent" acts differently from a "consumer agent")

The result isn't one AI's guess -- it's an **emergent simulation** where outcomes arise from complex interactions between agents, just like in the real world.

---

## Prerequisites

Before installing MiroFish, make sure you have:

| Requirement | Version | Check Command |
|---|---|---|
| Python | 3.11 or 3.12 | `python3 --version` |
| Node.js | 18 or higher | `node --version` |
| Git | Any recent version | `git --version` |
| RAM | 8GB minimum | -- |
| Disk Space | ~2GB | -- |

You'll also need API keys (covered in the setup section below).

---

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/666ghj/MiroFish.git
cd MiroFish
```

### Step 2: Set Up Python Environment

Always use a virtual environment to avoid dependency conflicts:

```bash
# Create virtual environment
python3.12 -m venv venv

# Activate it
# Mac/Linux:
source venv/bin/activate
# Windows:
.\venv\Scripts\Activate
```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs the AI frameworks, GraphRAG tools, and simulation engine. It may take a few minutes.

### Step 4: Install Frontend

```bash
cd frontend
npm install
cd ..
```

### Step 5: Get Your API Keys

You need two API keys:

**1. LLM API Key (for the AI brain)**

MiroFish recommends **Qwen-plus** from Alibaba (cheapest option):
1. Go to [dashscope.aliyun.com](https://dashscope.aliyun.com/)
2. Create an account
3. Navigate to API Keys
4. Generate and copy your key

*Alternative*: Any OpenAI SDK-compatible API works (OpenAI, Anthropic via proxy, local models via Ollama).

**2. Zep Cloud Key (for agent memory)**

1. Go to [getzep.com](https://www.getzep.com/)
2. Sign up (free tier available)
3. Create a project
4. Copy your API key

### Step 6: Configure

```bash
cp .env.example .env
```

Edit the `.env` file:

```env
LLM_API_KEY=sk-your-qwen-key-here
LLM_MODEL=qwen-plus
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
ZEP_API_KEY=your-zep-key-here
```

### Step 7: Launch

Open two terminal windows:

**Terminal 1 (Backend):**
```bash
source venv/bin/activate
python main.py
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

Open your browser to the URL shown (usually `http://localhost:5173`).

---

## Your First Simulation

Let's run a simulation that demonstrates MiroFish's power.

### Scenario: "What happens when a popular coffee chain doubles its prices?"

**Step 1: Prepare seed data**

Paste or upload a few relevant articles about coffee industry trends, consumer price sensitivity, and competitive dynamics. The more relevant your seed data, the better the simulation.

**Step 2: Write your query**

In the MiroFish interface, type:

> "Simulate what happens when a major coffee chain doubles all prices overnight. Model consumer behavior, competitor reactions, media coverage, and employee sentiment over 30 days. Include 500 agents: 300 consumers (varying income levels), 100 competitor business agents, 50 media agents, and 50 employees."

**Step 3: Configure parameters**

- **Agents**: 500 (good balance of detail vs speed)
- **Rounds**: 20 (each round ~ 1-2 simulated days)
- **Start with fewer rounds** for your first run to keep API costs low

**Step 4: Run and observe**

Click "Run Simulation." For 500 agents and 20 rounds, expect 3-7 minutes.

### Reading Your Results

MiroFish produces several outputs:

1. **Timeline**: A round-by-round breakdown of what happened
2. **Agent Behavior Summary**: How different agent types reacted
3. **Automated Report**: A ReportAgent synthesizes findings into a readable summary
4. **Interactive Chat**: You can chat with individual agents to understand their reasoning

**Sample findings you might see:**
- Low-income consumers switch to competitors by round 3
- Media agents amplify outrage, accelerating customer loss
- Competitors initially celebrate, then some raise prices to capture margin
- By round 15, the coffee chain loses ~40% of foot traffic
- Employee agents show declining morale, some "quit"

---

## Real-World Use Cases

### For Business Professionals
- **Product launches**: Simulate consumer and competitor reactions before spending marketing budget
- **Pricing strategy**: Test price changes with thousands of simulated customers
- **Crisis planning**: Model how PR disasters unfold and test response strategies

### For Researchers & Analysts
- **Policy analysis**: Simulate how populations respond to new regulations
- **Social dynamics**: Model information spread, opinion formation, and behavioral change
- **Urban planning**: Simulate how infrastructure changes affect communities

### For Content Creators & Entrepreneurs
- **Report business**: Run simulations on trending topics and sell prediction reports
- **Consulting**: Use simulations to back up strategic recommendations
- **Education**: Create courses teaching others how to use multi-agent simulation

---

## Tips for Better Simulations

1. **Start small**: Begin with 100-200 agents and 10-15 rounds. Scale up once you understand the tool.

2. **Seed data matters**: The quality of your simulation depends heavily on the seed materials you provide. Use recent, relevant articles and data.

3. **Be specific in queries**: "What happens to housing prices?" is vague. "What happens to median home prices in Austin, TX if 3 major tech companies announce remote-first policies?" is much better.

4. **Run multiple simulations**: Single runs can be fluky. Run the same scenario 3-5 times and look for consistent patterns.

5. **Watch your API costs**: Keep rounds under 40 initially. A 5,000-agent, 40-round simulation can cost $3-5 in API calls.

6. **Use the agent chat**: After simulation, chat with individual agents to understand WHY they made certain decisions. This is where the deepest insights hide.

---

## Cost Breakdown

| Usage Level | Agents | Rounds/Month | Approx. Monthly Cost |
|---|---|---|---|
| Casual | 100-200 | 10-20 sims | $10-30 |
| Regular | 500 | 30-50 sims | $50-150 |
| Heavy | 2,000+ | 100+ sims | $200-500 |

Costs are primarily from LLM API calls (Qwen-plus is cheapest) and Zep Cloud (free tier covers light usage).

---

## Common Errors and Fixes

| Error | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError` | Not in virtual environment | `source venv/bin/activate` |
| `401 Unauthorized` | Bad API key | Check `.env` file, no extra spaces |
| `Port already in use` | Previous instance running | Kill the process or change port |
| Simulation hangs | Rate limit or timeout | Use fewer agents/rounds |
| `npm ERR! ERESOLVE` | Dependency conflict | Delete `node_modules` + `package-lock.json`, reinstall |

---

## What's Next?

Now that you've run your first simulation, here are three paths forward:

1. **Go deeper**: Try complex multi-variable scenarios with thousands of agents
2. **Build a business**: Use MiroFish for consulting, report generation, or SaaS
3. **Learn the internals**: Study GraphRAG, the OASIS framework, and custom agent development

I publish weekly simulation reports and tutorials. Subscribe to my newsletter for the latest: **[YOUR SUBSTACK LINK]**

---

## Resources

- [MiroFish GitHub Repository](https://github.com/666ghj/MiroFish)
- [OASIS Framework (CAMEL-AI)](https://github.com/camel-ai/oasis)
- [Zep Cloud Documentation](https://www.getzep.com/)
- [GraphRAG by Microsoft](https://github.com/microsoft/graphrag)
- [Qwen API Documentation](https://dashscope.aliyun.com/)

---

*This guide is maintained and updated regularly. Last updated: April 2026.*

*Have questions? Drop a comment below or reach out on Twitter: **[YOUR HANDLE]***
