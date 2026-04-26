"""Reusable styles for The Dossier.

Single source of truth for colors and fonts. Import from here in every
scene module — never hardcode colors.

Brand grammar:
    BG / FG / MUTED  → neutral surface
    ACCENT           → redaction red, primary brand mark, "damning" emphasis
    SUPPORTING       → archive amber, "claim / unverified / developing"
    VERIFIED         → cross-checked teal, "sourced fact"
    REDACTED         → deep black bar overlay (used by `redaction_bar`)
"""
from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    FadeIn,
    Line,
    ManimColor,
    Polygon,
    Rectangle,
    Text,
    VGroup,
)

# --- Palette ------------------------------------------------------------------
BG = ManimColor("#0e0e10")
FG = ManimColor("#e8e8ea")
MUTED = ManimColor("#6b6b76")

ACCENT = ManimColor("#d63b2f")        # redaction red — primary brand
SUPPORTING = ManimColor("#e3a72f")    # archive amber — claim / developing
VERIFIED = ManimColor("#3aa7a0")      # teal — verified, sourced fact
REDACTED = ManimColor("#000000")      # pure black for redaction bars

# --- Typography ---------------------------------------------------------------
TITLE_FONT = "Inter"
BODY_FONT = "Inter"
MONO_FONT = "JetBrains Mono"


# --- Helpers ------------------------------------------------------------------
def title_card(title: str, subtitle: str | None = None) -> VGroup:
    """Centered title with optional subtitle below."""
    t = Text(title, font=TITLE_FONT, color=FG, weight="BOLD").scale(1.2)
    if subtitle is None:
        return VGroup(t)
    s = Text(subtitle, font=BODY_FONT, color=MUTED).scale(0.5)
    s.next_to(t, DOWN, buff=0.4)
    return VGroup(t, s)


def lower_third(label: str, source: str | None = None) -> VGroup:
    """Bottom-left label with accent bar; optional source citation."""
    bar = Rectangle(width=0.1, height=0.6, color=ACCENT, fill_opacity=1)
    label_t = Text(label, font=BODY_FONT, color=FG).scale(0.45)
    label_t.next_to(bar, RIGHT, buff=0.2)
    group = VGroup(bar, label_t)
    if source:
        src = Text(source, font=BODY_FONT, color=MUTED).scale(0.3)
        src.next_to(label_t, DOWN, aligned_edge=LEFT, buff=0.1)
        group.add(src)
    group.to_corner(DOWN + LEFT, buff=0.6)
    return group


def classification_stamp(label: str = "DECLASSIFIED") -> VGroup:
    """Top-right red stamp. Use sparingly — once per scene at most."""
    txt = Text(label, font=MONO_FONT, color=ACCENT, weight="BOLD").scale(0.45)
    border = Rectangle(
        width=txt.width + 0.4,
        height=txt.height + 0.25,
        color=ACCENT,
        stroke_width=3,
    )
    border.move_to(txt)
    group = VGroup(border, txt)
    group.rotate(-0.12)  # slight tilt — like a real stamp
    group.to_corner(UP + RIGHT, buff=0.5)
    return group


def redaction_bar(width: float = 2.0, height: float = 0.35) -> Rectangle:
    """Solid black bar — overlay on text to redact it."""
    return Rectangle(
        width=width,
        height=height,
        color=REDACTED,
        fill_opacity=1.0,
        stroke_width=0,
    )


def source_caption(source: str) -> Text:
    """Tiny muted citation, intended for bottom-right of a scene."""
    cap = Text(f"src: {source}", font=MONO_FONT, color=MUTED).scale(0.25)
    cap.to_corner(DOWN + RIGHT, buff=0.4)
    return cap


def episode_mark(episode_no: int, slug: str) -> VGroup:
    """Persistent bottom-left brand mark.

    Renders as: `[red bar] DOSSIER · 001  GLADIO`. Add at the start of a
    scene, leave on screen the whole time. Width is fixed regardless of
    slug length (slug truncated visually, not measured).
    """
    bar = Rectangle(width=0.07, height=0.32, color=ACCENT, fill_opacity=1, stroke_width=0)
    label = Text(
        f"DOSSIER · {episode_no:03d}",
        font=MONO_FONT,
        color=MUTED,
        weight="BOLD",
    ).scale(0.28)
    sep = Text("·", font=MONO_FONT, color=MUTED).scale(0.32)
    name = Text(slug.upper(), font=MONO_FONT, color=MUTED).scale(0.28)
    label.next_to(bar, RIGHT, buff=0.15)
    sep.next_to(label, RIGHT, buff=0.18)
    name.next_to(sep, RIGHT, buff=0.18)
    group = VGroup(bar, label, sep, name)
    group.to_corner(UP + LEFT, buff=0.4)
    return group


