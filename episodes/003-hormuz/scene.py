"""Episode 003 — The Day Iran Closed the Strait. First 90s, 4 scenes.

Render an individual scene preview:
    ./pipeline/render.sh episodes/003-hormuz/scene.py Hook -ql

Render all four 90s scenes at -ql (one process):
    PYTHONPATH=. .venv/bin/manim -ql episodes/003-hormuz/scene.py \\
        Hook Chokepoint Oil Cables

All colors and typography come from shared/styles. No hardcoded colors here.
No LaTeX (no MathTex/Tex) — host has no TeX.
"""
from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    Create,
    CurvedArrow,
    DashedLine,
    FadeIn,
    FadeOut,
    Line,
    Rectangle,
    Scene,
    Text,
    ValueTracker,
    VGroup,
    Write,
    always_redraw,
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
    episode_mark,
    lower_third,
    source_caption,
)


EP_NUM = 3
EP_SLUG = "Hormuz"


def _mark() -> VGroup:
    return episode_mark(EP_NUM, EP_SLUG)


def tracked_int(
    tracker: ValueTracker,
    *,
    center,
    font: str,
    color,
    scale: float = 1.0,
    weight: str = "BOLD",
    fmt: str = "{:,}",
):
    """Always-redrawn integer Text bound to a ValueTracker.

    Avoids Manim's Integer/DecimalNumber, which require LaTeX.
    """
    return always_redraw(
        lambda: Text(
            fmt.format(int(tracker.get_value())),
            font=font,
            color=color,
            weight=weight,
        )
        .scale(scale)
        .move_to(center)
    )


# -- Scene 1 -----------------------------------------------------------------
class Hook(Scene):
    """0:00–0:10 — title + CLOSED stamp."""

    def construct(self) -> None:
        self.camera.background_color = BG
        self.add(_mark())

        kicker = Text(
            "THE HORMUZ FILES",
            font=MONO_FONT,
            color=MUTED,
        ).scale(0.45)
        kicker.shift(UP * 1.2)

        title = Text(
            "the day Iran closed the strait",
            font=TITLE_FONT,
            color=FG,
            slant="ITALIC",
        ).scale(1.1)

        stamp = classification_stamp("CLOSED  28·II·2026")

        self.play(FadeIn(kicker, run_time=0.5))
        self.play(FadeIn(title, shift=DOWN * 0.2, run_time=0.7))
        self.play(FadeIn(stamp, scale=0.6, run_time=0.5))
        self.wait(7.3)
        self.play(
            FadeOut(kicker, run_time=0.4),
            FadeOut(title, run_time=0.4),
            FadeOut(stamp, run_time=0.4),
        )


# -- Scene 2 -----------------------------------------------------------------
class Chokepoint(Scene):
    """0:10–0:30 — stylised strait, the 34 km gap."""

    def construct(self) -> None:
        self.camera.background_color = BG
        self.add(_mark())

        # Stylised, non-cartographic: two horizontal coastlines with the
        # narrow channel between them. Iran on top, Arabian Peninsula on
        # the bottom. The 34 km gap is the visual point of the scene.
        iran_label = Text("IRAN", font=MONO_FONT, color=MUTED).scale(0.55)
        iran_label.shift(UP * 2.5 + LEFT * 4.0)

        arabia_label = Text("ARABIAN PENINSULA", font=MONO_FONT, color=MUTED).scale(0.45)
        arabia_label.shift(DOWN * 2.6 + RIGHT * 3.0)

        # Coastlines: simple wavy-ish dashed lines for stylised feel.
        iran_coast = DashedLine(
            [-6.0, 1.4, 0], [6.0, 1.0, 0],
            color=MUTED, stroke_width=2, dash_length=0.18,
        )
        arabia_coast = DashedLine(
            [-6.0, -1.4, 0], [6.0, -1.0, 0],
            color=MUTED, stroke_width=2, dash_length=0.18,
        )

        # The arrow that measures the narrow gap.
        gap_arrow = Arrow(
            [0.0, 1.05, 0], [0.0, -1.15, 0],
            buff=0,
            color=ACCENT,
            stroke_width=4,
            tip_length=0.25,
            max_tip_length_to_length_ratio=0.12,
        )
        # Manim Arrow is single-headed; mirror it for the second tip.
        gap_arrow_back = Arrow(
            [0.0, -1.15, 0], [0.0, 1.05, 0],
            buff=0,
            color=ACCENT,
            stroke_width=4,
            tip_length=0.25,
            max_tip_length_to_length_ratio=0.12,
        )

        gap_label = Text("34 km", font=MONO_FONT, color=ACCENT, weight="BOLD").scale(0.7)
        gap_label.move_to([0.85, 0.0, 0])

        comparison = Text(
            "≈ width of London W↔E",
            font=BODY_FONT,
            color=MUTED,
            slant="ITALIC",
        ).scale(0.38)
        comparison.move_to([0.85, -0.55, 0])

        cap = source_caption("IEA · Strait of Hormuz fact sheet")

        self.play(FadeIn(iran_label, run_time=0.4))
        self.play(Create(iran_coast, run_time=0.7))
        self.play(FadeIn(arabia_label, run_time=0.4))
        self.play(Create(arabia_coast, run_time=0.7))
        self.play(
            Create(gap_arrow, run_time=0.5),
            Create(gap_arrow_back, run_time=0.5),
        )
        self.play(FadeIn(gap_label, run_time=0.4))
        self.wait(0.4)
        self.play(FadeIn(comparison, run_time=0.4))
        self.play(FadeIn(cap, run_time=0.3))
        self.wait(20.0 - (0.4 + 0.7 + 0.4 + 0.7 + 0.5 + 0.4 + 0.4 + 0.4 + 0.3))
        self.play(
            FadeOut(VGroup(
                iran_label, iran_coast, arabia_label, arabia_coast,
                gap_arrow, gap_arrow_back, gap_label, comparison, cap,
            )),
            run_time=0.6,
        )


