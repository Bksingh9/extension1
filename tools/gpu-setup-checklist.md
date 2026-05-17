# GPU setup checklist — buy or rent the cheapest GPU that works

> **Purpose.** Generic spec sheet for buying or renting a GPU to
> run AI workloads (ComfyUI / Stable Diffusion / video generation /
> LLM inference) and getting them running end-to-end.
> Self-contained: every fact, link, and verification command an
> assistant needs is in this file.
>
> **Scope.** Workload-agnostic. The original use case was YouTube
> B-roll for *The Dossier*, but every recommendation below applies
> to any creator/developer running ComfyUI, A1111, Forge, Diffusers,
> Ollama, vLLM, llama.cpp, or any other consumer AI tool.
>
> **What this document does NOT do.** It does not, and an assistant
> following it should not, complete a purchase. The user must
> execute the buy themselves — payment method, shipping address,
> and account are theirs to provide.

---

## 0 · Pre-installed in this repo

Already done by an earlier session and ready to drop onto a GPU host:

- `~/ComfyUI/` — ComfyUI core + venv + custom nodes (Manager,
  AnimateDiff-Evolved, VideoHelperSuite, Frame-Interpolation),
  verified HTTP 200 on port 8188. Awaits model weights.
- `~/ComfyUI/workflows/text_to_video_sd15_animatediff.json` —
  example T2V workflow.
- `~/ComfyUI/start.sh` — auto-picks `--cpu` / `--lowvram` /
  `--normalvram` / `--highvram` from env vars.
- `tools/LTX-Video/` — submodule, Lightricks LTX-Video repo.
- `pipeline/broll.py` — LTX-Video runner for B-roll generation.
- `tools/video-gen.md` — model VRAM tiers reference.

---

## 1 · Pre-purchase questions

Ask in order. Numeric column shows the threshold that flips the
recommendation:

| # | Question | Threshold |
|---|---|---|
| 1 | Hours of GPU use per day on average? | ≥ 1 → own · < 1 → rent |
| 2 | Will you train (LoRA, fine-tune, dreambooth)? | yes → 24 GB+ owned · no → either |
| 3 | Models you actually want to run? | image only · video · LLM · all |
| 4 | Largest model VRAM requirement? | see §2 model table |
| 5 | Need offline / privacy / no third-party? | yes → must own · no → cloud OK |
| 6 | Used hardware acceptable? | yes → §3.1 / §3.4 · no → §3.2 / §3.3 |
| 7 | Budget cap (USD)? | drives §3 tier |

**Decision tree:**

```
budget < $400          → rent only (§4)
budget $700–900        → §3.1 used 3090 (24 GB)
budget $1,500          → §3.2 used 4090 (24 GB) — when 5090 stock cleared the resale market
budget $2,000–2,500    → §3.3 RTX 5090 (32 GB) new
budget $7,500+         → §3.5 RTX 6000 Ada (48 GB) — only if §1.2 = yes + 48 GB needed
> 1 hr/day video gen   → §3.3 5090 unless §1.7 demands otherwise
< 1 hr/day total       → rent (§4)
```

---

## 2 · VRAM tiers — what each unlocks

| VRAM | Image gen | Video gen | LLM inference |
|---|---|---|---|
| 8 GB | SD 1.5, SDXL with `--medvram` | AnimateDiff @ low res | 7B Q4 (Mistral 7B, Llama 3.1 8B) |
| 12 GB | SD 1.5 / SDXL comfortably | AnimateDiff 512×512 | 13B Q4 |
| **16 GB** | **SDXL / SD 3, Flux schnell** | LTX-Video distilled (slow) | 30B Q4 |
| **24 GB** | **Flux dev**, training LoRAs | **LTX-Video 13B distilled, CogVideoX-5B** | 70B Q3 / Q4 quants |
| 32 GB | All above with batch > 1 | LTX-Video 13B distilled comfortably | 70B Q4 / Q5 |
| 48 GB | Flux dev training | LTX-Video 13B **dev** | 70B unquantised |
| 80 GB | — | **HunyuanVideo, Mochi-1, Wan 2.1 full** | 70B at fp16, multi-GPU territory |