def document_card(
    headline: str,
    body_lines: list[str],
    classification: str = "TOP SECRET",
    citation: str | None = None,
) -> VGroup:
    """Stylised typewritten-page card.

    Use as a stand-in for a captured PDF page when network primary-source
    capture isn't available. Renders a manila-edged rectangle with a
    classification stamp top-right of the page, a centered headline, and
    monospace body lines beneath.
    """
    page = Rectangle(
        width=8.0,
        height=5.4,
        color=MUTED,
        stroke_width=2,
        fill_color=BG,
        fill_opacity=1,
    )

    head = Text(headline, font=MONO_FONT, color=FG, weight="BOLD").scale(0.42)
    head.move_to(page.get_top() + DOWN * 0.85)

    # Classification stamp on the page itself.
    stamp_txt = Text(classification, font=MONO_FONT, color=ACCENT, weight="BOLD").scale(0.32)
    stamp_box = Rectangle(
        width=stamp_txt.width + 0.3,
        height=stamp_txt.height + 0.18,
        color=ACCENT,
        stroke_width=2,
    )
    stamp_box.move_to(stamp_txt)
    stamp = VGroup(stamp_box, stamp_txt).rotate(-0.08)
    stamp.move_to(page.get_corner(UP + RIGHT) + LEFT * 1.1 + DOWN * 0.55)

    body = VGroup(*[
        Text(line, font=MONO_FONT, color=FG).scale(0.32)
        for line in body_lines
    ]).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
    body.next_to(head, DOWN, aligned_edge=LEFT, buff=0.55)
    body.shift(LEFT * (page.width / 2 - 0.6 - body.get_left()[0] + page.get_center()[0]))

    group = VGroup(page, head, stamp, body)
    if citation is not None:
        cite = Text(citation, font=MONO_FONT, color=MUTED).scale(0.24)
        cite.move_to(page.get_bottom() + UP * 0.35)
        group.add(cite)
    return group


def western_europe_outline(scale: float = 1.0) -> Polygon:
    """Coarse stylised polygon of Western Europe.

    Vertices roughly trace the western European coastline (Norway south
    through Iberia) and the eastern edge along Germany/Italy. Faint muted
    stroke, no fill. Pin coordinates in the Network scene are tuned to sit
    inside this outline.

    Coordinate system: same as the scene frame (~14 units wide × 8 tall),
    centered at origin. Apply `.scale(...)` after construction if needed.
    """
    pts = [
        # North — Norway / Sweden / Finland sweep
        (-2.4,  3.4),
        (-0.8,  3.6),
        ( 0.8,  3.6),
        ( 2.2,  3.2),
        # Eastern frontier south through Finland / Baltics / Germany
        ( 2.6,  2.0),
        ( 2.4,  0.8),    # central east, past German border
        ( 2.6,  0.0),
        # Eastern bulge toward Greece / Turkey (we include them)
        ( 3.2, -0.4),
        ( 3.8, -0.7),    # Turkey
        ( 4.0, -1.2),
        ( 3.0, -1.7),    # Greece tip
        # Italian boot — dip south
        ( 1.6, -1.8),
        ( 1.2, -2.5),    # Italy southern tip
        ( 0.6, -2.0),
        # Mediterranean north coast
        (-0.6, -1.6),
        (-1.8, -1.6),
        # Iberia — Spain south, Portugal west
        (-2.8, -1.4),
        (-3.6, -0.8),
        (-3.8,  0.0),
        # Atlantic France
        (-3.4,  0.8),
        # British Isles / Channel
        (-2.8,  1.6),
        (-3.2,  2.4),
        (-2.4,  3.4),
    ]
    poly = Polygon(
        *[(x * scale, y * scale, 0) for (x, y) in pts],
        color=MUTED,
        stroke_width=1.5,
        fill_opacity=0,
    )
    return poly


def slow_drift(mob, *, distance: float = 0.15, run_time: float = 8.0):
    """Return a slow drift animation suitable for keeping a static hold alive.

    Subtle upward drift with a tiny scale-up. Pair with `self.play(...)`
    instead of `self.wait(...)` during long static holds.
    """
    return mob.animate(run_time=run_time, rate_func=lambda t: t).shift(UP * distance).scale(1.015)
