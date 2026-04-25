"""Pilot episode — Operation Gladio. First 60 seconds, four scenes.

Render preview:
    ./pipeline/render.sh episodes/001-pilot/scene.py Hook -ql
    ./pipeline/render.sh episodes/001-pilot/scene.py Doctrine -ql
    ./pipeline/render.sh episodes/001-pilot/scene.py Network -ql
    ./pipeline/render.sh episodes/001-pilot/scene.py Pivot -ql

All colors and typography come from shared/styles. No hardcoded colors here.
"""
from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
    Circle,
    Dot,
    FadeIn,
    FadeOut,
    Rectangle,
    Scene,
    Text,
    Transform,
    VGroup,
    Wait,
    Write,
)

from shared.styles import (
    ACCENT,
    BG,
    BODY_FONT,
    FG,
    MONO_FONT,
    MUTED,
    SUPPORTING,
    TITLE_FONT,
    VERIFIED,
    classification_stamp,
    lower_third,
    source_caption,
)


# -- Scene 1 -----------------------------------------------------------------
class Hook(Scene):
    """0:00–0:08 — title + DECLASSIFIED stamp."""

    def construct(self) -> None:
        self.camera.background_color = BG

        title = Text(
            "OPERATION GLADIO",
            font=TITLE_FONT,
            color=FG,
            weight="BOLD",
        ).scale(1.3)
        subtitle = Text(
            "NATO's Secret War Inside Its Own Borders",
            font=MONO_FONT,
            color=MUTED,
        ).scale(0.45)
        subtitle.next_to(title, DOWN, buff=0.45)

        stamp = classification_stamp("DECLASSIFIED  24·X·1990")

        self.play(FadeIn(title, shift=DOWN * 0.2, run_time=0.7))
        self.play(FadeIn(subtitle, run_time=0.4))
        self.play(FadeIn(stamp, scale=0.6, run_time=0.5))
        self.wait(5.4)
        self.play(
            FadeOut(title, run_time=0.4),
            FadeOut(subtitle, run_time=0.4),
            FadeOut(stamp, run_time=0.4),
        )


# -- Scene 2 -----------------------------------------------------------------
class Doctrine(Scene):
    """0:08–0:25 — "STAY-BEHIND" plus the three attribute lines."""

    def construct(self) -> None:
        self.camera.background_color = BG

        headline = Text(
            "STAY-BEHIND",
            font=MONO_FONT,
            color=FG,
            weight="BOLD",
        ).scale(1.6)
        headline.shift(UP * 1.2)

        lines = VGroup(
            Text("cells with weapons.", font=BODY_FONT, color=FG).scale(0.6),
            Text("cells with codenames.", font=BODY_FONT, color=FG).scale(0.6),
            Text("cells with orders.", font=BODY_FONT, color=FG).scale(0.6),
        ).arrange(DOWN, buff=0.4)
        lines.next_to(headline, DOWN, buff=0.9)

        l3 = lower_third("NATO doctrine, 1947")

        self.play(Write(headline, run_time=0.8))
        self.play(FadeIn(l3, run_time=0.4))
        for line in lines:
            self.play(FadeIn(line, shift=RIGHT * 0.2, run_time=0.35))
            self.wait(0.4)
        self.wait(13.0 - (3 * 0.75) - 1.2)
        self.play(
            FadeOut(headline),
            FadeOut(lines),
            FadeOut(l3),
            run_time=0.5,
        )


