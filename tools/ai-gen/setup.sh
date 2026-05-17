#!/usr/bin/env bash
# setup.sh — bootstrap ~/ai-gen for the free batch HF Spaces generator.
#
# - Creates the project venv (uv if available, else python -m venv).
# - Installs deps INSIDE the venv (never globally).
# - Copies bundled config/spaces.yaml + prompts/clips.txt into ~/ai-gen/.
# - Drops a .env template alongside (gitignored).
# - Does NOT touch ~/.bashrc, never sudos.
set -euo pipefail

ROOT="${AI_GEN_ROOT:-$HOME/ai-gen}"
HERE="$(cd "$(dirname "$0")" && pwd)"

echo "→ project root: $ROOT"
mkdir -p "$ROOT"/{config,prompts,logs,outputs}

# venv
if command -v uv >/dev/null 2>&1; then
  echo "→ creating venv with uv"
  uv venv "$ROOT/.venv" --python 3.11 >/dev/null
else
  echo "→ creating venv with python3"
  python3 -m venv "$ROOT/.venv"
fi
# shellcheck disable=SC1091
. "$ROOT/.venv/bin/activate"
python -m pip install --quiet --upgrade pip
python -m pip install --quiet \
  gradio_client huggingface_hub python-slugify rich pyyaml httpx tenacity

# config + prompts
[ -f "$ROOT/config/spaces.yaml" ] || cp "$HERE/config/spaces.yaml" "$ROOT/config/spaces.yaml"
[ -f "$ROOT/prompts/clips.txt"  ] || cp "$HERE/prompts/clips.txt"  "$ROOT/prompts/clips.txt"

# .env template (gitignored)
if [ ! -f "$ROOT/.env" ]; then
  cat > "$ROOT/.env" <<'EOF'
# Hugging Face token — read-scope is enough.
# Get one at https://huggingface.co/settings/tokens
HF_TOKEN=
EOF
  echo "→ wrote $ROOT/.env (fill in HF_TOKEN, the file is gitignored)"
fi

# Symlink gen.py inside the project for convenience
ln -sf "$HERE/gen.py" "$ROOT/gen.py"

echo
echo "✅ done. Next:"
echo "    edit $ROOT/.env and paste your HF_TOKEN"
echo "    $ROOT/.venv/bin/python $ROOT/gen.py list-spaces"
echo "    $ROOT/.venv/bin/python $ROOT/gen.py health"
echo "    $ROOT/.venv/bin/python $ROOT/gen.py image --prompt 'a red panda on a bicycle in tokyo, golden hour, cinematic' --space evalstate/flux1_schnell --n 1"
echo "    $ROOT/.venv/bin/python $ROOT/gen.py video --prompt 'a paper boat sailing on a calm lake at sunset' --space Lightricks/ltx-video-distilled"
echo "    $ROOT/.venv/bin/python $ROOT/gen.py batch --file $ROOT/prompts/clips.txt --kind video --space auto"
