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
    ManimColor,
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
