"""Pilot episode — Operation Gladio. Full 6-minute episode, 10 scenes.

Render an individual scene preview:
    ./pipeline/render.sh episodes/001-pilot/scene.py Hook -ql

Render every scene at -ql (one process):
    PYTHONPATH=. .venv/bin/manim -ql episodes/001-pilot/scene.py \\
        Hook Doctrine Network Pivot Memoir Andreotti Bologna \\
        Belgium Disclosed Filed

All colors and typography come from shared/styles. No hardcoded colors here.
No LaTeX (no MathTex/Tex) — host has no TeX.
"""
from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    Line,
    Rectangle,
    Scene,
    Text,
    Transform,
    ValueTracker,
    VGroup,
    Write,
    always_redraw,
)


def tracked_int(
    tracker: ValueTracker,
    *,
    center,
    font: str,
    color,
    scale: float = 1.0,
    weight: str = "BOLD",
):
    """Always-redrawn integer Text bound to a ValueTracker.

    Avoids Manim's Integer/DecimalNumber, which require LaTeX.
    """
    return always_redraw(
        lambda: Text(
            f"{int(tracker.get_value())}",
            font=font,
            color=color,
            weight=weight,
        )
        .scale(scale)
        .move_to(center)
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
    document_card,
    episode_mark,
    lower_third,
    source_caption,
    western_europe_outline,
)


EP_NUM = 1
EP_SLUG = "Gladio"


def _mark() -> VGroup:
    """Shorthand for this episode's persistent brand mark."""
    return episode_mark(EP_NUM, EP_SLUG)


# -- Scene 1 -----------------------------------------------------------------
class Hook(Scene):
    """0:00–0:08 — title + DECLASSIFIED stamp."""

    def construct(self) -> None:
        self.camera.background_color = BG
        self.add(_mark())

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
        self.add(_mark())

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
        # Hold to end of 17s scene window (after ~4.5s of animation above).
        self.wait(11.5)
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
        self.add(_mark())

        # Frame label so viewers know what they're looking at.
        frame = Text(
            "stay-behind networks · western europe",
            font=MONO_FONT,
            color=MUTED,
        ).scale(0.35)
        frame.to_edge(UP, buff=0.4)
        self.play(FadeIn(frame, run_time=0.3))

        # Stylised Western Europe outline behind the pins.
        outline = western_europe_outline()
        self.play(Create(outline, run_time=0.7))

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
                    "622 members · 127 arms caches",
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

        # Hold the full map for the rest of the 20s scene window.
        self.wait(12.5)
        self.play(
            FadeOut(VGroup(frame, outline, *confirmed_pins, *later_pins, primary_label, cap)),
            run_time=0.5,
        )


# -- Scene 4 -----------------------------------------------------------------
class Pivot(Scene):
    """0:45–1:00 — date range + tease into the rest of the video."""

    def construct(self) -> None:
        self.camera.background_color = BG
        self.add(_mark())

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


