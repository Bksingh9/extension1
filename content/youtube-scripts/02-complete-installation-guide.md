# VIDEO 2: MiroFish Complete Installation Guide -- Every OS, Every Error

## Video Metadata
- **Title**: How to Install MiroFish on ANY Computer (Mac, Windows, Linux) -- Full Setup Guide 2026
- **Duration**: 15-20 minutes
- **Tags**: mirofish install, mirofish setup, mirofish tutorial, install mirofish windows, install mirofish mac, mirofish api key, qwen api setup, zep cloud setup
- **Thumbnail Text**: "INSTALL MIROFISH" with checkmarks and OS logos

## YouTube Description
```
The COMPLETE guide to installing MiroFish on Mac, Windows, and Linux.
I cover every step, every common error, and every gotcha so you can get
your AI simulation engine running in under 20 minutes.

Timestamps:
00:00 - What you need before starting
01:30 - Mac installation
05:00 - Windows installation
08:30 - Linux installation
11:00 - Getting API keys (Qwen + Zep Cloud)
13:30 - Configuration & first test run
16:00 - Troubleshooting common errors
18:00 - Next steps

Links:
- MiroFish GitHub: https://github.com/666ghj/MiroFish
- Python 3.11+: https://python.org
- Node.js 18+: https://nodejs.org
- Qwen API: https://dashscope.aliyun.com/
- Zep Cloud: https://www.getzep.com/

#MiroFish #Installation #Tutorial
```

---

## FULL SCRIPT

### HOOK (0:00 - 0:20)

"Installing MiroFish should take 15 minutes. For most people, it takes 3 hours because of one wrong Python version or a missing dependency. This video makes sure you get it right the first time. Every OS. Every common error. Let's go."

---

### PREREQUISITES (0:20 - 1:30)

**[ON CAMERA with checklist graphic]**

"Before we touch anything, here's what you need:

1. **Python 3.11 or 3.12** -- not 3.10, not 3.13. Specifically 3.11 or 3.12. I'll show you how to check.
2. **Node.js 18 or higher** -- for the frontend.
3. **Git** -- to clone the repo.
4. **A text editor** -- VS Code recommended.
5. **API keys** -- we'll set these up together.

Let me show you how to verify what you already have."

```bash
python3 --version    # Need 3.11.x or 3.12.x
node --version       # Need 18.x or higher
git --version        # Any recent version
```

"If any of these are wrong or missing, don't worry -- I'll cover installation for each OS."

---

### MAC INSTALLATION (1:30 - 5:00)

**[SCREEN -- Mac terminal]**

"Mac users, you're lucky -- this is the easiest setup.

**Install Homebrew if you don't have it:**"
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

"**Install Python 3.12 and Node.js 18:**"
```bash
brew install python@3.12 node@18
```

"**Important Mac gotcha:** macOS comes with Python 3 but it might be an old version. Always use `python3.12` explicitly or set up an alias.

**Clone MiroFish:**"
```bash
git clone https://github.com/666ghj/MiroFish.git
cd MiroFish
```

"**Create a virtual environment** -- trust me, do this. It prevents dependency conflicts:"
```bash
python3.12 -m venv venv
source venv/bin/activate
```

"**Install Python dependencies:**"
```bash
pip install -r requirements.txt
```

"**Install frontend:**"
```bash
cd frontend
npm install
cd ..
```

"If you see any errors about 'gcc' or 'xcode', run `xcode-select --install` and try again. That's the #1 Mac issue."

---

### WINDOWS INSTALLATION (5:00 - 8:30)

**[SCREEN -- Windows PowerShell/Terminal]**

"Windows users, pay close attention -- there are a few extra steps.

**Step 1: Install Python 3.12** from python.org. During installation, CHECK the box that says 'Add Python to PATH'. This is the number one mistake people make. If you miss it, nothing works.

**Step 2: Install Node.js 18+** from nodejs.org. The LTS version is fine. Default settings, just click through.

**Step 3: Install Git** from git-scm.com if you don't have it.

**Verify everything in PowerShell:**"
```powershell
python --version
node --version
git --version
```

"**Clone and setup:**"
```powershell
git clone https://github.com/666ghj/MiroFish.git
cd MiroFish

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate

# Install dependencies
pip install -r requirements.txt

# Frontend
cd frontend
npm install
cd ..
```

"**Windows-specific issues:**
- If you get 'execution policy' errors with venv, run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- If npm fails, try running PowerShell as Administrator
- If you get SSL errors, it's usually your antivirus -- temporarily disable it during install"

