# Video generation tools (parked, not wired in)

Open-source AI video models that could supply **B-roll** for episodes
(intro hero shots, transitions, ambient cutaways under voiceover).
They do **not** replace Manim — Manim still owns the diagram/equation
scenes where text and layout precision matter.

## Candidates

### CogVideoX — `https://github.com/zai-org/CogVideo`
- ~5B params, text-to-video and image-to-video.
- Runs on a **single 24 GB consumer GPU** (4090, A5000, etc.).
- Faster inference, lower fidelity than Hunyuan.
- **Use when:** you need quick ambient B-roll on a workstation you own.

### HunyuanVideo — `https://github.com/Tencent-Hunyuan/HunyuanVideo`
- ~13B params, text-to-video and image-to-video.
- Needs **60 GB+ VRAM** for full quality (H100 / A100-80GB / multi-GPU),
  or a community-distilled fork for smaller cards.
- Higher cinematic quality, slower.
- **Use when:** an episode opens with a hero shot worth renting a cloud
  H100 for an hour.

## When to actually wire one in

Trigger conditions:
1. An episode storyboard calls for a non-diagram cutaway that Manim
   can't fake with primitives.
2. You're willing to add a `pipeline/broll.py` step that runs **after**
   the script is locked but **before** final render, so B-roll clips
   are composited as background layers behind the Manim scene.
3. You have GPU access (local 24 GB for CogVideoX, or rented H100 for
   Hunyuan).

Until all three are true: leave this file as the only record.

## Workflow sketch (for future-you)

```
episodes/NNN/storyboard.md
  └── marks scenes that need B-roll with [BROLL: <prompt>]
pipeline/broll.py
  ├── parses storyboard for [BROLL] tags
  ├── calls CogVideoX or Hunyuan with the prompt
  ├── writes clips to episodes/NNN/broll/<scene>.mp4
  └── scene.py composites them as background via VideoMobject
```

No code yet. Add when condition (1) actually shows up in a real
storyboard.
