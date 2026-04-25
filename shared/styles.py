"""Reusable styles for the channel.

Single source of truth for colors and fonts. Import from here in every
scene module — never hardcode colors.
"""
from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    ManimColor,
    Rectangle,
    Text,
    VGroup,
)

BG = ManimColor("#0e0e10")
FG = ManimColor("#e8e8ea")
ACCENT = ManimColor("#7c5cff")
MUTED = ManimColor("#6b6b76")

TITLE_FONT = "Inter"
BODY_FONT = "Inter"
MONO_FONT = "JetBrains Mono"


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
