# GPU setup checklist — hand this to a fresh Claude session

> **Purpose.** Drop-in spec sheet for another Claude session (web,
> Code, or local) to guide the user through buying or renting a GPU
> for The Dossier's AI video pipeline and getting it running
> end-to-end. Self-contained: every fact, link, and verification
> command an agent needs is in this file.

---

## 0 · State of the world (what's already done)

- ✅ ComfyUI installed at `~/ComfyUI/` on a CPU-only sandbox box.
  Web UI verified (HTTP 200, port 8188, 922 node types).
- ✅ Custom nodes: ComfyUI-Manager, AnimateDiff-Evolved,
  VideoHelperSuite, Frame-Interpolation.
- ✅ Example workflow: `~/ComfyUI/workflows/text_to_video_sd15_animatediff.json`.
- ✅ LTX-Video submoduled at `tools/LTX-Video/`.
- ✅ Broll pipeline scaffold: `pipeline/broll.py` + `pipeline/veo3_browser.py`.
- ✅ Hormuz episode prompts: `episodes/003-hormuz/broll-prompts.md`
  and `episodes/003-hormuz/veo3-runbook.md`.
- ❌ **No GPU** on current sandbox (verified by `nvidia-smi`,
  `nvcc`, `torch.cuda.is_available()`).
- ❌ **No model weights** downloaded (huggingface.co blocked on
  current sandbox; must run on a normal-network host).

---

## 1 · Pre-purchase questions (ask the user first)

The right answer changes by use-case. Ask these in order:

| # | Question | If "yes / high" | If "no / low" |
|---|---|---|---|
| 1 | Will you use this GPU > 1 hr/day on average? | Lean toward owning | Lean toward renting |
| 2 | Will you train LoRAs (4–12 hr each)? | Own a 24 GB+ card | Rent is fine |
| 3 | Do you want full quality (LTX-dev tier)? | Need 48 GB | 24 GB enough |
| 4 | Will you also do image generation or fine-tuning? | Own justifies itself | Stick to rentals |
| 5 | Comfortable with used hardware? | Used 3090 is best $/VRAM | New 5090 or rent |
| 6 | Do you need offline / privacy? | Must own | Rent is fine |
| 7 | Budget cap? | Match tier to budget | — |

**Decision tree:**
- **All "no/low":** → §3 (cloud rental). Done.
- **#2 or #4 yes:** → §2 (buy a card). Pick by §1, §3, §5, §7.
- **#3 yes:** → §2 (RTX 6000 Ada, 48 GB).

---

## 2 · GPU shortlist (buying)

All prices are mid-2026 retail; verify before purchase.

### 2.1 Used RTX 3090 — 24 GB — $700–900 — **BEST $/VRAM**

| Spec | Value |
|---|---|
| Architecture | Ampere (GA102) |
| VRAM | 24 GB GDDR6X |
| TDP | 350 W |
| Power connectors | 2× 8-pin PCIe |
| Slot width | 3 slots |
| Length | ~313 mm (varies by AIB) |
| PCIe | Gen 4 x16 |
| Outputs | 1× HDMI 2.1, 3× DisplayPort 1.4a |

**Where to buy:** eBay, r/hardwareswap, r/buildapcsales, local
Facebook Marketplace. **Verify before paying**: ask for a stress
test screenshot (FurMark or 3DMark) showing no thermal throttling
above 83 °C, no artifacting at 1080p.

**Red flags to ask the seller about:**
- Was it used for mining? (Mined cards aren't doomed but lifespan
  shortened — accept only with proof of pads/paste re-do.)
- Memory junction temperature under load? (Should stay < 100 °C.)
- VBIOS modded? (Flashable, but adds work.)

### 2.2 RTX 5090 — 32 GB — $2,000–2,500 — **BEST NEW**

| Spec | Value |
|---|---|
| Architecture | Blackwell (GB202) |
| VRAM | 32 GB GDDR7 |
| TDP | 575 W |
| Power connector | 12V-2×6 (replaces 12VHPWR) |
| Slot width | 2.5–3.5 slots (varies) |
| Length | ~360 mm Founders Edition |
| PCIe | Gen 5 x16 |
| FP precision | FP4 + FP8 native |
| Outputs | 1× HDMI 2.1b, 3× DisplayPort 2.1b |