---

### LINUX INSTALLATION (8:30 - 11:00)

**[SCREEN -- Linux terminal]**

"Linux users, you probably know most of this, but here's the clean path.

**Ubuntu/Debian:**"
```bash
sudo apt update
sudo apt install python3.12 python3.12-venv python3-pip nodejs npm git
```

"**If Python 3.12 isn't in your default repos:**"
```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.12 python3.12-venv
```

"**Fedora/RHEL:**"
```bash
sudo dnf install python3.12 nodejs npm git
```

"**Then the standard setup:**"
```bash
git clone https://github.com/666ghj/MiroFish.git
cd MiroFish
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd frontend && npm install && cd ..
```

"Linux is generally the smoothest. If you hit permission errors, don't use sudo with pip -- use the virtual environment instead."

---

### API KEYS (11:00 - 13:30)

**[SCREEN -- browser + config file side by side]**

"Now the part that actually costs money -- but not much.

**API Key 1: LLM (Qwen-plus recommended)**

Go to dashscope.aliyun.com. Create an account. Navigate to API Keys. Generate a new key. Copy it.

Why Qwen? It's the cheapest option that works well with MiroFish. A typical simulation costs $0.05-0.50 depending on agent count and rounds.

**Alternative:** You can use any OpenAI SDK-compatible API. If you already have an OpenAI key, that works too -- just costs more.

**API Key 2: Zep Cloud**

Go to getzep.com. Sign up. They have a free tier that's enough for getting started. Navigate to your project settings and grab your API key.

**Configure MiroFish:**"

```bash
# Copy the example config
cp .env.example .env

# Edit with your keys
nano .env  # or open in VS Code
```

```env
LLM_API_KEY=sk-your-qwen-key-here
LLM_MODEL=qwen-plus
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
ZEP_API_KEY=your-zep-key-here
```

"Save it. That's your configuration done."

---

### FIRST TEST RUN (13:30 - 16:00)

**[SCREEN -- two terminal windows side by side]**

"Let's verify everything works.

**Terminal 1 -- Start the backend:**"
```bash
source venv/bin/activate  # if not already activated
python main.py
```

"You should see the server starting up with no errors. If you see 'Server running on port XXXX' -- you're golden.

**Terminal 2 -- Start the frontend:**"
```bash
cd frontend
npm run dev
```

"Open your browser to the URL it shows -- usually localhost:5173 or localhost:3000.

You should see the MiroFish interface. Try running the default example simulation -- it should complete in 2-3 minutes.

If you see results appearing... congratulations. You're set up."

---

### TROUBLESHOOTING (16:00 - 18:00)

**[ON CAMERA with error messages as graphics]**

"Here are the top 5 errors people hit and how to fix them:

**Error 1: 'ModuleNotFoundError'**
You're not in your virtual environment. Run `source venv/bin/activate` (Mac/Linux) or `.\venv\Scripts\Activate` (Windows).

**Error 2: 'API key invalid' or '401 Unauthorized'**
Double-check your .env file. No extra spaces, no quotes around the key. Make sure you copied the full key.

**Error 3: 'Port already in use'**
Another process is using that port. Kill it with `lsof -i :PORT_NUMBER` then `kill PID`, or change the port in config.

**Error 4: 'npm ERR! ERESOLVE'**
Delete `node_modules` and `package-lock.json` in the frontend folder, then run `npm install` again.

**Error 5: Simulation hangs or times out**
Your API key might have rate limits. Start with fewer agents (50-100) and fewer rounds (5-10) for your first run.

If you hit something not on this list, drop a comment below -- I personally respond to every installation question."

---

### NEXT STEPS (18:00 - 19:00)

"You're set up. In the next video, I'm going to run a simulation that tries to predict something real -- and we'll see how close the AI gets. Subscribe so you don't miss it.

And if you want the full deep dive, my Udemy course covers everything from beginner to building your own custom agents. Link in the description."

---

## PRODUCTION NOTES

### Recording Strategy
- Record Mac, Windows, and Linux sections separately
- Use clean VMs/fresh installs for authenticity
- Show REAL errors and fix them on camera (builds trust)
- Have all URLs in a pinned comment for easy copy-paste

### Chapters (YouTube Chapters)
```
0:00 Prerequisites
1:30 Mac Installation
5:00 Windows Installation
8:30 Linux Installation
11:00 Getting API Keys
13:30 First Test Run
16:00 Troubleshooting
18:00 Next Steps
```
