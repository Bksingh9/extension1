#!/usr/bin/env bash
# setup-comfyui-stack.sh — install ComfyUI + LTX-Video + Flux.1-schnell
#
# Mirrors the spec the user pasted in chat. Steps 1–9. Each major step
# prints a status line and waits for "ok" (press ENTER) before
# continuing. Use --yes to skip confirmations.
#
# Run on YOUR machine (Ubuntu/Debian/macOS or WSL2). NOT on the dev
# sandbox — that has no GPU and no Hugging Face access. See
# tools/gpu-setup-checklist.md if you haven't picked a GPU host yet.

set -euo pipefail

# ── flags ───────────────────────────────────────────────────────────
AUTO_YES=0
REMOTE_HOST=0
ROOT="${AI_VIDEO_ROOT:-$HOME/ai-video}"
for a in "$@"; do
  case "$a" in
    --yes|-y) AUTO_YES=1 ;;
    --remote) REMOTE_HOST=1 ;;
    --root=*) ROOT="${a#--root=}" ;;
    -h|--help)
      sed -n '1,15p' "$0"; exit 0 ;;
  esac
done

# ── helpers ─────────────────────────────────────────────────────────
hr()    { printf '\n%s\n' "──────────────────────────────────────────────"; }
ok()    { printf '✅ %s\n' "$*"; }
warn()  { printf '⚠️  %s\n' "$*" >&2; }
die()   { printf '❌ %s\n' "$*" >&2; exit 1; }
step()  { hr; printf '🔹 STEP %s\n' "$*"; }
ask()   {
  if [ "$AUTO_YES" = 1 ]; then return 0; fi
  printf '\n%s\nType ok to continue, anything else to abort: ' "$1"
  read -r reply
  [ "$reply" = "ok" ] || die "aborted at: $1"
}

# ── STEP 1 · system check ───────────────────────────────────────────
step "1 · system check"

OS="$(uname -s)"
case "$OS" in
  Linux)   OS_NAME="$(. /etc/os-release 2>/dev/null && echo "$PRETTY_NAME" || echo Linux)" ;;
  Darwin)  OS_NAME="macOS $(sw_vers -productVersion 2>/dev/null)" ;;
  *)       die "unsupported OS: $OS (use WSL2 on Windows)" ;;
esac
echo "OS:         $OS_NAME"

if ! command -v nvidia-smi >/dev/null 2>&1; then
  die "no nvidia-smi found — this spec requires an NVIDIA GPU. See tools/gpu-setup-checklist.md"
fi
GPU_NAME=$(nvidia-smi --query-gpu=name --format=csv,noheader | head -1)
VRAM_MB=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits | head -1)
DRIVER=$(nvidia-smi --query-gpu=driver_version --format=csv,noheader | head -1)
CUDA_DRV=$(nvidia-smi | awk -F'CUDA Version: ' '/CUDA Version/{print $2}' | awk '{print $1}' | head -1)
VRAM_GB=$(( VRAM_MB / 1024 ))
echo "GPU:        $GPU_NAME (${VRAM_GB} GB VRAM)"
echo "Driver:     $DRIVER · CUDA $CUDA_DRV"

if command -v nvcc >/dev/null 2>&1; then
  echo "nvcc:       $(nvcc --version | tail -1)"
else
  echo "nvcc:       not installed (fine — PyTorch ships its own CUDA)"
fi

PY_VER=$(python3 -c 'import sys; print("%d.%d.%d" % sys.version_info[:3])' 2>/dev/null || echo "")
if [ -z "$PY_VER" ] || [[ ! "$PY_VER" =~ ^3\.(10|11|12)\. ]]; then
  die "Python 3.10/3.11/3.12 required, found '${PY_VER:-none}'. Install via pyenv or uv."
fi
echo "Python:     $PY_VER"

FREE_GB=$(df -BG "$HOME" | awk 'NR==2{gsub("G","",$4); print $4}')
echo "Free disk:  ${FREE_GB} GB"
if [ "$FREE_GB" -lt 80 ]; then
  warn "free disk ${FREE_GB} GB is less than the 80 GB the spec asked for."
fi

# pick CUDA wheel index
case "$CUDA_DRV" in
  12.1*|12.2*) TORCH_INDEX="https://download.pytorch.org/whl/cu121" ;;
  12.4*)       TORCH_INDEX="https://download.pytorch.org/whl/cu124" ;;
  12.5*|12.6*|12.7*|12.8*|12.9*|13.*) TORCH_INDEX="https://download.pytorch.org/whl/cu124" ;;
  *) warn "unknown CUDA driver version '$CUDA_DRV' — defaulting to cu121."; TORCH_INDEX="https://download.pytorch.org/whl/cu121" ;;
esac
echo "Torch index: $TORCH_INDEX"

# VRAM warning
GGUF_ONLY=0
if [ "$VRAM_GB" -lt 12 ]; then
  warn "GPU VRAM is ${VRAM_GB} GB — below 12 GB. LTX-Video full + Flux fp8 will not fit."
  warn "Recommended path: GGUF quantized only (Flux GGUF + LTX-Video GGUF when available)."
  ask "Proceed in GGUF-only mode? (skips full fp8 model downloads)"
  GGUF_ONLY=1
