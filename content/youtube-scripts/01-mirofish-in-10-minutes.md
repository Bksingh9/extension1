# VIDEO 1: MiroFish in 10 Minutes -- Your First AI Simulation

## Video Metadata
- **Title**: MiroFish in 10 Minutes -- Run Your First AI Simulation (2026 Tutorial)
- **Duration**: 10-12 minutes
- **Tags**: mirofish, ai simulation, multi-agent ai, prediction engine, mirofish tutorial, ai agents, future prediction ai, mirofish 2026, ai forecasting
- **Description**: (see below)
- **Thumbnail Text**: "PREDICT THE FUTURE?" with a screenshot of MiroFish running

## YouTube Description
```
Can AI predict the future? MiroFish is an open-source AI prediction engine that
uses THOUSANDS of autonomous agents to simulate real-world scenarios. In this
video, I'll show you how to set it up and run your first simulation in under
10 minutes.

What you'll learn:
00:00 - What is MiroFish?
01:15 - Why this changes everything
02:30 - Quick setup (3 minutes)
05:30 - Running your first simulation
08:00 - Reading the results
09:30 - What to simulate next

Links:
- MiroFish GitHub: https://github.com/666ghj/MiroFish
- Full installation guide: [YOUR BLOG LINK]
- My complete MiroFish course: [UDEMY LINK]
- Get Qwen API key: https://dashscope.aliyun.com/

Follow me:
- Twitter: [YOUR HANDLE]
- Newsletter: [YOUR SUBSTACK]

#MiroFish #AISimulation #MultiAgentAI #Tutorial
```

---

## FULL SCRIPT

### HOOK (0:00 - 0:30)

**[ON CAMERA -- energetic, direct]**

"What if I told you there's an AI tool that can simulate the future? Not guess -- actually *simulate* it with thousands of autonomous AI agents that think, interact, and make decisions just like real people.

It's called MiroFish, it's completely open source, it's backed by a billion-dollar company, and in the next 10 minutes, I'm going to show you how to run your first simulation. Let's go."

**[TRANSITION -- quick cut to screen recording]**

---

### WHAT IS MIROFISH (0:30 - 1:45)

**[SCREEN -- show GitHub repo page]**

"So MiroFish -- 48,000 stars on GitHub, backed by Shanda Group -- is what's called a multi-agent prediction engine. Here's what that means in plain English:

You give it a scenario -- like 'What happens if Company X raises prices by 20%?' -- and it builds a digital world populated by thousands of AI agents. These agents represent consumers, competitors, media, regulators -- all the players in the real world.

Then it lets them loose. They interact, make decisions, react to each other -- and you watch what happens."

**[SCREEN -- show a quick animation or diagram of agents interacting]**

"Think of it like SimCity meets ChatGPT, but for predicting real-world outcomes."

**[KEY POINT -- pause for emphasis]**

"And the wild part? It's free. Open source. You just need API keys for the AI models, which cost pennies per simulation."

---

### WHY THIS MATTERS (1:45 - 2:30)

**[ON CAMERA]**

"Now, why should you care? Three reasons:

**One** -- businesses are already paying thousands of dollars for this kind of scenario analysis from consulting firms. You can now do it yourself.

**Two** -- the predictions are actually interesting. I've run simulations that predicted outcomes I never would have guessed, and I'll show you one today.

**Three** -- this is a skill that's going to be worth a LOT of money. Companies need people who can run these simulations. Right now, almost nobody knows how. First-mover advantage is real."

---

### SETUP (2:30 - 5:30)

**[SCREEN RECORDING -- terminal and browser]**

"Alright, let's get this running. You need three things: Python, Node.js, and API keys. Let me walk you through it.

**Step 1: Clone the repo.**"

```bash
git clone https://github.com/666ghj/MiroFish.git
cd MiroFish
```

**[TYPE IN TERMINAL]**

"**Step 2: Install dependencies.**"