**Where to buy:** Nvidia.com (FE drops), Best Buy, B&H, Newegg.
Stock has stabilized as of mid-2026; expect MSRP availability.

**Bundle requirements** (often forgotten):
- 1000 W+ PSU with **native** 12V-2×6 cable (Seasonic Vertex GX,
  Corsair RM1000x Shift, Super Flower Leadex Platinum).
- Do NOT use adapters — they have melted on some 4090s.

### 2.3 RTX 6000 Ada — 48 GB — $7,500–9,000 — **WORKSTATION**

| Spec | Value |
|---|---|
| Architecture | Ada Lovelace (AD102) |
| VRAM | 48 GB GDDR6 ECC |
| TDP | 300 W |
| Power connector | 1× 16-pin (16-pin to 2× 8-pin adapter included) |
| Slot width | 2 slots blower |
| Length | 267 mm |
| PCIe | Gen 4 x16 |

Buy only if you'll run LTX-Video 13B dev tier or train LoRAs on
big datasets. Otherwise overspending vs §2.2.

### 2.4 Cards to skip

| Card | Why |
|---|---|
| RTX 4090 | Discontinued; 5090 is better. Used 4090 fine if cheap. |
| RTX 4080 / 4070 | 16 GB / 12 GB — insufficient for LTX-13B. |
| Any Mac Studio | MPS support for video gen is patchy as of 2026. |
| H100 / H200 | $25k+. Datacenter; overkill. |
| AMD RX 7900 XTX | 24 GB but ROCm support for video diffusion still flaky. |
| Intel Arc | Same — IPEX still spotty for newer models. |

---

## 3 · Cloud rental — the "don't buy" path

Cheaper for The Dossier's volume (~13 GPU-hr/year).

| Provider | GPU | $/hr | Setup time | Notes |
|---|---|---|---|---|
| **RunPod** | RTX A5000 24 GB | ~$0.34 | 2 min | Best default. PyTorch image. SSH + port-forward 8188. |
| RunPod | RTX 3090 24 GB | ~$0.30 | 2 min | Spot pricing, can be preempted. |
| RunPod | RTX 4090 24 GB | ~$0.69 | 2 min | Fastest 24 GB option. |
| RunPod | H100 80 GB | ~$3.30 | 2 min | For HunyuanVideo / large batches. |
| **Modal** | A100 40 GB | ~$0.0006/s | 0 min (serverless) | Pay per second. Best for one-off batches. |
| Vast.ai | varies | $0.20–0.80 | 5 min | Cheapest but variable quality. |
| Lambda Cloud | A100 / H100 | $1.10–2.50 | 5 min | Stable, reservation-friendly. |
| Colab Pro | T4 / L4 / A100 | $10/mo flat | 1 min | Notebook only; awkward for ComfyUI. |

**Recommended cloud combo:** RunPod RTX 3090 spot for development
iterations, Modal A100 serverless for the final episode render.

---

## 4 · System requirements (if buying)

| Item | 3090 spec | 5090 spec | Notes |
|---|---|---|---|
| PSU | 850 W 80+ Gold | 1000 W 80+ Gold + 12V-2×6 native | Seasonic / Corsair RMx / Super Flower |
| Case | 3-slot, 320 mm clearance | 3-slot, 360 mm clearance | Fractal Torrent, Lian Li O11, Phanteks Enthoo Pro |
| CPU | Any Ryzen 5 / Core i5 from 2020+ | Same | Inference is GPU-bound |
| RAM | 32 GB DDR4/DDR5 | 32 GB DDR5 | 64 GB if multiple models loaded at once |
| Storage | 2 TB NVMe Gen 4 | 2 TB NVMe Gen 4 or 5 | Models are 5–15 GB each; you'll fill it |
| Cooling | 3× 140 mm intake + GPU vent | Same + rear exhaust | These cards run hot |
| OS | Ubuntu 22.04 / 24.04 LTS | Same | NVIDIA driver ≥ 535 |
| Driver | NVIDIA Open Kernel Module 555+ | NVIDIA 570+ | Required for FP8 / FP4 on 5090 |
| Network | 100 Mbps down minimum | Same | Initial model pulls are 30 GB+ |

---

## 5 · Setup runbook (after GPU is in or pod is up)

### 5.1 Driver + CUDA verification
```bash
nvidia-smi                                # should show your card + driver version
python -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0))"
# expected: True, "NVIDIA GeForce RTX 3090" (or your card)
```

