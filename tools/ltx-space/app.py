"""LTX-Video text-to-video — Hugging Face ZeroGPU Space.

Open-source video generation as a web app. Runs on HF's FREE ZeroGPU
hardware (no local GPU, no payment). Deploy this folder to a Space on
your own HF account — see DEPLOY.md.

The @spaces.GPU decorator attaches a GPU only for the duration of each
generation call, which is what makes ZeroGPU free.
"""
import random

import gradio as gr
import numpy as np
import spaces
import torch
from diffusers import LTXPipeline
from diffusers.utils import export_to_video

MODEL_ID = "Lightricks/LTX-Video"
MAX_SEED = np.iinfo(np.int32).max

# Loaded once at startup. ZeroGPU provides a CUDA device at build time
# for the initial load; per-request GPU is granted by @spaces.GPU.
pipe = LTXPipeline.from_pretrained(MODEL_ID, torch_dtype=torch.bfloat16)
pipe.to("cuda")

DEFAULT_NEG = (
    "worst quality, inconsistent motion, blurry, jittery, distorted, "
    "watermark, text, logo"
)


@spaces.GPU(duration=120)
def generate(
    prompt: str,
    negative_prompt: str,
    width: int,
    height: int,
    num_frames: int,
    steps: int,
    seed: int,
    randomize_seed: bool,
    progress=gr.Progress(track_tqdm=True),
):
    if not prompt or not prompt.strip():
        raise gr.Error("Enter a prompt.")
    if randomize_seed:
        seed = random.randint(0, MAX_SEED)
    generator = torch.Generator(device="cuda").manual_seed(int(seed))

    frames = pipe(
        prompt=prompt.strip(),
        negative_prompt=(negative_prompt or DEFAULT_NEG).strip(),
        width=int(width),
        height=int(height),
        num_frames=int(num_frames),
        num_inference_steps=int(steps),
        generator=generator,
    ).frames[0]

    out_path = export_to_video(frames, fps=24)
    return out_path, seed


EXAMPLES = [
    ["a paper boat sailing on a calm lake at sunset, soft ripples, golden hour"],
    ["aerial dawn shot of a narrow sea strait, a single tanker drifting through, glassy water"],
    ["slow forward push over fibre-optic cables on a silt seabed, cold blue-green, particulate drift"],
    ["a red panda riding a bicycle through neon Tokyo at dusk, slow tracking shot"],
]

with gr.Blocks(title="LTX-Video Generator") as demo:
    gr.Markdown(
        "# 🎬 LTX-Video Generator\n"
        "Open-source text-to-video on free ZeroGPU. Type a prompt, press **Generate**, "
        "download the MP4. Keep clips short (≤ 5 s / 121 frames) so each run fits the "
        "ZeroGPU time budget."
    )
    with gr.Row():
        with gr.Column(scale=3):
            prompt = gr.Textbox(label="Prompt", lines=3,
                                placeholder="a paper boat sailing on a calm lake at sunset…")
            negative = gr.Textbox(label="Negative prompt", value=DEFAULT_NEG, lines=2)
            with gr.Row():
                width = gr.Slider(384, 1280, value=768, step=32, label="Width")
                height = gr.Slider(384, 1280, value=512, step=32, label="Height")
            with gr.Row():
                num_frames = gr.Slider(25, 161, value=121, step=8, label="Frames (24 fps)")
                steps = gr.Slider(10, 50, value=30, step=1, label="Steps")
            with gr.Row():
                seed = gr.Slider(0, MAX_SEED, value=0, step=1, label="Seed")
                randomize = gr.Checkbox(value=True, label="Randomize seed")
            go = gr.Button("Generate", variant="primary")
        with gr.Column(scale=2):
            video_out = gr.Video(label="Result")
            used_seed = gr.Number(label="Seed used", interactive=False)
    gr.Examples(EXAMPLES, inputs=[prompt])

    go.click(
        generate,
        inputs=[prompt, negative, width, height, num_frames, steps, seed, randomize],
        outputs=[video_out, used_seed],
    )

if __name__ == "__main__":
    demo.queue().launch()
