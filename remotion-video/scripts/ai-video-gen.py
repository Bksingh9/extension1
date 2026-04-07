#!/usr/bin/env python3
"""
AI Video Generation Pipeline for Geo-Politics Documentary
==========================================================
Generates cinematic B-roll clips per chapter using open-source models.

Supported models (auto-detected by available VRAM):
  - Wan 2.2 5B   (8GB VRAM minimum)  — Best for low-end GPUs
  - LTX-2        (10GB+ VRAM)        — Native 4K with audio
  - Open-Sora    (varies)            — Most flexible T2V/I2V
  - HunyuanVideo (14GB+)            — Highest visual quality
  - Mochi 1      (22GB+)            — Best motion quality

Usage:
  python scripts/ai-video-gen.py --chapter all --model wan2.2
  python scripts/ai-video-gen.py --chapter ch1_petrodollar --model ltx2
  python scripts/ai-video-gen.py --list-models

Requirements:
  pip install torch torchvision diffusers transformers accelerate
  # Model-specific:
  pip install wan-video          # Wan 2.2
  pip install ltx-video          # LTX-2
  # Or clone Open-Sora/HunyuanVideo repos
"""

import argparse
import os
import sys
import json
from pathlib import Path

# ─── Chapter prompts (cinematic conspiracy documentary style) ───
CHAPTER_PROMPTS = {
    "ch1_petrodollar": {
        "prompt": "Cinematic dark shot of gold coins cascading onto a glowing world map, dramatic side lighting, "
                  "deep shadows, conspiracy documentary aesthetic, smoke wisps, 720p, moody color grading",
        "negative": "bright, cheerful, cartoon, low quality, blurry",
        "duration": 4,  # seconds
    },
    "ch2_chipwar": {
        "prompt": "Extreme close-up of silicon microchip circuitry with pulsing red and blue LED reflections, "
                  "dark background, tech war aesthetic, data streams flowing, cinematic macro photography",
        "negative": "natural, outdoor, people, cartoon, low quality",
        "duration": 4,
    },
    "ch3_energy": {
        "prompt": "Dramatic underwater shot of a metal pipeline rupturing with bubbles and debris rising, "
                  "dark ocean, volumetric light rays from above, documentary cinematography, teal color grade",
        "negative": "bright, sunny, happy, cartoon, low quality",
        "duration": 4,
    },
    "ch4_brics": {
        "prompt": "Gold bars being stacked methodically on a dark table, flags of Brazil Russia India China "
                  "South Africa waving in soft background, dramatic spotlight, moody atmosphere",
        "negative": "bright, outdoor, people, cartoon, low quality",
        "duration": 4,
    },
    "ch5_mideast": {
        "prompt": "Ornate chess pieces on a map of the Middle East, dramatic side lighting casting long shadows, "
                  "oil derricks silhouetted in background, desert dust particles, cinematic",
        "negative": "bright, modern, cartoon, low quality, blurry",
        "duration": 4,
    },
    "ch6_surveillance": {
        "prompt": "Security camera POV footage with green digital scan lines and data overlays, dystopian city "
                  "surveillance, facial recognition boxes appearing, dark cyberpunk aesthetic",
        "negative": "bright, cheerful, nature, cartoon, low quality",
        "duration": 4,
    },
    "ch7_warmachine": {
        "prompt": "Slow motion military fighter jets flying in formation over a rain of hundred dollar bills, "
                  "dramatic sky, dark clouds, cinematic wide shot, documentary style",
        "negative": "bright, peaceful, cartoon, low quality, blurry",
        "duration": 4,
    },
    "intro": {
        "prompt": "Dark spinning globe with glowing network connections between cities, conspiracy red string "
                  "connections overlaid, dramatic zoom, smoke, cinematic title card background",
        "negative": "bright, cheerful, cartoon, low quality",
        "duration": 5,
    },
    "outro": {
        "prompt": "Dramatic slow push-in on a single eye with the world reflected in the iris, "
                  "dark atmosphere, surveillance theme, cinematic depth of field",
        "negative": "bright, happy, cartoon, low quality, blurry",
        "duration": 3,
    },
}