# -- Scene 3 -----------------------------------------------------------------
class Oil(Scene):
    """0:30–0:55 — 20 mb/d ticker + national share row + LNG line."""

    def construct(self) -> None:
        self.camera.background_color = BG
        self.add(_mark())

        kicker = Text("HORMUZ · 2024 · DAILY OIL FLOW",
                      font=MONO_FONT, color=MUTED).scale(0.4)
        kicker.shift(UP * 2.6)

        # Big number ticking up.
        oil_track = ValueTracker(0)
        oil_pos = [0, 0.7, 0]
        oil_n = tracked_int(
            oil_track, center=oil_pos,
            font=MONO_FONT, color=ACCENT, scale=1.7,
        )
        oil_unit = Text("barrels of oil per day",
                        font=MONO_FONT, color=MUTED).scale(0.45)
        oil_unit.move_to([0, -0.2, 0])

        # National share chips. Saudi Arabia in red (38% / 5.5M b/d),
        # the rest white. Order: SA, UAE, Iraq, Kuwait, Qatar, Iran.
        chips_data = [
            ("Saudi Arabia",  "5.5 M · 38%", ACCENT),
            ("UAE",            "",           FG),
            ("Iraq",           "",           FG),
            ("Kuwait",         "",           FG),
            ("Qatar",          "",           FG),
            ("Iran",           "",           FG),
        ]
        chips = VGroup()
        for name, sub, color in chips_data:
            head = Text(name, font=MONO_FONT, color=color, weight="BOLD").scale(0.32)
            if sub:
                tail = Text(sub, font=MONO_FONT, color=color).scale(0.26)
                chip = VGroup(head, tail).arrange(DOWN, buff=0.05)
            else:
                chip = VGroup(head)
            chips.add(chip)
        chips.arrange(RIGHT, buff=0.55)
        chips.move_to([0, -1.3, 0])

        lng_line = Text(
            "+ ⅕ of global LNG trade · mostly Qatari",
            font=BODY_FONT, color=VERIFIED, slant="ITALIC",
        ).scale(0.42)
        lng_line.move_to([0, -2.3, 0])

        cap = source_caption("U.S. EIA · Today In Energy · 2024")

        self.play(FadeIn(kicker, run_time=0.4))
        self.add(oil_n)
        self.play(FadeIn(oil_unit, run_time=0.3))
        self.play(oil_track.animate.set_value(20_000_000), run_time=2.2)
        self.wait(0.3)
        for chip in chips:
            self.play(FadeIn(chip, shift=RIGHT * 0.1, run_time=0.25))
        self.wait(0.3)
        self.play(FadeIn(lng_line, run_time=0.5))
        self.play(FadeIn(cap, run_time=0.3))
        held = (
            0.4 + 0.3 + 2.2 + 0.3
            + 6 * 0.25
            + 0.3 + 0.5 + 0.3
        )
        self.wait(max(25.0 - held, 0.5))
        self.remove(oil_n)
        self.play(
            FadeOut(VGroup(kicker, oil_unit, chips, lng_line, cap)),
            run_time=0.6,
        )