fi

ok "STEP 1 complete"
ask "STEP 1 ok?"

# ── STEP 2 · project + venv ─────────────────────────────────────────
step "2 · project + venv at $ROOT"
mkdir -p "$ROOT"
cd "$ROOT"

if command -v uv >/dev/null 2>&1; then
  echo "using uv"
  uv venv .venv --python 3.11 >/dev/null
else
  echo "using python -m venv (uv not installed)"
  python3 -m venv .venv
fi
# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install --quiet --upgrade pip
ok "venv at $ROOT/.venv  · Python $(python --version | awk '{print $2}')"
ask "STEP 2 ok?"

# ── STEP 3 · ComfyUI + PyTorch ──────────────────────────────────────
step "3 · ComfyUI + PyTorch ($TORCH_INDEX)"
if [ ! -d "$ROOT/ComfyUI" ]; then
  git clone --depth 1 https://github.com/comfyanonymous/ComfyUI.git "$ROOT/ComfyUI"
fi
cd "$ROOT/ComfyUI"

pip install --upgrade --index-url "$TORCH_INDEX" torch torchvision torchaudio
pip install -r requirements.txt

python -c "import torch; assert torch.cuda.is_available(), 'CUDA not available after install'; print('torch', torch.__version__, '· cuda OK ·', torch.cuda.get_device_name(0))"
python main.py --help >/dev/null && ok "main.py --help runs"
ask "STEP 3 ok?"

# ── STEP 4 · ComfyUI-Manager ────────────────────────────────────────
step "4 · ComfyUI-Manager"
mkdir -p custom_nodes
cd custom_nodes
[ -d ComfyUI-Manager ] || git clone --depth 1 https://github.com/ltdrdata/ComfyUI-Manager.git
[ -f ComfyUI-Manager/requirements.txt ] && pip install -r ComfyUI-Manager/requirements.txt
ok "Manager installed"
ask "STEP 4 ok?"

# ── STEP 5 · GGUF + video custom nodes ──────────────────────────────
step "5 · GGUF + video custom nodes"
# Picked Lightricks/ComfyUI-LTXVideo — it's the official node from
# the model authors, first-party support for new LTX model drops,
# and currently the most active LTX-Video node. Swap to a kijai
# fork later if you want alternative samplers.
NODES=(
  "city96/ComfyUI-GGUF"
  "Lightricks/ComfyUI-LTXVideo"
  "kijai/ComfyUI-KJNodes"
  "Fannovel16/ComfyUI-Frame-Interpolation"
)
for n in "${NODES[@]}"; do
  name="${n##*/}"
  if [ ! -d "$name" ]; then
    git clone --depth 1 "https://github.com/$n.git"
  fi
  if [ -f "$name/requirements.txt" ]; then
    pip install -r "$name/requirements.txt"
  fi
done
ok "custom nodes installed: ${NODES[*]##*/}"
ask "STEP 5 ok?"

# ── STEP 6 · model downloads ────────────────────────────────────────
step "6 · model downloads (list first, then confirm)"
cd "$ROOT/ComfyUI"
mkdir -p models/{checkpoints,text_encoders,unet,vae,clip,loras}

pip install --quiet "huggingface_hub[cli]"

# Prompt for HF token if not already set
if [ -z "${HF_TOKEN:-}" ] && ! huggingface-cli whoami >/dev/null 2>&1; then
  echo
  echo "Paste your Hugging Face token (read access is fine):"
  echo "(create one at https://huggingface.co/settings/tokens)"
  read -rs HF_TOKEN
  echo
  export HF_TOKEN
fi
[ -n "${HF_TOKEN:-}" ] && huggingface-cli login --token "$HF_TOKEN" --add-to-git-credential 2>/dev/null || true

# Manifest: repo · filename · destination · approx size
declare -a MANIFEST
if [ "$GGUF_ONLY" = 0 ]; then
  MANIFEST+=(
    "Lightricks/LTX-Video|ltx-video-2b-v0.9.5.safetensors|models/checkpoints|~9 GB"
    "Lightricks/LTX-Video|text_encoders/t5xxl_fp16.safetensors|models/text_encoders|~9.8 GB"
  )
fi
MANIFEST+=(
  "city96/FLUX.1-schnell-gguf|flux1-schnell-Q4_K_S.gguf|models/unet|~6.8 GB"
  "black-forest-labs/FLUX.1-schnell|ae.safetensors|models/vae|~335 MB"
  "comfyanonymous/flux_text_encoders|clip_l.safetensors|models/clip|~246 MB"
  "comfyanonymous/flux_text_encoders|t5xxl_fp8_e4m3fn.safetensors|models/clip|~4.9 GB"
)

echo
echo "Planned downloads:"
for m in "${MANIFEST[@]}"; do
  IFS='|' read -r repo file dst size <<<"$m"
  printf "  %-50s  %-25s  %s\n" "$repo / $file" "→ $dst" "$size"