# -- Scene 3 -----------------------------------------------------------------
class Network(Scene):
    """0:25–0:45 — stylized country pins across Western Europe."""

    # Approximate, intentionally non-cartographic positions in Manim units.
    # Order matters: Italy first (large red), then 12 confirmed (white),
    # then Sweden + Finland (teal — "later disclosed").
    PINS = [
        # (name, x, y, kind)
        ("Italy",         0.6, -1.2, "primary"),
        ("Belgium",      -0.9,  0.7, "confirmed"),
        ("Netherlands",  -0.7,  1.2, "confirmed"),
        ("Luxembourg",   -0.5,  0.4, "confirmed"),
        ("West Germany",  0.2,  0.9, "confirmed"),
        ("France",       -1.6,  0.0, "confirmed"),
        ("Switzerland",  -0.2,  0.1, "confirmed"),
        ("Austria",       0.9,  0.3, "confirmed"),
        ("Denmark",       0.4,  1.7, "confirmed"),
        ("Norway",        0.1,  2.6, "confirmed"),
        ("Portugal",     -3.0, -1.0, "confirmed"),
        ("Spain",        -2.3, -0.8, "confirmed"),
        ("Greece",        2.4, -1.5, "confirmed"),
        ("Turkey",        3.4, -0.9, "confirmed"),
        ("Sweden",        0.7,  2.4, "later"),
        ("Finland",       1.6,  2.6, "later"),
    ]

    def color_for(self, kind: str):
        if kind == "primary":
            return ACCENT
        if kind == "later":
            return VERIFIED
        return FG

    def size_for(self, kind: str) -> float:
        return 0.18 if kind == "primary" else 0.10

    def construct(self) -> None:
        self.camera.background_color = BG

        # Frame label so viewers know what they're looking at.
        frame = Text(
            "stay-behind networks · western europe",
            font=MONO_FONT,
            color=MUTED,
        ).scale(0.35)
        frame.to_edge(UP, buff=0.4)
        self.play(FadeIn(frame, run_time=0.3))

        primary_label = None
        confirmed_pins = []
        later_pins = []

        for name, x, y, kind in self.PINS:
            dot = Dot(point=[x, y, 0], color=self.color_for(kind), radius=self.size_for(kind))
            label = Text(name, font=BODY_FONT, color=FG).scale(0.28)
            label.next_to(dot, RIGHT, buff=0.1)
            group = VGroup(dot, label)

            if kind == "primary":
                primary_label = Text(
                    "622 members · 139 arms caches",
                    font=MONO_FONT,
                    color=ACCENT,
                ).scale(0.32)
                primary_label.next_to(dot, DOWN, buff=0.2)
                self.play(
                    FadeIn(group, scale=0.5, run_time=0.35),
                    FadeIn(primary_label, run_time=0.35),
                )
                self.wait(0.4)
            elif kind == "later":
                later_pins.append(group)
            else:
                confirmed_pins.append(group)

        # Drop the 13 confirmed pins in groups of 3.
        for i in range(0, len(confirmed_pins), 3):
            batch = confirmed_pins[i : i + 3]
            self.play(*[FadeIn(g, scale=0.5, run_time=0.4) for g in batch])
            self.wait(0.2)

        # Then the two "later disclosed" teal pins.
        self.play(*[FadeIn(g, scale=0.5, run_time=0.45) for g in later_pins])

        cap = source_caption("EU Parliament Res., 22 Nov 1990")
        self.play(FadeIn(cap, run_time=0.4))

        self.wait(2.0)
        self.play(
            FadeOut(VGroup(frame, *confirmed_pins, *later_pins, primary_label, cap)),
            run_time=0.5,
        )


# -- Scene 4 -----------------------------------------------------------------
class Pivot(Scene):
    """0:45–1:00 — date range + tease into the rest of the video."""

    def construct(self) -> None:
        self.camera.background_color = BG

        dates = Text(
            "1947  —  1990",
            font=MONO_FONT,
            color=ACCENT,
            weight="BOLD",
        ).scale(1.6)
        dates.shift(UP * 0.6)

        line1 = Text(
            "Officially, they were there to fight Soviets who never came.",
            font=BODY_FONT,
            color=FG,
        ).scale(0.45)
        line1.next_to(dates, DOWN, buff=0.7)

        line2 = Text(
            "What they actually did is the rest of this dossier.",
            font=BODY_FONT,
            color=SUPPORTING,
        ).scale(0.4)
        line2.next_to(line1, DOWN, buff=0.35)

        self.play(Write(dates, run_time=0.9))
        self.play(FadeIn(line1, shift=DOWN * 0.15, run_time=0.5))
        self.wait(0.6)
        self.play(FadeIn(line2, run_time=0.5))
        self.wait(11.5)
        self.play(
            FadeOut(VGroup(dates, line1, line2)),
            run_time=0.6,
        )
