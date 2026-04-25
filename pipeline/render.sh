#!/usr/bin/env bash
# Render a Manim scene.
#
# Usage:
#   ./pipeline/render.sh <scene_file> <SceneName> [quality_flag]
#
# Examples:
#   ./pipeline/render.sh episodes/001-pilot/scene.py Hook -ql   # preview
#   ./pipeline/render.sh episodes/001-pilot/scene.py Hook       # 4K final (default)
set -euo pipefail

FILE="${1:?path to scene.py required}"
SCENE="${2:?scene class name required}"
QUALITY="${3:--qk}"   # default to 4K

# Run from repo root so manim.cfg and shared/ resolve correctly.
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

PYTHONPATH="$ROOT" exec manim "$QUALITY" "$FILE" "$SCENE"
