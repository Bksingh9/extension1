"""Episode 002 — Operation Northwoods.

Scene stub: only the Hook is implemented. Build out scenes 2–10 after
the Playwright pass downloads the NSArchive PDF and we can quote line
numbers from the actual document.

Render preview:
    PYTHONPATH=. .venv/bin/manim -ql episodes/002-northwoods/scene.py Hook
"""
from __future__ import annotations

from manim import (
    DOWN,
    FadeIn,
    FadeOut,
    Scene,
    Text,
    VGroup,
)

from shared.styles import (
    ACCENT,
    BG,
    FG,
    MONO_FONT,
    MUTED,
    TITLE_FONT,
    classification_stamp,
)


class Hook(Scene):
    """0:00–0:08 — title + DECLASSIFIED stamp."""

    def construct(self) -> None:
        self.camera.background_color = BG

        title = Text(
            "OPERATION NORTHWOODS",
            font=TITLE_FONT,
            color=FG,
            weight="BOLD",
        ).scale(1.2)

        subtitle = Text(
            "The False Flag the Pentagon Wrote Down",
            font=MONO_FONT,
            color=MUTED,
        ).scale(0.45)
        subtitle.next_to(title, DOWN, buff=0.45)

        stamp = classification_stamp("TOP SECRET  —  DECLASSIFIED 18·XI·1997")

        self.play(FadeIn(title, shift=DOWN * 0.2, run_time=0.7))
        self.play(FadeIn(subtitle, run_time=0.4))
        self.play(FadeIn(stamp, scale=0.6, run_time=0.5))
        self.wait(5.4)
        self.play(
            FadeOut(VGroup(title, subtitle, stamp)),
            run_time=0.4,
        )
