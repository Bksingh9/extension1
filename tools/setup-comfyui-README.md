# ComfyUI stack setup — run on your own GPU machine

End-to-end installer for ComfyUI + LTX-Video (text-to-video,
image-to-video) + Flux.1-schnell (text-to-image) + volume
generation. Matches the spec the user pasted, including the
"pause and confirm at every major step" requirement.

## What you need before running

- Linux (Ubuntu/Debian) or macOS. Windows: WSL2 Ubuntu.
- **NVIDIA GPU, ≥ 12 GB VRAM**, driver supporting CUDA 12.1+.
- Python 3.10 / 3.11 / 3.12.
- ~80 GB free disk.
- A Hugging Face account (free). Get a read-token at
  <https://huggingface.co/settings/tokens>.

The script refuses to run without an NVIDIA GPU (per spec).

## One-line install

```bash
git clone <this-repo> dossier
cd dossier
chmod +x tools/setup-comfyui-stack.sh
./tools/setup-comfyui-stack.sh                # local box
./tools/setup-comfyui-stack.sh --remote       # remote GPU host
./tools/setup-comfyui-stack.sh --yes          # skip confirmations
./tools/setup-comfyui-stack.sh --root=/data/ai-video   # custom root
```

Steps 1–9 of the spec run in order. Each major step prints a
status line and waits for you to type `ok`. STEP 6 lists every
file to be downloaded (filename + size + source repo) and waits
for `ok` before pulling.

## What gets installed

| Path | What |
|---|---|
| `~/ai-video/.venv/` | Python venv (uv if installed, else `python -m venv`) |
| `~/ai-video/ComfyUI/` | ComfyUI core |
| `~/ai-video/ComfyUI/custom_nodes/ComfyUI-Manager` | Manager UI |
| `~/ai-video/ComfyUI/custom_nodes/ComfyUI-GGUF` | GGUF model loaders |
| `~/ai-video/ComfyUI/custom_nodes/ComfyUI-LTXVideo` | **Lightricks' official LTX-Video node** (picked over kijai's fork — first-party, kept current with model releases) |
| `~/ai-video/ComfyUI/custom_nodes/ComfyUI-KJNodes` | kijai's utility nodes |
| `~/ai-video/ComfyUI/custom_nodes/ComfyUI-Frame-Interpolation` | RIFE / FILM |
| `~/ai-video/ComfyUI/models/checkpoints/` | LTX-Video safetensors |
| `~/ai-video/ComfyUI/models/text_encoders/` | T5-XXL fp16 |
| `~/ai-video/ComfyUI/models/unet/` | Flux GGUF |
| `~/ai-video/ComfyUI/models/vae/` | Flux VAE |
| `~/ai-video/ComfyUI/models/clip/` | CLIP-L + T5-XXL fp8 |
| `~/ai-video/workflows/` | Example workflow JSONs |
| `~/ai-video/start-comfyui.sh` | Launcher |
| `~/ai-video/outputs/` | Generated images / videos |
| `~/ai-video/runs.csv` | Job log |
| `~/ai-video/comfyui.log` | ComfyUI server log |

Total disk after install: ~30–35 GB.

## After install: start / stop

```bash
~/ai-video/start-comfyui.sh                   # foreground
# UI: http://127.0.0.1:8188/  (local)
# or  http://0.0.0.0:8188/    (with --remote, plus the ssh -L tunnel printed at install)
```

To stop: Ctrl-C the foreground process, or `pkill -f "python main.py --listen"`.

## Volume generation with batch.py

```bash
# Default: LTX-Video text-to-video
echo "a paper boat sailing on a calm lake, soft sunset light, gentle ripples" >  ~/ai-video/prompts.txt
echo "a red panda riding a bicycle in tokyo, cinematic, golden hour"          >> ~/ai-video/prompts.txt
python tools/batch.py --prompts ~/ai-video/prompts.txt

# Flux text-to-image
python tools/batch.py --prompts ~/ai-video/prompts.txt --workflow flux

# Custom workflow JSON
python tools/batch.py --prompts ~/ai-video/prompts.txt --workflow /path/to/workflow.json

# Other flags
#   --seed N            fixed seed (default -1 = random per prompt)
#   --concurrency N     queues N at once (ComfyUI itself is serial)
#   --tag NAME          prefix on output filenames
#   --out DIR           override output directory
#   --runs-csv PATH     override job log location
```