# ─── Model configurations ───
MODELS = {
    "wan2.2": {
        "name": "Wan 2.2 (5B MoE)",
        "min_vram_gb": 8,
        "repo": "Wan-Video/Wan2.2",
        "install": "pip install wan-video",
        "type": "diffusers",
    },
    "ltx2": {
        "name": "LTX-2 (Lightricks)",
        "min_vram_gb": 10,
        "repo": "Lightricks/LTX-Video",
        "install": "pip install ltx-video",
        "type": "ltx",
    },
    "open-sora": {
        "name": "Open-Sora 2.0 (11B)",
        "min_vram_gb": 12,
        "repo": "hpcaitech/Open-Sora",
        "install": "git clone https://github.com/hpcaitech/Open-Sora && cd Open-Sora && pip install -v .",
        "type": "open-sora",
    },
    "hunyuan": {
        "name": "HunyuanVideo (13B)",
        "min_vram_gb": 14,
        "repo": "Tencent-Hunyuan/HunyuanVideo",
        "install": "git clone https://github.com/Tencent-Hunyuan/HunyuanVideo",
        "type": "hunyuan",
    },
    "mochi": {
        "name": "Mochi 1 (10B)",
        "min_vram_gb": 22,
        "repo": "genmoai/mochi",
        "install": "pip install mochi-video",
        "type": "mochi",
    },
}


def detect_gpu():
    """Detect available GPU and VRAM."""
    try:
        import torch
        if torch.cuda.is_available():
            vram = torch.cuda.get_device_properties(0).total_memory / (1024**3)
            name = torch.cuda.get_device_name(0)
            return {"available": True, "name": name, "vram_gb": round(vram, 1)}
    except ImportError:
        pass
    return {"available": False, "name": "None", "vram_gb": 0}


def select_best_model(gpu_info):
    """Auto-select best model for available hardware."""
    vram = gpu_info["vram_gb"]
    if vram >= 22:
        return "mochi"
    elif vram >= 14:
        return "hunyuan"
    elif vram >= 12:
        return "open-sora"
    elif vram >= 10:
        return "ltx2"
    elif vram >= 8:
        return "wan2.2"
    return None


def generate_wan22(prompt_data, output_path, fps=24):
    """Generate video using Wan 2.2."""
    try:
        import torch
        from diffusers import WanPipeline
        from diffusers.utils import export_to_video

        pipe = WanPipeline.from_pretrained(
            "Wan-Video/Wan2.2-T2V-5B",
            torch_dtype=torch.float16,
        ).to("cuda")
        pipe.enable_model_cpu_offload()

        frames = pipe(
            prompt=prompt_data["prompt"],
            negative_prompt=prompt_data.get("negative", ""),
            num_frames=prompt_data["duration"] * fps,
            height=720,
            width=1280,
            num_inference_steps=30,
            guidance_scale=7.0,
        ).frames[0]

        export_to_video(frames, output_path, fps=fps)
        return True
    except Exception as e:
        print(f"  [ERROR] Wan 2.2 generation failed: {e}")
        return False


def generate_ltx2(prompt_data, output_path, fps=24):
    """Generate video using LTX-2."""
    try:
        import torch
        from diffusers import LTXPipeline
        from diffusers.utils import export_to_video

        pipe = LTXPipeline.from_pretrained(
            "Lightricks/LTX-Video",
            torch_dtype=torch.float16,
        ).to("cuda")
        pipe.enable_model_cpu_offload()

        frames = pipe(
            prompt=prompt_data["prompt"],
            negative_prompt=prompt_data.get("negative", ""),
            num_frames=prompt_data["duration"] * fps,
            height=720,
            width=1280,
            num_inference_steps=40,
        ).frames[0]

        export_to_video(frames, output_path, fps=fps)
        return True
    except Exception as e:
        print(f"  [ERROR] LTX-2 generation failed: {e}")
        return False


def generate_placeholder(prompt_data, output_path, fps=24):
    """Generate a placeholder clip when no GPU is available."""
    print(f"  [INFO] No GPU — saving prompt to {output_path}.prompt.json")
    prompt_file = str(output_path) + ".prompt.json"
    with open(prompt_file, "w") as f:
        json.dump(prompt_data, f, indent=2)
    print(f"  [SAVED] Prompt saved. Run on GPU machine to generate actual video.")
    return False


