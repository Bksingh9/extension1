# ai-gen — free batch HF Spaces video + image generator

Drives Hugging Face ZeroGPU Spaces (LTX-Video, Wan, Flux) over
`gradio_client`. No local GPU. No payment. Free HF account quota.

## ⚠️ Where this runs

**Not from this dev sandbox.** This repo's sandbox firewalls
`huggingface.co` and `*.hf.space` (verified 403 host_not_allowed
on every endpoint). Run this on a host with normal egress:

- Your own laptop (any OS with Python 3.10/3.11)
- GitHub Codespaces or Gitpod
- Oracle Cloud Free Tier VM
- Any VPS

## Setup

```bash
git clone <this-repo> && cd <repo>
chmod +x tools/ai-gen/setup.sh
./tools/ai-gen/setup.sh

# Edit ~/ai-gen/.env and paste your HF_TOKEN.
# (Get one at https://huggingface.co/settings/tokens — read scope is enough.)
```

The setup script:

- Creates `~/ai-gen/` and a Python venv inside it (uv if installed, else `python -m venv`)
- Installs `gradio_client`, `huggingface_hub`, `python-slugify`, `rich`, `pyyaml`, `httpx`, `tenacity`
- Copies the bundled `config/spaces.yaml` + `prompts/clips.txt`
- Writes `~/ai-gen/.env` (gitignored) for your HF token
- Symlinks `gen.py` to `~/ai-gen/gen.py`

It does **not**:

- Modify `~/.bashrc` or any shell rc
- Install anything globally
- Use sudo
- Touch HF until you run a subcommand

## Quick start

All commands run from anywhere; the script reads `~/ai-gen/`.

```bash
source ~/ai-gen/.venv/bin/activate
python ~/ai-gen/gen.py list-spaces
python ~/ai-gen/gen.py health
python ~/ai-gen/gen.py image --prompt "a red panda on a bicycle in tokyo, golden hour, cinematic" --space evalstate/flux1_schnell --n 1
python ~/ai-gen/gen.py video --prompt "a paper boat sailing on a calm lake at sunset" --space Lightricks/ltx-video-distilled
python ~/ai-gen/gen.py batch --file ~/ai-gen/prompts/clips.txt --kind video --space auto
```

## Subcommands

| Command | What it does |
|---|---|
| `image --prompt "…" --space <id> --n N` | N images via Flux/etc., saves to `~/ai-gen/outputs/<date>/` |
| `video --prompt "…" --space <id> --n N` | N video clips |
| `batch --file path --kind {image\|video} --space auto` | One run per non-comment line in the prompts file; `auto` picks first healthy Space from `spaces.yaml` |
| `list-spaces` | Pretty table of configured Spaces |
| `probe <space_id>` | Calls `Client.view_api()` and prints the discovered function name, prompt arg, seed arg, default extras. Cached to `config/<id>.json`. |
| `health` | Pings every Space + your HF whoami + ZeroGPU quota note |

Common flags:

- `--tag NAME` — prefix on output filenames (e.g. `hormuz_`)
- `--space auto` — try the first healthy Space from `spaces.yaml`; retries the next on error (max 3)

## Output convention

```
~/ai-gen/outputs/<YYYY-MM-DD>/<idx>_<slug>_<j>.<ext>
~/ai-gen/logs/runs.csv
```

`runs.csv` columns: `ts · space · prompt · seed · duration_sec · output_path · status`

## Adding a Space

Edit `~/ai-gen/config/spaces.yaml`:

```yaml
video:
  - id: my-user/my-video-space
    note: optional free-text
```

Then probe it once to cache the API schema:

```bash
python ~/ai-gen/gen.py probe my-user/my-video-space
```

That writes `~/ai-gen/config/my-user__my-video-space.json` with the
discovered function name and parameter mapping. Edit by hand if the
heuristics picked the wrong fields — `prompt_arg`, `seed_arg`,
`neg_arg`, and `extras` are all overridable.

## Adding a new "kind" (e.g. image-to-video)

1. In `spaces.yaml`, add a new top-level key:

   ```yaml
   image_to_video:
     - id: ...
   ```

2. In `gen.py`, the `cmd_batch` and `resolve_space` flow already
   parameterises on `--kind`, so just pass `--kind image_to_video`.
   For a new dedicated CLI subcommand, add a parser mirroring `cmd_video`.

3. For an image-to-video Space, the schema picker will likely find
   both a `prompt` arg and an `image` arg. Use the probe cache to
   add an `extras` entry pointing at a default image path, or call
   `client.predict()` directly with the right args.

## Free-quota notes

- ZeroGPU is free for **all HF users with a verified email**. As of
  2026 the daily ZeroGPU compute budget is **5 min/day per anonymous
  user** and **higher for signed-in users** (varies by Space; each
  Space declares its own cost).
- Some Spaces (e.g. `black-forest-labs/FLUX.1-dev`) are gated —
  click "Agree and access" on the model card once with your HF
  account before the Space will accept your token.
- Queue time depends on Space popularity. `--space auto` rotates
  through the list in `spaces.yaml` so you don't get stuck on a
  slow one.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `KeyError: 'prompt_arg'` | Heuristic missed the prompt parameter | `gen.py probe <space>` then edit the cached `config/<id>.json` |
| `Queue is full` / 503 | Space is overloaded | `--space auto` retries the next candidate |
| `gated_repo` 403 | Model needs licence acceptance | Visit the model card on HF, click "Agree" once |
| `Invalid token` | HF_TOKEN missing or wrong scope | Re-paste from https://huggingface.co/settings/tokens (read scope) |
| Output saved but is 0 bytes | Space returned a placeholder | Check `runs.csv`, re-run with a different seed |
| `gradio_client` import error | Setup didn't activate the venv | `source ~/ai-gen/.venv/bin/activate` |

## What's NOT installed

By design, this tool stays small:

- No ComfyUI (use `tools/setup-comfyui-stack.sh` instead if you want local control)
- No PyTorch / model weights
- No paid APIs
- No global Python deps

## File layout

```
~/ai-gen/
├── .venv/                      # project Python env (gitignored)
├── .env                        # HF_TOKEN (gitignored)
├── gen.py                      # symlink to tools/ai-gen/gen.py
├── config/
│   ├── spaces.yaml             # Space list (kind → [id, note])
│   └── <user>__<space>.json    # cached API schemas, one per Space
├── prompts/
│   └── clips.txt               # batch prompts (one per line, # = comment)
├── outputs/
│   └── YYYY-MM-DD/             # generated files
└── logs/
    └── runs.csv                # every run, every status
```
