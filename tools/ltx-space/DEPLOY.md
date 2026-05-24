# Deploy this folder as a free ZeroGPU Space

Three ways. All free. Do this on your own machine (the dev sandbox
can't reach huggingface.co).

## Option A — HF web UI (no terminal)

1. Go to <https://huggingface.co/new-space>.
2. Owner = you · Space name = `ltx-video-generator` · SDK = **Gradio**
   · Hardware = **ZeroGPU** (free) · Visibility = your choice.
3. Create the Space, then **Files → Add file → Upload files** and
   drop in `app.py`, `requirements.txt`, `README.md` from this folder.
4. Wait for the build (a few minutes). When it says "Running", open
   the Space URL and generate.

## Option B — git push

```bash
pip install huggingface_hub
huggingface-cli login                     # paste your HF token

# create the Space (one time)
huggingface-cli repo create ltx-video-generator --type space --space_sdk gradio

# push the three files
git clone https://huggingface.co/spaces/<your-username>/ltx-video-generator
cp tools/ltx-space/{app.py,requirements.txt,README.md} ltx-video-generator/
cd ltx-video-generator
git add app.py requirements.txt README.md
git commit -m "LTX-Video ZeroGPU space"
git push
```

Then in the Space **Settings → Hardware**, select **ZeroGPU** (free).

## Option C — huggingface_hub from Python

```python
from huggingface_hub import HfApi
api = HfApi(token="hf_...")
repo_id = "<your-username>/ltx-video-generator"
api.create_repo(repo_id, repo_type="space", space_sdk="gradio", exist_ok=True)
for f in ("app.py", "requirements.txt", "README.md"):
    api.upload_file(path_or_fileobj=f"tools/ltx-space/{f}",
                    path_in_repo=f, repo_id=repo_id, repo_type="space")
# then set hardware to ZeroGPU in the Space settings UI
```

## Notes

- **ZeroGPU is free** but requires a (free) HF account; assign it in
  Space Settings → Hardware → ZeroGPU.
- First build downloads the LTX-Video weights (~9 GB) onto the Space —
  that's on HF's disk, not yours.
- If the model load OOMs the ZeroGPU allocation, lower resolution /
  frame count in `app.py`, or switch `MODEL_ID` to a distilled LTX
  checkpoint.
- To batch many prompts headlessly against your deployed Space, point
  the existing `tools/ai-gen/gen.py` at it:
  `python gen.py video --prompt "…" --space <your-username>/ltx-video-generator`.
