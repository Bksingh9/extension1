---
title: LTX Video Generator
emoji: 🎬
colorFrom: indigo
colorTo: purple
sdk: gradio
sdk_version: 5.9.1
app_file: app.py
pinned: false
license: apache-2.0
short_description: Open-source text-to-video on free ZeroGPU
suggested_hardware: zero-a10g
---

# LTX-Video Generator (ZeroGPU Space)

Open-source text-to-video, running as a Hugging Face Space on **free
ZeroGPU** hardware. No local GPU. No payment. A web UI you open in a
browser and can share.

This is the "create the videos like a Space" deliverable. The files
here ARE a deployable HF Space. See `DEPLOY.md` for the 5-minute push.

## Why this works when everything else was blocked

Every earlier attempt failed because generation tried to run from the
dev sandbox, which firewalls Hugging Face, GPUs, and external APIs.
A Space flips that around: **the code runs on HF's servers**, which
have the GPU and the model weights. You just open the URL.

## Files

| File | Purpose |
|---|---|
| `app.py` | Gradio app; `@spaces.GPU` grants a GPU per generation |
| `requirements.txt` | diffusers + torch + gradio + spaces |
| `README.md` | this file — the YAML frontmatter above configures the Space |
| `DEPLOY.md` | how to push to your own Space |

## Once deployed

Open your Space URL, type a prompt, press **Generate**, download the
MP4. Keep clips ≤ 5 s (≤ 121 frames) so each run fits the ZeroGPU
time budget. Free ZeroGPU quota refreshes daily.
