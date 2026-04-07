#!/bin/bash
# ═══════════════════════════════════════════════════════
# Piper TTS Narration Pipeline
# Generates AI voiceover for the Geo-Politics Documentary
# ═══════════════════════════════════════════════════════
#
# Prerequisites:
#   pip install piper-tts
#
# Available voices (en_US):
#   lessac-medium  — Professional narrator (recommended)
#   amy-medium     — British female
#   ryan-medium    — American male
#   ljspeech       — Clear female
#
# Usage:
#   bash scripts/generate-narration.sh
#   bash scripts/generate-narration.sh --voice en_US-lessac-medium
#   bash scripts/generate-narration.sh --chapters  # Split into per-chapter files

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
OUT_DIR="$PROJECT_DIR/out/audio"
VOICE="${1:-en_US-lessac-medium}"

echo ""
echo "  ╔═══════════════════════════════════════════╗"
echo "  ║  Piper TTS — Narration Generator          ║"
echo "  ║  Voice: $VOICE                            ║"
echo "  ╚═══════════════════════════════════════════╝"
echo ""

# Check piper is installed
if ! command -v piper &> /dev/null; then
    echo "  [ERROR] Piper TTS not found."
    echo "  Install: pip install piper-tts"
    echo "  Docs: https://github.com/rhasspy/piper"
    echo ""
    echo "  Alternative: Use any TTS engine with the narration script:"
    echo "    node scripts/extract-narration.mjs > out/narration.txt"
    echo ""
    exit 1
fi

# Create output directory
mkdir -p "$OUT_DIR"

# Extract narration text
echo "  Extracting narration script..."
node "$SCRIPT_DIR/extract-narration.mjs" > "$OUT_DIR/narration.txt"
echo "  [OK] Narration script saved to out/audio/narration.txt"

# Generate full narration WAV
echo "  Generating speech with Piper TTS ($VOICE)..."
piper --model "$VOICE" --output_file "$OUT_DIR/narration.wav" < "$OUT_DIR/narration.txt"
echo "  [OK] Full narration: out/audio/narration.wav"

# If ffmpeg available, split into chapters
if command -v ffmpeg &> /dev/null; then
    echo "  Splitting into chapter segments..."

    # Approximate timings (adjust based on actual speech speed)
    # Chapter boundaries based on text volume
    CHAPTERS=(
        "intro:0:15"
        "ch1_petrodollar:15:90"
        "ch2_chipwar:90:145"
        "ch3_energy:145:210"
        "ch4_brics:210:260"
        "ch5_mideast:260:310"
        "ch6_surveillance:310:380"
        "ch7_warmachine:380:450"
        "outro:450:465"
    )

    for ch_info in "${CHAPTERS[@]}"; do
        IFS=':' read -r name start end <<< "$ch_info"
        duration=$((end - start))
        ffmpeg -y -i "$OUT_DIR/narration.wav" \
            -ss "$start" -t "$duration" \
            -c:a pcm_s16le \
            "$OUT_DIR/$name.wav" \
            -loglevel error 2>/dev/null || true
        echo "    [OK] $name.wav (${start}s → ${end}s)"
    done
fi

echo ""
echo "  ═══ Done ═══"
echo "  Full narration: $OUT_DIR/narration.wav"
echo "  Chapter WAVs:   $OUT_DIR/ch*.wav"
echo ""
echo "  Add to Remotion:"
echo "    import { Audio, staticFile } from 'remotion';"
echo "    <Audio src={staticFile('audio/narration.wav')} />"
echo ""