Outputs land in `~/ai-video/outputs/<idx>_<slug>_<j><ext>`. Every
job appends a row to `~/ai-video/runs.csv` with timestamp, tag,
workflow, seed, prompt, duration, and saved paths.

## How batch.py picks the right nodes

When a workflow JSON has multiple `CLIPTextEncode` nodes, the
script keeps the negative prompt as-is and only mutates the
positive one (heuristic: lowest count of negative-prompt hints
in current text). For the seed, it sets whichever node has a
`seed` or `noise_seed` input — works for `KSampler`,
`KSamplerAdvanced`, `SamplerCustom`, and the LTX-Video sampler.
If your workflow doesn't fit this shape, point `--workflow` at
a path and the heuristics still apply, or open `batch.py` and
hard-code the node IDs.

## Adding new prompts

Append to `~/ai-video/prompts.txt`, one per line, lines starting
with `#` are skipped. Re-run `tools/batch.py --prompts ...`. The
script does **not** skip prompts you've run before — that's by
design, so you can re-roll the same prompt with a new seed.

## Adding more custom nodes

Two paths:

1. **Manager UI:** in ComfyUI's web UI, **Manager → Custom Nodes Manager → search → Install**.
2. **CLI:**
   ```bash
   cd ~/ai-video/ComfyUI/custom_nodes
   git clone --depth 1 <repo-url>
   cd <node-name>
   [ -f requirements.txt ] && ~/ai-video/.venv/bin/pip install -r requirements.txt
   # restart ComfyUI
   ```

## Troubleshooting

| Symptom | Fix |
|---|---|
| `nvidia-smi: not found` at STEP 1 | Install the NVIDIA driver matching your card. `sudo ubuntu-drivers autoinstall` on Ubuntu. |
| `torch.cuda.is_available() == False` after STEP 3 | Wrong torch wheel — the script picks cu121 / cu124 from `nvidia-smi`'s reported CUDA version. Reinstall manually if needed: `pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124` |
| HF 401 / 403 during STEP 6 | Your token doesn't have read access to the target repo. Some Lightricks models need you to accept the license on the model page first. |
| `OutOfMemoryError` during a workflow | VRAM too small. Either lower the resolution / number of frames in the workflow, or switch to the GGUF model variants in `~/ai-video/ComfyUI/models/unet/`. |
| `port 8188 already in use` | A previous ComfyUI is still running. `pkill -f "python main.py --listen"`. |
| `batch.py` errors with "no CLIPTextEncode node found" | The workflow JSON doesn't have a standard text-prompt node. Open it in the UI, find the prompt node, set it manually once, save back. |
| Remote box: can't reach the UI from your laptop | Need the SSH tunnel: `ssh -L 8188:localhost:8188 user@gpubox`. The install script prints the exact command when run with `--remote`. |

## Disk usage breakdown (approx)

| Item | Size |
|---|---|
| ComfyUI + custom nodes | ~250 MB |
| Python venv (torch + nvidia libs) | ~7 GB |
| LTX-Video 2B safetensors | ~9 GB |
| T5-XXL fp16 | ~9.8 GB |
| Flux schnell Q4_K_S GGUF | ~6.8 GB |
| Flux VAE | ~335 MB |
| CLIP-L | ~246 MB |
| T5-XXL fp8 | ~4.9 GB |
| **Total** | **~38 GB** |

Plus whatever you generate in `outputs/`.

## What this stack does NOT include

- AnimateDiff (SD-1.5-era T2V) — superseded by LTX-Video for this use case
- SDXL / SD-3 base models — install via Manager if you want them
- ControlNet — install via Manager when needed
- IPAdapter / Style transfer — same
- Audio (Stable Audio, Bark) — separate stack

Add any of those via ComfyUI-Manager from the UI when you need them.