**Sweet spot for most creators: 24 GB.** Covers every consumer
workflow today; only top-tier research video models need more.

---

## 3 · GPU shortlist (buying)

All prices mid-2026 retail; verify before purchase.

### 3.1 Used RTX 3090 — 24 GB — **$650–900** — CHEAPEST 24 GB

| Spec | Value |
|---|---|
| Architecture | Ampere (GA102) |
| VRAM | 24 GB GDDR6X |
| TDP | 350 W |
| Power connector | 2× 8-pin PCIe (or 1× 12-pin → 2× 8-pin adapter on FE) |
| Slot width | 3 slots typical |
| Length | ~313 mm |

**Where to find them (cheapest first):**

1. **Government surplus auctions** — §3.7. Often $300–500 if you
   catch a federal/state IT refresh. Worth checking weekly.
2. **Reddit r/hardwareswap** — heat-required, $700–800 common.
3. **eBay used + "Buy It Now" filter sorted price-ascending**, with
   feedback ≥ 99 %, returns accepted, US/EU shipping. $750–900.
4. **Facebook Marketplace local** — $700–850, in-person tests
   possible.
5. **r/buildapcsales** — new old stock occasionally at $800–950.
6. **Newegg / Microcenter open-box** — $850–950 with warranty.

### 3.2 Used RTX 4090 — 24 GB — **$1,200–1,600**

Same VRAM as 3090, ~70 % faster, half the power efficiency
improvement. Used inventory is rising in 2026 as 5090 adopters sell
off. Hunt the same sources as §3.1.

### 3.3 RTX 5090 — 32 GB — **$2,000–2,500** — BEST NEW

| Spec | Value |
|---|---|
| Architecture | Blackwell (GB202) |
| VRAM | 32 GB GDDR7 |
| TDP | 575 W |
| Power connector | 12V-2×6 (NOT 12VHPWR — use a PSU with the native cable) |
| Slot width | 2.5–3.5 slots |
| Length | ~360 mm Founders Edition |

Worth the premium over 3090 only if §1.1 ≥ 1 hr/day. Otherwise the
used 3090 hits the same 24-GB-tier ceiling for 1/3 the price.

### 3.4 Used RTX 3090 Ti — **$800–1,000** — niche

24 GB faster memory than 3090, marginally faster compute, 450 W
TDP. Pick only if found near 3090 pricing.

### 3.5 RTX 6000 Ada — 48 GB — **$5,500–7,500 (used) · $7,500–9,000 (new)**

Workstation Lovelace card, blower cooler, 300 W. Only buy if you'll
specifically use LTX-Video 13B *dev* tier, train medium-sized LoRAs
on large datasets, or run 70B LLMs unquantised.

### 3.6 Cards to skip

| Card | Why |
|---|---|
| RTX 4080 / 4070 Ti | 16 GB / 12 GB — falls short of 24 GB tier |
| RTX 5080 | 16 GB GDDR7 — same VRAM problem |
| AMD RX 7900 XTX (24 GB) | ROCm coverage for video diffusion still incomplete in 2026 |
| Intel Arc A770/B580 | IPEX path works for SDXL, less so for video gen |
| Mac Studio (any) | MPS path patchy; not recommended for ComfyUI |
| H100 / H200 | Datacenter; $20k–35k. Rent instead. |

### 3.7 Government surplus auctions — the cheap path

US federal and state agencies (DoD, GSA, universities, hospitals,
schools) liquidate IT hardware quarterly. Workstations from R&D
labs often had **RTX A4000, A5000, A6000, Tesla T4, V100,
RTX 3090s** for ML projects that ended.

**Live sites (browse from your own machine — all are blocked on
this sandbox):**