### 5.2 Clone this repo + sync submodule
```bash
git clone <repo-url> dossier
cd dossier
git submodule update --init --recursive
git checkout claude/setup-youtube-production-GYo4W  # the active dev branch
```

### 5.3 ComfyUI install (mirror what was done on the CPU sandbox)
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

### 5.4 Download models (the step that failed on the CPU sandbox)
```bash
.venv/bin/pip install huggingface_hub
huggingface-cli login         # paste your HF token (free, signup at huggingface.co)
cd models/checkpoints
huggingface-cli download stable-diffusion-v1-5/stable-diffusion-v1-5 \
  v1-5-pruned-emaonly.safetensors --local-dir .
cd ../animatediff_models
huggingface-cli download guoyww/animatediff mm_sd_v15_v2.ckpt --local-dir .
```

### 5.5 Launch ComfyUI
```bash
# Copy the launcher from the dossier repo:
cp <path-to-dossier-repo>/extension1/  # not needed if start.sh is already at ~/ComfyUI/
cd ~/ComfyUI && GPU=1 VRAM_GB=24 ./start.sh
# Visit http://127.0.0.1:8188/
# On RunPod: use the port-forwarding URL shown in the pod console.
```

### 5.6 Optional — set up LTX-Video for higher-quality clips
```bash
cd <path-to-dossier-repo>/tools/LTX-Video
pip install -e ".[inference]"
cd <dossier-repo-root>
python pipeline/broll.py episodes/003-hormuz/
# Outputs land in episodes/003-hormuz/broll/
```

---

## 6 · End-to-end verification

When all of the following pass, the user is done and can generate
B-roll for The Dossier:

```bash
# (a) GPU is visible to torch
python -c "import torch; assert torch.cuda.is_available(), 'no GPU'; print(torch.cuda.get_device_name(0))"

# (b) ComfyUI HTTP up
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8188/   # expect 200

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

# (e) Example workflow runs end-to-end
# In browser: File → Open → workflows/text_to_video_sd15_animatediff.json
# → Queue Prompt → expect a 2-second mp4 in ~30s on a 3090, ~15s on a 5090.
```

---

## 7 · If anything fails

| Symptom | Likely cause | Fix |
|---|---|---|
| `torch.cuda.is_available() == False` | No GPU / driver / wrong torch wheel | `nvidia-smi`; reinstall torch from `pytorch.org/get-started` with the matching CUDA |
| ComfyUI port 8188 not responding | Process crashed or bound to a different host | `pkill -f "python main.py"`; check `~/ComfyUI/start.log` |
| `Model not found` in UI | Models not in `models/checkpoints/` | Re-run §5.4 |
| `OutOfMemoryError` mid-generation | Model too big for VRAM | Lower resolution / frames; use `--lowvram` |
| Custom node import error | Missing Python dep | `cd custom_nodes/<node>; ../../.venv/bin/pip install -r requirements.txt` |
| RunPod pod preempted | Spot instance lost | Switch to on-demand pricing or use Modal serverless |
| 12V-2×6 connector hot | Adapter or under-seated cable | Use native cable; reseat fully; replace if any discolouration |
| Driver kernel error on boot | Secure Boot blocking unsigned module | Disable Secure Boot or sign the NVIDIA module |

---

## 8 · References

- `tools/video-gen.md` — model VRAM tiers + LTX-Video runbook
- `~/ComfyUI/SETUP_NOTES.md` — full ComfyUI install notes
- `pipeline/broll.py` — LTX-Video B-roll runner
- `pipeline/veo3_browser.py` — alternative path via Google Vids
- `episodes/003-hormuz/broll-prompts.md` — example prompt set
- `episodes/003-hormuz/veo3-runbook.md` — manual Veo 3 workflow

---

## 9 · Handoff prompt for the next Claude session

Paste this into a fresh Claude conversation along with this file:

> I'm setting up a local or rented GPU to run the AI video B-roll
> pipeline for my YouTube channel **The Dossier** (faceless,
> document-first geopolitics). Read `tools/gpu-setup-checklist.md`
> for the full spec. Ask me the 7 pre-purchase questions in §1
> first, then guide me through either buying a card or spinning
> up a RunPod based on my answers. End-to-end success = the
> verification block in §6 all passes and one Hormuz B-roll clip
> generates from `episodes/003-hormuz/broll-prompts.md`.
