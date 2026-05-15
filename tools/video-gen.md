# Video generation tools

Open-source AI video models for B-roll. Manim still owns the diagram /
equation scenes; AI clips supply cinematic cutaways under VO.

## Primary: LTX-Video (wired in)

- Repo: `https://github.com/Lightricks/LTX-Video` — vendored at
  `tools/LTX-Video/` as a submodule.
- Closest open-source match to **Higgsfield / Kling / Runway Gen-3**
  in cinematic quality + speed. DiT architecture. Apache 2.0.
- Two model sizes:
  - **`ltxv-13b-0.9.8-distilled`** — 24–32 GB VRAM. Good default.
  - **`ltxv-13b-0.9.8-dev`** — 48 GB+ VRAM. Best quality.
- All configs in `tools/LTX-Video/configs/`.

## Alternates (not vendored)

| Model | Repo | VRAM | When |
|---|---|---|---|
| CogVideoX-5B | `THUDM/CogVideo` | 24 GB | Quick ambient, lower fidelity |
| HunyuanVideo | `Tencent-Hunyuan/HunyuanVideo` | 60 GB+ | Hero shot worth an H100 hour |
| Mochi-1 | `genmoai/mochi` | 60 GB+ | Highest realism, slow |
| Wan 2.1 | `Wan-Video/Wan2.1` | 24–80 GB | Multi-aspect, alternative DiT |

## Workflow (wired)

```
episodes/NNN/broll-prompts.md      ←  one block per cinematic cutaway
pipeline/broll.py episodes/NNN/    ←  generates the clips
episodes/NNN/broll/<scene>.mp4     ←  output, gitignored
episodes/NNN/scene.py              ←  composites clips as VideoMobject
                                       backgrounds at low opacity
```

Each `broll-prompts.md` block has the form:

```
## <SceneName> · <seconds>s · <W>x<H>
<prompt body>
```

`SceneName` must match the Manim Scene class so the clip composites
into the right scene.

## Runbook — running on a GPU host

This codebase **cannot** generate clips from the original development
sandbox: the network blocks Hugging Face, Replicate, Runway, Pixabay,
Pexels, Higgsfield, and every other AI-video service. Inference runs
elsewhere. Three reasonable hosts:

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
3. You have a usage budget — model weight downloads are ~30 GB each
   and cloud GPU time is metered.

## Cost estimate (Hormuz episode, 7 clips)

| Clip | Seconds | Approx. time on H100 | Approx. cost |
|---|---|---|---|
| Hook | 5 | 90 s | $0.08 |
| Chokepoint | 4 | 75 s | $0.07 |
| Cables | 5 | 90 s | $0.08 |
| Closure | 6 | 110 s | $0.10 |
| Pipelines | 4 | 75 s | $0.07 |
| Successor | 5 | 90 s | $0.08 |
| Filed | 5 | 90 s | $0.08 |
| **Total** | **34 s** | **~10 min** | **~$0.56** |

Estimates assume RunPod H100 at ~$3.30/hr and the distilled-13B
model. Real timings vary ±2× depending on prompt complexity.
