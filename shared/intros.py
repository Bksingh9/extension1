"""Standard intro and outro scenes.

Subclass and override CHANNEL_NAME / TAGLINE per channel identity.
"""
from __future__ import annotations

from manim import FadeIn, FadeOut, Scene

from shared.styles import title_card


class StandardIntro(Scene):
    """5-second branded intro."""

    CHANNEL_NAME: str = "TBD"
    TAGLINE: str = "TBD"

    def construct(self) -> None:
        card = title_card(self.CHANNEL_NAME, self.TAGLINE)
        self.play(FadeIn(card, run_time=1.0))
        self.wait(2.0)
        self.play(FadeOut(card, run_time=1.0))


class StandardOutro(Scene):
    """3-second outro card."""

    MESSAGE: str = "Subscribe for more."

    def construct(self) -> None:
        card = title_card(self.MESSAGE)
        self.play(FadeIn(card, run_time=0.6))
        self.wait(1.6)
        self.play(FadeOut(card, run_time=0.6))