# -- Scene 4 -----------------------------------------------------------------
class Cables(Scene):
    """0:55–1:30 — three cable arcs, all routed in Omani waters."""

    def construct(self) -> None:
        self.camera.background_color = BG
        self.add(_mark())

        # Re-use the same stylised strait outline from Scene 2, muted
        # so the cables (the point of this scene) read on top.
        iran_coast = DashedLine(
            [-6.0, 1.4, 0], [6.0, 1.0, 0],
            color=MUTED, stroke_width=1, dash_length=0.18,
        )
        arabia_coast = DashedLine(
            [-6.0, -1.4, 0], [6.0, -1.0, 0],
            color=MUTED, stroke_width=1, dash_length=0.18,
        )
        iran_lbl = Text("IRAN", font=MONO_FONT, color=MUTED).scale(0.4)
        iran_lbl.move_to([-5.2, 1.9, 0])
        arabia_lbl = Text("OMAN / GULF STATES", font=MONO_FONT, color=MUTED).scale(0.35)
        arabia_lbl.move_to([5.0, -1.9, 0])

        # Three coloured cable arcs hugging the lower (Omani) shoreline.
        # CurvedArrow with shallow curvature gives a clean cable look.
        cable_aae1 = CurvedArrow(
            start_point=[-5.5, -0.8, 0],
            end_point=[5.5, -0.7, 0],
            color=VERIFIED,
            angle=0.55,
            stroke_width=4,
            tip_length=0.18,
        )
        cable_falcon = CurvedArrow(
            start_point=[-5.5, -0.95, 0],
            end_point=[5.5, -0.85, 0],
            color=FG,
            angle=0.45,
            stroke_width=3,
            tip_length=0.16,
        )
        cable_gbi = CurvedArrow(
            start_point=[-5.5, -1.1, 0],
            end_point=[5.5, -1.0, 0],
            color=SUPPORTING,
            angle=0.35,
            stroke_width=3,
            tip_length=0.16,
        )

        aae1_lbl = Text("AAE-1", font=MONO_FONT, color=VERIFIED, weight="BOLD").scale(0.36)
        aae1_lbl.move_to([-4.8, -0.4, 0])
        falcon_lbl = Text("FALCON", font=MONO_FONT, color=FG).scale(0.32)
        falcon_lbl.move_to([0.0, -0.55, 0])
        gbi_lbl = Text("GULF BRIDGE", font=MONO_FONT, color=SUPPORTING).scale(0.32)
        gbi_lbl.move_to([4.0, -0.7, 0])

        l3 = lower_third("17 cables · all routed in Omani waters")

        cap = source_caption("TeleGeography · Submarine Cable Map · Apr 2026")

        # Build the scene.
        self.play(FadeIn(iran_lbl, run_time=0.3), FadeIn(arabia_lbl, run_time=0.3))
        self.play(Create(iran_coast, run_time=0.6), Create(arabia_coast, run_time=0.6))
        self.play(Create(cable_aae1, run_time=0.7))
        self.play(FadeIn(aae1_lbl, run_time=0.3))
        self.play(Create(cable_falcon, run_time=0.7))
        self.play(FadeIn(falcon_lbl, run_time=0.3))
        self.play(Create(cable_gbi, run_time=0.7))
        self.play(FadeIn(gbi_lbl, run_time=0.3))
        self.play(FadeIn(l3, run_time=0.5))
        self.play(FadeIn(cap, run_time=0.3))
        held = (
            0.3 + 0.6
            + 0.7 + 0.3
            + 0.7 + 0.3
            + 0.7 + 0.3
            + 0.5 + 0.3
        )
        self.wait(max(35.0 - held, 0.5))
        self.play(
            FadeOut(VGroup(
                iran_lbl, arabia_lbl, iran_coast, arabia_coast,
                cable_aae1, cable_falcon, cable_gbi,
                aae1_lbl, falcon_lbl, gbi_lbl,
                l3, cap,
            )),
            run_time=0.6,
        )