# -- Scene 5 -----------------------------------------------------------------
class Memoir(Scene):
    """1:00–1:45 — Colby's Honorable Men, where the network began."""

    def construct(self) -> None:
        self.camera.background_color = BG
        self.add(_mark())

        # Mock book cover on the left.
        cover = Rectangle(
            width=3.0, height=4.2,
            color=MUTED, stroke_width=2, fill_opacity=0,
        )
        cover.shift(LEFT * 3.5)
        title_top = Text("HONORABLE MEN", font=MONO_FONT, color=FG, weight="BOLD").scale(0.32)
        title_sub = Text("MY LIFE IN THE CIA", font=MONO_FONT, color=MUTED).scale(0.22)
        author = Text("WILLIAM E. COLBY", font=MONO_FONT, color=ACCENT).scale(0.28)
        year = Text("1978", font=MONO_FONT, color=MUTED).scale(0.32)
        title_top.move_to(cover.get_top() + DOWN * 0.7)
        title_sub.next_to(title_top, DOWN, buff=0.18)
        author.move_to(cover.get_center() + DOWN * 0.4)
        year.move_to(cover.get_bottom() + UP * 0.4)
        book = VGroup(cover, title_top, title_sub, author, year)

        # Pull-quote on the right.
        q1 = Text("“Sweden, 1951.", font=BODY_FONT, color=FG).scale(0.45)
        q2 = Text("Italy, 1953.", font=BODY_FONT, color=FG).scale(0.45)
        q3 = Text("The cells were buried with weapons.", font=BODY_FONT, color=FG).scale(0.45)
        q4 = Text("They were trained for a war that never came.”", font=BODY_FONT, color=FG).scale(0.45)
        quote = VGroup(q1, q2, q3, q4).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        quote.shift(RIGHT * 2.5)

        cap = source_caption("Colby, Honorable Men (Simon & Schuster, 1978)")

        self.play(Create(cover, run_time=0.6))
        self.play(
            FadeIn(title_top, run_time=0.3),
            FadeIn(title_sub, run_time=0.3),
        )
        self.play(FadeIn(author, run_time=0.3), FadeIn(year, run_time=0.3))
        self.wait(0.4)
        for line in quote:
            self.play(FadeIn(line, shift=RIGHT * 0.15, run_time=0.45))
            self.wait(0.4)
        self.play(FadeIn(cap, run_time=0.4))
        # Slow drift on the book + quote group to keep the long hold alive.
        whole = VGroup(book, quote)
        self.play(
            whole.animate(run_time=36.0, rate_func=lambda t: t)
                 .shift(UP * 0.12)
                 .scale(1.018),
        )
        self.play(
            FadeOut(VGroup(book, quote, cap)),
            run_time=0.6,
        )


# -- Scene 6 -----------------------------------------------------------------
class Andreotti(Scene):
    """1:45–2:45 — the disclosure speech and EU resolution."""

    def construct(self) -> None:
        self.camera.background_color = BG
        self.add(_mark())

        date_main = Text("24 · X · 1990", font=MONO_FONT, color=ACCENT, weight="BOLD").scale(1.4)
        date_main.shift(UP * 2.6)

        speaker = Text("GIULIO ANDREOTTI — to the Italian parliament",
                       font=MONO_FONT, color=MUTED).scale(0.32)
        speaker.next_to(date_main, DOWN, buff=0.3)

        quote = VGroup(
            Text("“a structure of information,",
                 font=BODY_FONT, color=FG, slant="ITALIC").scale(0.55),
            Text("response, and safeguard”",
                 font=BODY_FONT, color=FG, slant="ITALIC").scale(0.55),
        ).arrange(DOWN, buff=0.18)
        quote.shift(UP * 0.4)

        # Numbers row: 622 members · 127 caches.
        members_track = ValueTracker(0)
        caches_track = ValueTracker(0)
        members_pos = [-2.5, -1.6, 0]
        caches_pos = [2.5, -1.6, 0]
        members_n = tracked_int(members_track, center=members_pos,
                                font=MONO_FONT, color=ACCENT, scale=1.4)
        caches_n = tracked_int(caches_track, center=caches_pos,
                               font=MONO_FONT, color=ACCENT, scale=1.4)
        members_lbl = Text("members", font=MONO_FONT, color=MUTED).scale(0.4)
        members_lbl.move_to([members_pos[0], members_pos[1] - 0.85, 0])
        caches_lbl = Text("arms caches dismantled", font=MONO_FONT, color=MUTED).scale(0.4)
        caches_lbl.move_to([caches_pos[0], caches_pos[1] - 0.85, 0])

        cap = source_caption("Andreotti report to Commissione Stragi, 24 Oct 1990")

        # Beat 1: date + speaker.
        self.play(Write(date_main, run_time=0.7))
        self.play(FadeIn(speaker, run_time=0.4))
        self.wait(0.6)
        # Beat 2: quote.
        self.play(Write(quote[0], run_time=0.6))
        self.play(Write(quote[1], run_time=0.6))
        self.wait(0.5)
        # Beat 3: numbers tick up.
        self.add(members_n, caches_n)
        self.play(FadeIn(members_lbl, run_time=0.3), FadeIn(caches_lbl, run_time=0.3))
        self.play(
            members_track.animate.set_value(622),
            caches_track.animate.set_value(127),
            run_time=1.6,
        )
        self.play(FadeIn(cap, run_time=0.4))
        self.wait(2.0)

        # Beat 4: dissolve to EU resolution card.
        self.remove(members_n, caches_n)
        self.play(
            FadeOut(VGroup(date_main, speaker, quote, members_lbl, caches_lbl, cap)),
            run_time=0.5,
        )

        eu_date = Text("22 · XI · 1990", font=MONO_FONT, color=ACCENT, weight="BOLD").scale(1.4)
        eu_date.shift(UP * 1.0)
        eu_label = Text("European Parliament Resolution", font=BODY_FONT, color=FG).scale(0.6)
        eu_label.next_to(eu_date, DOWN, buff=0.5)
        oj_ref = Text("OJ C 324/201", font=MONO_FONT, color=MUTED).scale(0.45)
        oj_ref.next_to(eu_label, DOWN, buff=0.25)
        eu_quote = Text("“…escaped all democratic controls.”",
                        font=BODY_FONT, color=SUPPORTING, slant="ITALIC").scale(0.5)
        eu_quote.next_to(oj_ref, DOWN, buff=0.7)

        cap2 = source_caption("OJ C 324, 24 Dec 1990, p. 201")

        self.play(Write(eu_date, run_time=0.6))
        self.play(FadeIn(eu_label, run_time=0.4), FadeIn(oj_ref, run_time=0.4))
        self.wait(0.4)
        self.play(FadeIn(eu_quote, run_time=0.5))
        self.play(FadeIn(cap2, run_time=0.4))
        # Slow drift on the EU card group to keep the long hold alive.
        eu_group = VGroup(eu_date, eu_label, oj_ref, eu_quote)
        self.play(
            eu_group.animate(run_time=44.0, rate_func=lambda t: t)
                    .shift(UP * 0.10)
                    .scale(1.012),
        )
        self.play(
            FadeOut(VGroup(eu_date, eu_label, oj_ref, eu_quote, cap2)),
            run_time=0.6,
        )