```bash
# Backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

"**Step 3: Get your API keys.** You need two things:

First, an LLM API key. MiroFish recommends Qwen-plus from Alibaba -- it's cheap and works great. Go to dashscope.aliyun.com, sign up, grab your key.

Second, a Zep Cloud key for agent memory. Go to getzep.com, sign up for the free tier."

**[SCREEN -- show .env file or config]**

"Drop both keys into your config file like this..."

```
LLM_API_KEY=your-qwen-key-here
ZEP_API_KEY=your-zep-key-here
```

"**Step 4: Start it up.**"

```bash
# Start backend
python main.py

# In another terminal, start frontend
cd frontend
npm run dev
```

"And boom -- you should see the MiroFish interface at localhost. If you hit any errors, I've got a full troubleshooting guide linked in the description."

---

### FIRST SIMULATION (5:30 - 8:00)

**[SCREEN -- MiroFish UI]**

"Now for the fun part. Let's run our first simulation.

I'm going to test a scenario that's relevant right now: **'What happens when a major social media platform introduces a paid verification system?'**

**[CLICK THROUGH THE UI]**

Step 1: I'll paste in some seed data -- a few news articles about social media trends and verification systems.

Step 2: I type my query in natural language: 'Simulate how users, advertisers, and competitors react when Platform X introduces a $15/month verification badge. Model 30 days of behavior.'

Step 3: I set the parameters:
- 500 agents -- that's a good number for our first run
- 20 simulation rounds -- each round represents roughly a day
- Agent types: regular users, power users, advertisers, competitor platforms, media outlets

Step 4: Hit 'Run Simulation' and... we wait."

**[TIME LAPSE or JUMP CUT -- show progress bar]**

"This takes a few minutes depending on your settings. For 500 agents and 20 rounds, expect 3-5 minutes.

And... we're done. Let's look at the results."

---

### READING RESULTS (8:00 - 9:30)

**[SCREEN -- results page]**

"Okay, here's where it gets interesting. Look at this timeline:

**Rounds 1-5** -- Initial backlash. 60% of simulated users expressed negative sentiment. But look -- the power users? They actually adopted it at a 40% rate. They want the status symbol.

**Rounds 6-12** -- Here's the twist the simulation predicted: advertisers started preferring verified accounts for partnerships. This created an economic incentive that the initial backlash didn't account for.

**Rounds 13-20** -- Adoption climbed to 25% overall, but -- and this is the key finding -- competitor platforms saw a 15% user increase from people who left.

**[HIGHLIGHT THE REPORT]**

The automated report summarizes it perfectly: 'Paid verification creates a two-tier ecosystem. Short-term backlash is real but insufficient to reverse adoption once economic incentives kick in. Biggest risk is competitor poaching of mid-tier creators.'

That's genuinely useful insight. A consulting firm would charge thousands for this analysis. We just did it in 10 minutes."

---

### WHAT'S NEXT (9:30 - 10:30)

**[ON CAMERA]**

"So now you've run your first simulation. Here's what I'd suggest:

**Start simple.** Run 3-5 more simulations on topics you're curious about. Get a feel for how agents behave and what kinds of questions produce the most interesting results.

**Keep rounds under 40.** The docs warn about resource consumption, and your API bill will thank you.

**Save your results.** Every simulation you run is potential content, a potential case study, or a potential product you can sell.

In my next video, I'm going to show you how to build **custom agents** and run a simulation that actually predicted a real-world outcome. You won't want to miss it.

If this was helpful, smash subscribe -- I'm going deep on MiroFish and AI simulation. Drop a comment telling me what scenario YOU want me to simulate, and I might feature it in an upcoming video.

See you in the next one."

**[END SCREEN -- subscribe button, next video link]**

---

## PRODUCTION NOTES

### B-Roll Needed
- MiroFish GitHub page scrolling
- Terminal commands running
- MiroFish UI walkthrough
- Agent interaction visualization
- Results/report page
- Diagram of how multi-agent simulation works

### Screen Recording Tips
- Use 1920x1080, dark terminal theme
- Zoom into text when showing code/config
- Use mouse highlighter plugin
- Add subtle zoom animations on key moments

### Editing Notes
- Keep cuts tight -- no dead air
- Add lower-third text for key terms
- Use sound effects sparingly (whoosh on transitions)
- Background music: lo-fi or ambient tech (low volume)
- Total runtime target: 10-12 minutes (sweet spot for YouTube algorithm)
