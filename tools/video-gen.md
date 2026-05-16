# Video generation tools

Open-source AI video models for B-roll. Manim still owns the diagram /
equation scenes; AI clips supply cinematic cutaways under VO.

## Preferred path (free, highest quality): Veo 3 via Google Vids

- Google's Veo 3 is currently the best video model in production
  (better than Higgsfield, Kling, Runway Gen-3, LTX-Video).
- **Free tier: 10 AI clips / month** via Google Vids — enough for one
  full episode's B-roll with margin.
- Per-episode runbook lives in `episodes/NNN/veo3-runbook.md`. It
  contains: (1) browser steps, (2) ready-to-paste prompts mapped to
  each Manim scene, (3) the 8-second-bypass trick for longer cuts,
  (4) the drop-in convention for outputs.
- **Runs in your own browser**, not the dev sandbox. `vids.google.com`,
  `workspace.google.com`, `gemini.google.com`, `labs.google` are all
  blocked at this sandbox's network boundary.

See `episodes/003-hormuz/veo3-runbook.md` for the worked example.

## Fallback (self-hosted, paid GPU time): LTX-Video

- Repo: `https://github.com/Lightricks/LTX-Video` — vendored at
  `tools/LTX-Video/` as a submodule.
- Closest open-source match to Veo 3 / Kling. DiT architecture.
  Apache 2.0.
- Use when: you've blown the Veo 3 free quota, or want full local
  control without depending on Google.
- Two model sizes:
  - **`ltxv-13b-0.9.8-distilled`** — 24–32 GB VRAM. Good default.
  - **`ltxv-13b-0.9.8-dev`** — 48 GB+ VRAM. Best quality.
- All configs in `tools/LTX-Video/configs/`.

## Other alternates (not vendored)

| Model | Repo | VRAM | When |
|---|---|---|---|
| CogVideoX-5B | `THUDM/CogVideo` | 24 GB | Quick ambient, lower fidelity |
| HunyuanVideo | `Tencent-Hunyuan/HunyuanVideo` | 60 GB+ | Hero shot worth an H100 hour |
| Mochi-1 | `genmoai/mochi` | 60 GB+ | Highest realism, slow |
| Wan 2.1 | `Wan-Video/Wan2.1` | 24–80 GB | Multi-aspect, alternative DiT |

## Workflow (wired)

```
episodes/NNN/veo3-runbook.md       ←  preferred: prompts for browser
episodes/NNN/broll-prompts.md      ←  fallback: prompts for LTX
pipeline/broll.py episodes/NNN/    ←  fallback runner (LTX)
episodes/NNN/broll/<scene>.mp4     ←  output from either path
episodes/NNN/scene.py              ←  composites clips as VideoMobject
                                       backgrounds at low opacity
```

Veo 3 path: paste prompts in browser, drop MP4s in `broll/`. Manual.
LTX path: one command on a GPU host. Scripted.

## Runbook — LTX-Video on a GPU host

### Option A — your own machine (24 GB+ GPU)

```bash
git clone <this-repo> && cd <repo>
git submodule update --init --recursive

# Set up LTX-Video env (one-time).
cd tools/LTX-Video
python -m pip install -e ".[inference]"
cd ../..

# Hugging Face login (one-time; model weights download lazily on first run).
huggingface-cli login

# Generate Hormuz B-roll.
python pipeline/broll.py episodes/003-hormuz/
```

### Option B — RunPod (rented GPU, ~$0.50–$2/hr)

1. Spin up a "PyTorch 2.x" pod on a 24 GB or 48 GB GPU (RTX A5000,
   A6000, or L40S). Choose the "Network Storage" option if you want
   to persist the model weights between runs.
2. SSH in; `git clone` this repo (and submodules).
3. Run the same `python pipeline/broll.py episodes/003-hormuz/`.
4. SCP the `episodes/003-hormuz/broll/*.mp4` back to your laptop.

### Option C — Modal (serverless, pay-per-second)

Write a Modal stub that wraps `pipeline/broll.py` and runs it on
an A100 / H100 image. Typical cost for the seven Hormuz clips:
under $5. (Stub not yet committed — write it when the workflow is
proven on Option A or B.)

## Trigger conditions for using AI B-roll

The Dossier's brand is **document-first**. AI B-roll is the
exception, not the rule. Use it only when:

1. The storyboard genuinely calls for a cutaway Manim primitives
   can't fake (e.g., aerial of a strait, underwater cable, empty
   night port). A typographic diagram is always cheaper, faster,
   and more on-brand.
2. The cutaway sits **behind** the typography at low opacity — the
   citations and source captions still own the foreground.
3. You have a usage budget — Veo 3 free is 10 clips/mo; LTX
   self-hosted is GPU time.

## Cost estimate (Hormuz episode, 7 clips)

| Path | Total cost | Time | Notes |
|---|---|---|---|
| **Veo 3 free tier** | $0 | ~10 min hands-on | 7 of 10 monthly credits |
| LTX-Video on RunPod H100 | ~$0.56 | ~10 min compute | $3.30/hr × ~10 min |
| LTX-Video on local 24 GB GPU | $0 (electricity) | ~30 min | distilled-13B preset |
| LTX-Video on Modal | <$5 | <10 min | serverless A100 |