GENERATORS = {
    "wan2.2": generate_wan22,
    "ltx2": generate_ltx2,
    "open-sora": generate_placeholder,  # Requires custom integration
    "hunyuan": generate_placeholder,     # Requires custom integration
    "mochi": generate_placeholder,       # Requires custom integration
}


def main():
    parser = argparse.ArgumentParser(description="AI Video Generation for Geo-Politics Documentary")
    parser.add_argument("--chapter", default="all", help="Chapter ID or 'all'")
    parser.add_argument("--model", default="auto", help="Model: wan2.2, ltx2, open-sora, hunyuan, mochi, auto")
    parser.add_argument("--output", default="public/ai-clips", help="Output directory")
    parser.add_argument("--fps", type=int, default=24, help="Frames per second")
    parser.add_argument("--list-models", action="store_true", help="List available models")
    parser.add_argument("--list-chapters", action="store_true", help="List chapter prompts")
    args = parser.parse_args()

    print("\n  ╔═══════════════════════════════════════════════╗")
    print("  ║  AI Video Gen — Geo-Politics Documentary      ║")
    print("  ║  Open-Source Models (Wan 2.2 / LTX-2 / etc.)  ║")
    print("  ╚═══════════════════════════════════════════════╝\n")

    if args.list_models:
        print("  Available models:\n")
        for key, m in MODELS.items():
            print(f"    {key:12s} — {m['name']:30s} (min {m['min_vram_gb']}GB VRAM)")
            print(f"    {'':12s}   Repo: github.com/{m['repo']}")
            print(f"    {'':12s}   Install: {m['install']}\n")
        return

    if args.list_chapters:
        print("  Chapter prompts:\n")
        for key, p in CHAPTER_PROMPTS.items():
            print(f"    {key:20s} — {p['duration']}s — {p['prompt'][:80]}...")
        return

    # Detect GPU
    gpu = detect_gpu()
    print(f"  GPU: {gpu['name']} ({gpu['vram_gb']}GB VRAM)")

    # Select model
    if args.model == "auto":
        model_key = select_best_model(gpu)
        if model_key:
            print(f"  Auto-selected: {MODELS[model_key]['name']}")
        else:
            print("  No GPU or insufficient VRAM — generating prompt files only")
            model_key = "wan2.2"  # Will fall through to placeholder
    else:
        model_key = args.model
        if model_key not in MODELS:
            print(f"  [ERROR] Unknown model: {model_key}. Use --list-models to see options.")
            sys.exit(1)
        print(f"  Selected: {MODELS[model_key]['name']}")

    # Determine chapters
    if args.chapter == "all":
        chapters = list(CHAPTER_PROMPTS.keys())
    else:
        if args.chapter not in CHAPTER_PROMPTS:
            print(f"  [ERROR] Unknown chapter: {args.chapter}. Use --list-chapters.")
            sys.exit(1)
        chapters = [args.chapter]

    # Create output directory
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate videos
    generator = GENERATORS.get(model_key, generate_placeholder)
    results = {"generated": [], "prompts_saved": [], "failed": []}

    print(f"\n  Generating {len(chapters)} clips...\n")

    for ch_id in chapters:
        prompt_data = CHAPTER_PROMPTS[ch_id]
        output_path = output_dir / f"{ch_id}.mp4"
        print(f"  [{ch_id}] {prompt_data['prompt'][:60]}...")

        if not gpu["available"]:
            generate_placeholder(prompt_data, output_path)
            results["prompts_saved"].append(ch_id)
        else:
            success = generator(prompt_data, str(output_path), fps=args.fps)
            if success:
                results["generated"].append(ch_id)
                print(f"  [OK] {output_path}")
            else:
                results["prompts_saved"].append(ch_id)

    # Summary
    print(f"\n  ═══ Summary ═══")
    print(f"  Generated: {len(results['generated'])} clips")
    print(f"  Prompts saved: {len(results['prompts_saved'])} (run on GPU to generate)")
    if results["generated"]:
        print(f"\n  Clips ready in: {output_dir}/")
        print(f"  Add to Remotion via: <AiClipOverlay chapterId='ch1_petrodollar' />")
    print()


if __name__ == "__main__":
    main()
