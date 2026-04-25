"""Pilot episode — first 60 seconds (3–4 scenes).

Filled in by Step 6 of the bootstrap prompt, after research.md, script.md,
and storyboard.md exist. Imports come from shared/styles.py — no
hardcoded colors.

Render preview:
    ./pipeline/render.sh episodes/001-pilot/scene.py Hook -ql
"""
from __future__ import annotations

from manim import FadeIn, FadeOut, Scene

from shared.styles import title_card


class Hook(Scene):
    """Scene 1 — hook (0:00–0:08)."""

    def construct(self) -> None:
        card = title_card("Pilot", "Replace me once script.md is locked")
        self.play(FadeIn(card, run_time=0.8))
        self.wait(6.4)
        self.play(FadeOut(card, run_time=0.8))