# -- Scene 7 -----------------------------------------------------------------
class Bologna(Scene):
    """2:45–3:45 — Bologna massacre + 2021 'State massacre' ruling."""

    def construct(self) -> None:
        self.camera.background_color = BG
        self.add(_mark())

        date = Text("2 · VIII · 1980", font=MONO_FONT, color=ACCENT, weight="BOLD").scale(1.3)
        date.shift(UP * 2.6)
        time_t = Text("10:25 a.m. · Bologna Centrale", font=MONO_FONT, color=MUTED).scale(0.4)
        time_t.next_to(date, DOWN, buff=0.25)

        # Death counter.
        counter_track = ValueTracker(0)
        counter_pos = [0, 0.2, 0]
        counter = tracked_int(counter_track, center=counter_pos,
                              font=MONO_FONT, color=ACCENT, scale=2.4)
        killed_lbl = Text("killed", font=MONO_FONT, color=MUTED).scale(0.5)
        killed_lbl.move_to([0, -1.2, 0])

        cap = source_caption("Wikipedia: Bologna massacre / Britannica")

        self.play(Write(date, run_time=0.6), FadeIn(time_t, run_time=0.6))
        self.wait(0.4)
        self.add(counter)
        self.play(FadeIn(killed_lbl, run_time=0.3))
        self.play(counter_track.animate.set_value(85), run_time=2.0)
        self.play(FadeIn(cap, run_time=0.4))
        self.wait(1.5)

        # Fade counter, bring up split columns.
        self.remove(counter)
        self.play(
            FadeOut(VGroup(killed_lbl, cap)),
            FadeOut(time_t),
            date.animate.scale(0.6).to_edge(UP, buff=0.4),
            run_time=0.6,
        )

        left_h = Text("CONVICTED — Italian Supreme Court",
                      font=MONO_FONT, color=ACCENT, weight="BOLD").scale(0.32)
        left_names = VGroup(
            Text("Valerio Fioravanti  — life, 1995", font=BODY_FONT, color=FG).scale(0.34),
            Text("Francesca Mambro    — life, 1995", font=BODY_FONT, color=FG).scale(0.34),
            Text("Luigi Ciavardini    — 30 yrs, 2007", font=BODY_FONT, color=FG).scale(0.34),
            Text("Gilberto Cavallini  — life, 2023", font=BODY_FONT, color=FG).scale(0.34),
            Text("Paolo Bellini       — life, 2022", font=BODY_FONT, color=FG).scale(0.34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        left_col = VGroup(left_h, left_names).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        left_col.shift(LEFT * 6.0 + DOWN * 0.4)
        # Anchor the left column to the left edge of the frame.
        left_col.to_edge(LEFT, buff=0.6).shift(DOWN * 0.4)

        right_h_a = Text("2021 — Court of Appeal:",
                         font=MONO_FONT, color=ACCENT, weight="BOLD").scale(0.32)
        right_h_b = Text("“una strage di Stato”",
                         font=BODY_FONT, color=ACCENT, slant="ITALIC", weight="BOLD").scale(0.40)
        right_h = VGroup(right_h_a, right_h_b).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        right_names = VGroup(
            Text("Licio Gelli         — P2 lodge", font=BODY_FONT, color=FG).scale(0.34),
            Text("F. U. D'Amato       — NATO / Stay-Behind", font=BODY_FONT, color=FG).scale(0.34),
            Text("Umberto Ortolani    — P2 lodge", font=BODY_FONT, color=FG).scale(0.34),
            Text("Mario Tedeschi      — cover-up", font=BODY_FONT, color=FG).scale(0.34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        right_col = VGroup(right_h, right_names).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        right_col.to_edge(RIGHT, buff=0.6).shift(DOWN * 0.4)

        cap2 = source_caption("ANSA, 8 Jan 2021")

        self.play(FadeIn(left_h, shift=RIGHT * 0.2, run_time=0.4))
        for n in left_names:
            self.play(FadeIn(n, shift=RIGHT * 0.15, run_time=0.25))
        self.play(FadeIn(right_h_a, shift=LEFT * 0.2, run_time=0.4))
        self.play(FadeIn(right_h_b, run_time=0.4))
        for n in right_names:
            self.play(FadeIn(n, shift=LEFT * 0.15, run_time=0.25))
        self.play(FadeIn(cap2, run_time=0.4))
        self.wait(60.0 - (0.6 + 0.4 + 0.3 + 2.0 + 0.4 + 1.5 + 0.6 + 0.4 + 5 * 0.25 + 0.4 + 0.4 + 4 * 0.25 + 0.4))
        self.play(
            FadeOut(VGroup(date, left_col, right_col, cap2)),
            run_time=0.6,
        )


# -- Scene 8 -----------------------------------------------------------------
class Belgium(Scene):
    """3:45–4:45 — SDRA-VIII and the Brabant case."""

    def construct(self) -> None:
        self.camera.background_color = BG
        self.add(_mark())

        codename = Text("SDRA-VIII", font=MONO_FONT, color=ACCENT, weight="BOLD").scale(1.6)
        codename.shift(UP * 2.4)

        expansion = Text(
            "Service de Documentation, de Renseignements et d'Action VIII",
            font=BODY_FONT, color=MUTED,
        ).scale(0.42)
        expansion.next_to(codename, DOWN, buff=0.3)

        disclosed = Text("disclosed: 7 · XI · 1990", font=MONO_FONT, color=ACCENT).scale(0.45)
        disclosed.next_to(expansion, DOWN, buff=0.3)

        # Brabant timeline: years 1982-1985 stretched horizontally.
        timeline_y = -1.0
        line = Line([-4.5, timeline_y, 0], [4.5, timeline_y, 0], color=MUTED, stroke_width=2)
        years = ["1982", "1983", "1984", "1985"]
        year_marks = VGroup()
        for i, y in enumerate(years):
            x = -4.5 + (9.0 * i / (len(years) - 1))
            tick = Line([x, timeline_y - 0.1, 0], [x, timeline_y + 0.1, 0], color=MUTED)
            label = Text(y, font=MONO_FONT, color=MUTED).scale(0.32)
            label.next_to(tick, DOWN, buff=0.15)
            year_marks.add(VGroup(tick, label))

        brabant_h = Text("Brabant attacks", font=BODY_FONT, color=FG).scale(0.5)
        brabant_h.move_to([0, timeline_y + 0.6, 0])

        deaths_track = ValueTracker(0)
        deaths_pos = [3.4, timeline_y - 1.2, 0]
        deaths = tracked_int(deaths_track, center=deaths_pos,
                             font=MONO_FONT, color=ACCENT, scale=1.4)
        deaths_lbl = Text("dead", font=MONO_FONT, color=MUTED).scale(0.38)
        deaths_lbl.move_to([deaths_pos[0] + 1.0, deaths_pos[1], 0])

        amber = Text(
            "Belgian parliamentary inquiry: no substantive evidence linking SDRA-VIII to the killings",
            font=BODY_FONT, color=SUPPORTING,
        ).scale(0.32)
        amber.move_to([0, -3.1, 0])

        cap = source_caption("Wikipedia: Brabant killers / Belgian Senate, 1991")

        self.play(Write(codename, run_time=0.7))
        self.play(FadeIn(expansion, run_time=0.5))
        self.play(FadeIn(disclosed, run_time=0.4))
        self.wait(0.5)
        self.play(Create(line, run_time=0.6))
        self.play(*[FadeIn(m, run_time=0.25) for m in year_marks])
        self.play(FadeIn(brabant_h, shift=DOWN * 0.1, run_time=0.4))
        self.add(deaths)
        self.play(FadeIn(deaths_lbl, run_time=0.3))
        self.play(deaths_track.animate.set_value(28), run_time=1.4)
        self.wait(0.4)
        self.play(FadeIn(amber, run_time=0.5))
        self.play(FadeIn(cap, run_time=0.3))
        self.wait(60.0 - (0.7 + 0.5 + 0.4 + 0.5 + 0.6 + 1.0 + 0.4 + 0.3 + 1.4 + 0.4 + 0.5 + 0.3))
        self.remove(deaths)
        self.play(
            FadeOut(VGroup(codename, expansion, disclosed, line, year_marks,
                           brabant_h, deaths_lbl, amber, cap)),
            run_time=0.6,
        )


# -- Scene 9 -----------------------------------------------------------------
class Disclosed(Scene):
    """4:45–5:30 — country-by-country disclosure timeline."""

    DISCLOSURES = [
        ("1990", "Italy. Belgium. Switzerland."),
        ("1991", "France. Denmark. Greece."),
        ("1996", "Norway — Lund Commission."),
        ("2000", "Pellegrino Report — Italian Senate."),
        ("2014", "Sweden — 'Sveaborg' confirmed."),
    ]

    def construct(self) -> None:
        self.camera.background_color = BG
        self.add(_mark())

        header = Text("THE DISCLOSURES", font=MONO_FONT, color=MUTED).scale(0.45)
        header.to_edge(UP, buff=0.5)

        # Year ticker via ValueTracker.
        year_tracker = ValueTracker(1990)
        year_display = always_redraw(
            lambda: Text(
                f"{int(year_tracker.get_value()):4d}",
                font=MONO_FONT,
                color=ACCENT,
                weight="BOLD",
            ).scale(2.0).move_to([0, 1.6, 0])
        )

        cap = source_caption("Andreotti report (1990); Pellegrino Report (2000); Swedish MoD (2014)")

        self.play(FadeIn(header, run_time=0.4))
        self.add(year_display)
        self.wait(0.3)

        # Stack of revealed lines.
        revealed = VGroup()
        revealed_anchor = [0, -0.4, 0]

        target_years = [1990, 1991, 1996, 2000, 2014]
        for i, (year_str, desc) in enumerate(self.DISCLOSURES):
            target = target_years[i]
            self.play(year_tracker.animate.set_value(target),
                      run_time=1.2 if i > 0 else 0.4,
                      rate_func=lambda t: t)
            row_year = Text(year_str, font=MONO_FONT, color=ACCENT, weight="BOLD").scale(0.5)
            row_desc = Text(desc, font=BODY_FONT, color=FG).scale(0.45)
            row = VGroup(row_year, row_desc).arrange(RIGHT, buff=0.5)
            if len(revealed) == 0:
                row.move_to(revealed_anchor)
            else:
                row.next_to(revealed[-1], DOWN, aligned_edge=LEFT, buff=0.25)
            revealed.add(row)
            self.play(FadeIn(row, shift=RIGHT * 0.2, run_time=0.4))
            self.wait(0.4)

        self.play(FadeIn(cap, run_time=0.4))
        # Hold to scene end (~45s total).
        self.wait(45.0 - (0.4 + 0.3 + 0.4 + 4 * 1.2 + 5 * 0.8 + 0.4))
        self.play(
            FadeOut(VGroup(header, year_display, revealed, cap)),
            run_time=0.6,
        )


# -- Scene 10 ----------------------------------------------------------------
class Filed(Scene):
    """5:30–6:00 — folder closes, Operation Northwoods tease, 'Filed.'"""

    def construct(self) -> None:
        self.camera.background_color = BG
        self.add(_mark())

        # Centered closing card.
        what_we_dont_know = Text(
            "What we still do not know",
            font=BODY_FONT, color=MUTED, slant="ITALIC",
        ).scale(0.55)
        what_we_dont_know.shift(UP * 2.4)

        items = VGroup(
            Text("— the British network", font=BODY_FONT, color=FG).scale(0.42),
            Text("— Turkey's 'Counter-Guerrilla'", font=BODY_FONT, color=FG).scale(0.42),
            Text("— fourteen national archives, still classified", font=BODY_FONT, color=FG).scale(0.42),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        items.next_to(what_we_dont_know, DOWN, buff=0.5)

        self.play(FadeIn(what_we_dont_know, run_time=0.6))
        for i in items:
            self.play(FadeIn(i, shift=RIGHT * 0.1, run_time=0.35))
            self.wait(0.15)

        self.wait(1.2)

        # Manila folder slides up to "close" the dossier.
        folder = Rectangle(
            width=16.0, height=10.0,
            color=ACCENT, fill_color=BG, fill_opacity=1, stroke_width=4,
        )
        folder.shift(DOWN * 12.0)  # off-screen below
        self.add(folder)
        self.play(folder.animate.shift(UP * 12.0), run_time=0.9)

        # Stamp swap: DECLASSIFIED  →  FILED.
        stamp_text = Text("FILED.", font=MONO_FONT, color=ACCENT, weight="BOLD").scale(1.5)
        stamp_text.rotate(-0.08)

        tease = Text(
            "Next dossier: OPERATION NORTHWOODS",
            font=MONO_FONT, color=FG,
        ).scale(0.5)
        tease.next_to(stamp_text, DOWN, buff=0.6)
        tease_sub = Text(
            "the false flag the Pentagon wrote down",
            font=BODY_FONT, color=MUTED, slant="ITALIC",
        ).scale(0.4)
        tease_sub.next_to(tease, DOWN, buff=0.2)

        self.play(FadeIn(stamp_text, scale=0.7, run_time=0.6))
        self.play(FadeIn(tease, run_time=0.5), FadeIn(tease_sub, run_time=0.5))
        self.wait(20.0)  # hold to give VO time + dramatic close
        self.play(
            FadeOut(VGroup(stamp_text, tease, tease_sub, folder)),
            run_time=0.8,
        )
