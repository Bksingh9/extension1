#!/usr/bin/env bash
# Render a Manim scene.
#
# Usage:
#   ./pipeline/render.sh <scene_file> <SceneName> [quality_flag]
#
# Examples:
#   ./pipeline/render.sh episodes/001-pilot/scene.py Hook -ql   # preview
#   ./pipeline/render.sh episodes/001-pilot/scene.py Hook       # 4K final (default)
#
# Each episode renders into its own <episode>/media/ tree so multiple
# episodes named scene.py do not collide.
set -euo pipefail

FILE="${1:?path to scene.py required}"
SCENE="${2:?scene class name required}"
QUALITY="${3:--qk}"   # default to 4K

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

EPISODE_DIR="$(cd "$(dirname "$FILE")" && pwd)"
MEDIA_DIR="$EPISODE_DIR/media"

PYTHONPATH="$ROOT" exec .venv/bin/manim \
  "$QUALITY" --media_dir "$MEDIA_DIR" "$FILE" "$SCENE"