| Site | Coverage | Notes |
|---|---|---|
| `gsaauctions.gov` | US federal civilian | Need free account. Watch lists supported. |
| `govdeals.com` | US state / local / fed | Largest. Categories: "Computers & Tablets" → "Computer Components" → "Graphics Cards" |
| `govplanet.com` | US military surplus | More vehicles than PCs, but occasional workstation drops. |
| `liquidation.com` | private liquidators + some gov | Big-lot only; bid only if you'll resell extras. |
| `publicsurplus.com` | US K-12, universities | Lots of lab workstations. |
| `treasury.gov auctions` | US federal seizures | Rare GPU hits but occasionally servers. |
| `nationwidesurplus.com` | gov + private | Mid-tier inventory. |
| `auctionsplus.com.au` | AU government | If outside US. |
| `disposable.gov.uk` (UK gov surplus portal) | UK government | UK readers. |
| Local university surplus stores | Walk-in | Search `"<your-state> university surplus"`. |

**Typical price range when GPUs do appear:**

| Card | Surplus typical | Retail used | Notes |
|---|---|---|---|
| RTX A4000 (16 GB) | $250–400 | $450–650 | Best surplus deal; 16 GB workstation Ampere. |
| RTX A5000 (24 GB) | $400–700 | $900–1,200 | The bargain — 24 GB single-slot blower. |
| RTX A6000 (48 GB) | $1,200–2,000 | $3,500–4,500 | Rare; pounce if you see one < $1,500. |
| RTX 3090 (24 GB) | $300–500 | $700–900 | Occasionally drops from research labs. |
| Tesla V100 16/32 GB | $200–400 | $500–900 | Datacenter card; needs blower + ECC server. |
| Tesla T4 (16 GB) | $150–250 | $400–600 | Low-power but slow. |

**Risks specific to surplus auctions:**

1. **Sold "as-is" no warranty.** Test on arrival; can't return.
2. **No accessories** — usually card only, no power cables, no box.
3. **DRM / vBIOS lockout** — some Quadro/Tesla cards from
   specific OEMs (Dell, HP, Lenovo) ship with locked vBIOS that
   only signed BIOSes will boot. Verify the model number on
   TechPowerUp's GPU database before bidding.
4. **Mining cards** — possible but rare in government surplus
   (most surplus comes from research labs, not miners). Ask the
   seller; often they don't know.
5. **Shipping** — pickup-only auctions are common. Check this
   before bidding.

---

## 4 · Cloud rental — when not to buy

| Provider | GPU | $/hr | Setup time | Best for |
|---|---|---|---|---|
| **RunPod** | RTX 3090 24 GB (spot) | ~$0.30 | 2 min | dev iteration |
| RunPod | RTX A5000 24 GB | ~$0.34 | 2 min | reliable on-demand |
| RunPod | RTX 4090 24 GB | ~$0.69 | 2 min | fastest 24 GB |
| RunPod | H100 80 GB | ~$3.30 | 2 min | HunyuanVideo / batch |
| Modal | A100 40 GB | ~$0.0006/s | 0 min serverless | one-off batches |
| Vast.ai | varies | $0.20–0.80 | 5 min | cheapest spot |
| Lambda Cloud | A100/H100 | $1.10–2.50 | 5 min | stable reservation |
| Colab Pro | T4 / L4 / A100 | $10/mo flat | 1 min | notebook only |
| Paperspace | A6000 | $1.10 | 3 min | always-on workstation feel |

**Break-even rule of thumb:** owning makes sense around
**2,000–3,000 hours of GPU use** versus renting at $0.30–0.50/hr.
Below that, rent.

---

## 5 · System requirements (if buying)

| Item | 24 GB tier | 5090 tier | 6000 Ada tier |
|---|---|---|---|
| PSU | 850 W 80+ Gold | 1000 W 80+ Gold + native 12V-2×6 | 850 W |
| Power connector | 2× 8-pin | 12V-2×6 (no adapter) | 1× 16-pin |
| Case slot clearance | 3 slots | 3.5 slots | 2 slots (blower) |
| Case length | 320 mm | 360 mm | 270 mm |
| CPU | Ryzen 5 / Core i5 5-yr-old+ | Same | Same |
| RAM | 32 GB DDR4/5 | 32 GB DDR5 | 32 GB ECC preferred |
| Storage | 2 TB NVMe Gen 4 | Gen 4 or 5 | Gen 4 |
| Cooling | 3× 140 mm intake | + rear exhaust | blower self-cools |
| OS | Ubuntu 22.04 / 24.04 LTS | Same | Same |
| Driver | NVIDIA ≥ 535 | NVIDIA ≥ 570 | NVIDIA ≥ 535 |