done
echo
ask "Approve all downloads above?"

for m in "${MANIFEST[@]}"; do
  IFS='|' read -r repo file dst size <<<"$m"
  out="$ROOT/ComfyUI/$dst/$(basename "$file")"
  if [ -f "$out" ]; then
    echo "skip: $out exists"
    continue
  fi
  echo "↓ $repo / $file → $dst ($size)"
  huggingface-cli download "$repo" "$file" --local-dir "$ROOT/ComfyUI/$dst" --local-dir-use-symlinks False
done

ok "models downloaded"
ask "STEP 6 ok?"

# ── STEP 7 · workflows ──────────────────────────────────────────────
step "7 · example workflows"
mkdir -p "$ROOT/workflows"
# Pull from the official Lightricks examples folder
cd /tmp && rm -rf ltx-workflows && git clone --depth 1 \
  https://github.com/Lightricks/ComfyUI-LTXVideo.git ltx-workflows 2>/dev/null || true
if [ -d /tmp/ltx-workflows/example_workflows ]; then
  cp /tmp/ltx-workflows/example_workflows/*.json "$ROOT/workflows/" 2>/dev/null || true
fi
# Flux schnell workflow ships with ComfyUI's frontend templates
FLUX_TPL=$(find "$ROOT/ComfyUI/.venv" "$ROOT/ComfyUI" -name "flux_schnell*.json" 2>/dev/null | head -1)
[ -n "$FLUX_TPL" ] && cp "$FLUX_TPL" "$ROOT/workflows/flux_schnell_t2i.json"

ls "$ROOT/workflows/" | sed 's/^/  · /'
ok "workflows copied to $ROOT/workflows/"
ask "STEP 7 ok?"

# ── STEP 8 · launch ─────────────────────────────────────────────────
step "8 · launch ComfyUI"
cd "$ROOT/ComfyUI"

if [ "$REMOTE_HOST" = 1 ]; then
  HOST=0.0.0.0
  echo
  echo "Launching bound to 0.0.0.0:8188 (remote mode)."
  echo "On your local laptop, run this to tunnel:"
  USER_HOST="${USER}@$(hostname -I 2>/dev/null | awk '{print $1}')"
  printf '\n  ssh -L 8188:localhost:8188 %s\n\n' "$USER_HOST"
else
  HOST=127.0.0.1
fi

cat > "$ROOT/start-comfyui.sh" <<EOF
#!/usr/bin/env bash
set -e
cd "$ROOT/ComfyUI"
source "$ROOT/.venv/bin/activate"
exec python main.py --listen $HOST --port 8188 "\$@"
EOF
chmod +x "$ROOT/start-comfyui.sh"

echo "launcher: $ROOT/start-comfyui.sh"
echo "starting in background → log: $ROOT/comfyui.log"
nohup "$ROOT/start-comfyui.sh" > "$ROOT/comfyui.log" 2>&1 &
COMFY_PID=$!
echo "PID: $COMFY_PID"

for i in $(seq 1 30); do
  if curl -s -o /dev/null -m 3 http://127.0.0.1:8188/; then ok "UI up after ${i}x2s"; break; fi
  sleep 2
done
echo
echo "🌐 http://$HOST:8188/"
[ "$REMOTE_HOST" = 1 ] && echo "🌐 tunneled: http://127.0.0.1:8188/  (after running the ssh -L command above)"
ask "STEP 8 ok? (UI reachable?)"

# ── STEP 9 · smoke tests ────────────────────────────────────────────
step "9 · smoke tests"
mkdir -p "$ROOT/outputs"
cd "$ROOT"

echo "running Flux schnell smoke test…"
python "$(dirname "$0")/batch.py" --workflow flux \
  --prompts-text "a red panda riding a bicycle in tokyo, cinematic, golden hour" \
  --out "$ROOT/outputs" --runs-csv "$ROOT/runs.csv" --tag smoke_flux \
  || warn "Flux smoke test failed — check $ROOT/comfyui.log"

echo "running LTX-Video T2V smoke test…"
python "$(dirname "$0")/batch.py" --workflow ltx \
  --prompts-text "a paper boat sailing on a calm lake, soft sunset light, gentle ripples" \
  --out "$ROOT/outputs" --runs-csv "$ROOT/runs.csv" --tag smoke_ltx \
  || warn "LTX smoke test failed — check $ROOT/comfyui.log"

ls -lh "$ROOT/outputs" | tail -5
ok "smoke tests complete · see $ROOT/runs.csv"

hr
echo "🎉 done. Quick reference:"
echo "  start UI:   $ROOT/start-comfyui.sh"
echo "  batch gen:  python $(dirname "$0")/batch.py --prompts $ROOT/prompts.txt --out $ROOT/outputs"
echo "  models:     $ROOT/ComfyUI/models/"
echo "  workflows:  $ROOT/workflows/"
echo "  README:     $ROOT/README.md  (will be generated next; see tools/setup-comfyui-stack.sh)"
echo "  total disk: $(du -sh "$ROOT" | cut -f1)"