---

## 6 · Chrome extensions + browser tools for deal hunting

Install these in **your own** Chrome (not on this sandbox — Chrome
Web Store is blocked here):

| Tool | Use | Where |
|---|---|---|
| **eBay app / built-in saved search alerts** | Email when matching listing appears | ebay.com → search → save w/ email alerts |
| **Keepa** (Chrome ext) | Amazon price history; alerts on drops | chromewebstore.google.com → "Keepa" |
| **CamelCamelCamel** (Chrome ext) | Same idea, second source | chromewebstore.google.com → "Camelizer" |
| **PriceBlink** (Chrome ext) | Compare current page price across stores | chromewebstore.google.com → "PriceBlink" |
| **Honey / Capital One Shopping** | Auto-apply coupons; less useful for GPUs | chromewebstore.google.com |
| **r/hardwareswap RSS** | Feed of new posts; pipe to Telegram/email | `https://www.reddit.com/r/hardwareswap/.rss` |
| **gsaauctions.gov watch lists** | Built-in alerting on saved searches | Site account → My Saved Searches |
| **govdeals.com email alerts** | Same | Site account → Email Alerts |
| **eBay Sniping Tool (Gixen / BidSlammer)** | Auto-bid in last 8 seconds of an auction | External service, links to your eBay account |

**No Chrome extension reliably buys hardware autonomously.** Even
Honey only applies coupons; the human still clicks "Place Order."

**A pragmatic deal-hunt workflow on your laptop:**

1. Save GPU-of-interest search on eBay with email alerts.
2. Save same search on govdeals.com and gsaauctions.gov.
3. Subscribe to `r/hardwareswap.rss` and `r/buildapcsales.rss`.
4. Install Keepa for Amazon refurbished alerts.
5. Set a Discord/Telegram channel for `#deal-alerts` to pipe RSS.
6. When alert fires: verify model #, check feedback, bid or buy.

---

## 7 · Setup runbook (after GPU is in or pod is up)

### 7.1 Driver + CUDA verification
```bash
nvidia-smi                                          # card + driver
python -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0))"
# Expected: True, "NVIDIA GeForce RTX 3090" (or your card)
```

### 7.2 Clone repo + sync submodule
```bash
git clone <repo-url> <dir>
cd <dir>
git submodule update --init --recursive
```

### 7.3 ComfyUI install (mirror what the CPU sandbox session did)
```bash
cd ~
git clone --depth 1 https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/pip install -r requirements.txt
mkdir -p models/{checkpoints,animatediff_models,vae,loras,clip_vision} custom_nodes
cd custom_nodes
for r in ltdrdata/ComfyUI-Manager Kosinkadink/ComfyUI-AnimateDiff-Evolved \
         Kosinkadink/ComfyUI-VideoHelperSuite Fannovel16/ComfyUI-Frame-Interpolation; do
  git clone --depth 1 "https://github.com/$r.git"
done
for d in ComfyUI-Manager ComfyUI-VideoHelperSuite; do
  [ -f "$d/requirements.txt" ] && ../.venv/bin/pip install -r "$d/requirements.txt"
done
```

### 7.4 Download models
```bash
.venv/bin/pip install huggingface_hub
huggingface-cli login                  # free HF token from huggingface.co
cd models/checkpoints
huggingface-cli download stable-diffusion-v1-5/stable-diffusion-v1-5 \
  v1-5-pruned-emaonly.safetensors --local-dir .
cd ../animatediff_models
huggingface-cli download guoyww/animatediff mm_sd_v15_v2.ckpt --local-dir .
```

### 7.5 Launch
```bash
cd ~/ComfyUI && GPU=1 VRAM_GB=24 ./start.sh
# UI: http://127.0.0.1:8188/
# On RunPod: use the forwarded port URL from the pod console.
```

---

## 8 · End-to-end verification

All of the following must pass:

```bash
# (a) GPU visible to torch
python -c "import torch; assert torch.cuda.is_available(), 'no GPU'; print(torch.cuda.get_device_name(0))"

# (b) ComfyUI HTTP up
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8188/   # 200

# (c) Custom video nodes loaded
curl -s http://127.0.0.1:8188/object_info | python -c "
import sys, json
d = json.load(sys.stdin)
for k in ['ADE_AnimateDiffLoaderGen1','VHS_VideoCombine','RIFE VFI']:
    assert k in d, f'missing node: {k}'
print('all video nodes loaded')
"

# (d) Models present
ls ~/ComfyUI/models/checkpoints/v1-5-pruned-emaonly.safetensors
ls ~/ComfyUI/models/animatediff_models/mm_sd_v15_v2.ckpt

# (e) Example workflow runs
# In browser: File → Open → workflows/text_to_video_sd15_animatediff.json
# → Queue Prompt → expect ~30s on a 3090, ~15s on a 5090.
```

---

## 9 · Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `torch.cuda.is_available() == False` | No driver / wrong torch wheel | `nvidia-smi`; reinstall torch from pytorch.org for your CUDA |
| ComfyUI port unresponsive | Process crashed | `tail ~/ComfyUI/start.log`; `pkill -f "python main.py"`; restart |
| `Model not found` | Models not in `models/checkpoints/` | Re-run §7.4 |
| `OutOfMemoryError` mid-generation | Model too big for VRAM | Lower resolution / frames; use `--lowvram` |
| Custom node import error | Missing Python dep | `cd custom_nodes/<node> && ../../.venv/bin/pip install -r requirements.txt` |
| RunPod pod preempted | Spot lost | Switch to on-demand or use Modal serverless |
| 12V-2×6 connector hot | Adapter / under-seated | Use native cable; reseat fully |
| Driver kernel error on boot | Secure Boot blocking module | Disable Secure Boot or sign the NVIDIA module |
| Surplus card won't post | OEM-locked vBIOS | Verify model # on TechPowerUp before bidding next time |
| Mined card thermals high | Pads dried out | Replace thermal pads + paste (~$30 + 2 hr) |

---

## 10 · References

- `tools/video-gen.md` — model VRAM tiers + LTX-Video runbook
- `~/ComfyUI/SETUP_NOTES.md` — full ComfyUI install notes
- `pipeline/broll.py` — LTX-Video B-roll runner
- TechPowerUp GPU database — `techpowerup.com/gpu-specs` — verify
  any card model before buying surplus
- pcpartpicker.com — sanity-check PSU + case compatibility

---

## 11 · Handoff prompt for a fresh Claude session

Paste this into a new chat along with the file:

> Read `tools/gpu-setup-checklist.md` for the full spec. I'm
> setting up a local or rented GPU for AI workloads (image
> generation, video generation, LLM inference — confirm with me
> which). Ask me the 7 pre-purchase questions in §1, then guide
> me through either buying a card (§3 — including the surplus
> auction path in §3.7) or spinning up a rental (§4), based on
> my answers. Set up the deal-hunting workflow in §6 if I'm
> buying. End-to-end success = the verification block in §8 all
> passes.

---

## 12 · What the assistant cannot do

To be explicit: an assistant following this checklist **cannot**:

- Place a purchase on the user's behalf — payment, address,
  account login, and per-purchase authorization belong to the
  user.
- Install Chrome extensions remotely — user does this in their
  own browser.
- Bid in real auctions on the user's behalf — same reason.
- Guarantee a particular surplus listing exists at the price
  shown — surplus prices vary widely and inventory turns weekly.

The assistant **can**:

- Walk through §1, recommend a tier from §3 / §4.
- Generate exact search queries for gsaauctions / govdeals /
  eBay tailored to the user's budget.
- Verify a model number against TechPowerUp.
- Execute the §7 install runbook over SSH on a GPU host the
  user has provisioned.
- Run §8 verification commands when the host is reachable.
