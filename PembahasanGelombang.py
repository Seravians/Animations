from manim import *
from manim_physics import StandingWave
import numpy as np
import textwrap

BG_COLOR = "#080c18"
PANEL = "#111827"
PANEL_STROKE = "#24344d"
PRIMARY = BLUE_C
SECONDARY = RED_C
ACCENT = YELLOW_C
GOOD = GREEN_C
BAD = RED_C
TEXT = GREY_A
DIM = GREY_B
QUESTION_BG = "#f8fafc"
QUESTION_BAR = "#e2e8f0"
QUESTION_INK = "#0f172a"
UI_FONT = "Arial"

# Voiceover timing profile
# Rough targets from storyboard:
# Intro ~30s | Soal 1 ~3:00 | Soal 2 ~2:50 | Soal 3 ~2:10 | Soal 4 ~2:00 | Soal 5 ~2:30
QUESTION_PAUSE = 2.6          # default 2-3 second hold after each question highlight
QUESTION_SWIPE_TIME = 0.85    # slow left-to-right highlight sweep, easier to sync to VO
STEP_PAUSE = 5.2              # default pause after a reasoning/formula step
FORMULA_PAUSE = 6.5           # default pause after transformed formulas
LONG_PAUSE = 8.0
INTRO_HOLD = 17.0             # long final intro hold so total intro is around 30s

SOAL1_HIGHLIGHT_PAUSE = 4.0
SOAL1_STEP_PAUSE = 16.0
SOAL1_FORMULA_PAUSE = 17.0
SOAL1_ANSWER_PAUSE = 13.65

SOAL2_HIGHLIGHT_PAUSE = 4.0
SOAL2_SILENT_WAVE_TIME = 6.0  # storyboard note: no narration here; let the standing wave move
SOAL2_STEP_PAUSE = 13.0
SOAL2_FORMULA_PAUSE = 14.0
SOAL2_ANSWER_PAUSE = 17.2

SOAL3_HIGHLIGHT_PAUSE = 4.0
SOAL3_OSCILLATION_TIME = 9.0  # storyboard note: narrate observation during spring motion
SOAL3_STEP_PAUSE = 8.0
SOAL3_FORMULA_PAUSE = 11.0
SOAL3_ANSWER_PAUSE = 15.25

SOAL4_HIGHLIGHT_PAUSE = 4.0
SOAL4_GRAPH_PAUSE = 8.0
SOAL4_FORMULA_PAUSE = 11.0
SOAL4_ANSWER_PAUSE = 16.25

SOAL5_HIGHLIGHT_PAUSE = 4.0
SOAL5_DIAGRAM_PAUSE = 9.0
SOAL5_FORMULA_PAUSE = 11.5
SOAL5_ANSWER_PAUSE = 13.85

config.background_color = BG_COLOR


def reset_camera_frame(scene):
    if hasattr(scene.camera, "frame"):
        scene.camera.frame.set(width=config.frame_width)
        scene.camera.frame.move_to(ORIGIN)


def begin_scene(scene):
    scene.clear()
    reset_camera_frame(scene)


def end_scene(scene, run_time=1.2):
    mobs = list(scene.mobjects)
    if mobs:
        scene.play(*[FadeOut(mob) for mob in mobs], run_time=run_time)
    scene.clear()
    reset_camera_frame(scene)


def make_header(num, title):
    num_text = Text(num, font_size=22, color=PRIMARY, weight=BOLD)
    title_text = Text(title, font_size=30, color=TEXT, weight=BOLD)
    line = Line(LEFT * 2.8, RIGHT * 2.8, color=PRIMARY, stroke_width=2)
    group = VGroup(num_text, title_text, line).arrange(DOWN, buff=0.12)
    return group.to_edge(UP, buff=0.28)


def make_spring(start, end, num_coils=8, width=0.24):
    start = np.array(start)
    end = np.array(end)
    length = np.linalg.norm(end - start)
    if length < 0.1:
        return Line(start, end, color=DIM)
    direction = (end - start) / length
    perp = np.array([-direction[1], direction[0], 0])
    points = [start]
    for i in range(num_coils * 2):
        t = (i + 0.5) / (num_coils * 2)
        sign = 1 if i % 2 == 0 else -1
        points.append(start + direction * length * t + perp * width * sign)
    points.append(end)
    return VMobject(color=DIM, stroke_width=3).set_points_as_corners(points)


def text_block(text, font_size=18, color=QUESTION_INK, chars=78, weight=NORMAL):
    wrapped = textwrap.wrap(text, width=chars) or [text]
    return VGroup(
        *[
            Text(line, font=UI_FONT, font_size=font_size, color=color, weight=weight)
            for line in wrapped
        ]
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.055)


def q_math(tex, font_size=27):
    return MathTex(tex, font_size=font_size, color=QUESTION_INK)


def q_text(text, font_size=20, chars=78, weight=NORMAL):
    return text_block(text, font_size=font_size, chars=chars, weight=weight)


def make_question_screenshot(title, rows, width=11.4):
    body_rows = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    usable_width = width - 0.85
    if body_rows.width > usable_width:
        body_rows.scale_to_fit_width(usable_width)

    bar_height = 0.42
    height = max(2.25, body_rows.height + bar_height + 0.85)
    shell = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.14,
        stroke_color="#cbd5e1",
        stroke_width=2,
        fill_color=QUESTION_BG,
        fill_opacity=1,
    )
    bar = Rectangle(
        width=width - 0.06,
        height=bar_height,
        stroke_width=0,
        fill_color=QUESTION_BAR,
        fill_opacity=1,
    )
    bar.align_to(shell, UP)
    bar.shift(DOWN * (bar_height / 2 + 0.03))

    dots = VGroup(
        Dot(radius=0.045, color="#ef4444"),
        Dot(radius=0.045, color="#f59e0b"),
        Dot(radius=0.045, color="#22c55e"),
    ).arrange(RIGHT, buff=0.07)
    dots.move_to(bar.get_left() + RIGHT * 0.28)

    title_text = Text(title, font=UI_FONT, font_size=13, color="#334155")
    title_text.move_to(bar)
    title_text.align_to(shell, LEFT).shift(RIGHT * 0.55)

    body_rows.next_to(bar, DOWN, buff=0.25, aligned_edge=LEFT)
    body_rows.align_to(shell, LEFT).shift(RIGHT * 0.45)

    card = VGroup(shell, bar, dots, title_text, body_rows)
    card.rows = body_rows
    return card



def make_question_highlight(target, color=ACCENT, buff=0.075):
    rect = SurroundingRectangle(target, color=color, buff=buff, stroke_width=2)
    rect.set_fill(color, opacity=0.28)
    rect.set_stroke(color, opacity=0.9, width=2)
    return rect


def _swipe_single_highlight(scene, target, color=ACCENT, run_time=0.55, buff=0.075):
    full = make_question_highlight(target, color, buff=buff)
    left_anchor = full.get_left()

    def update(mob, alpha):
        mob.become(full.copy())
        mob.stretch(max(alpha, 1e-4), 0, about_point=left_anchor)

    proxy = full.copy()
    proxy.stretch(1e-4, 0, about_point=left_anchor)
    scene.play(UpdateFromAlphaFunc(proxy, update), run_time=run_time, rate_func=linear)
    return proxy


def swipe_in_highlight(scene, target, color=ACCENT, run_time=QUESTION_SWIPE_TIME):
    # q_text rows are VGroups of Text lines when text wraps — highlight each line separately.
    # The total sweep time is divided across wrapped lines so voiceover pacing stays predictable.
    # A tight buff prevents the highlight from covering two rows at once.
    if isinstance(target, VGroup) and len(target) > 1 and isinstance(target[0], Text):
        per_line_time = max(0.35, run_time / len(target))
        highlights = []
        for line in target:
            highlights.append(_swipe_single_highlight(scene, line, color, run_time=per_line_time, buff=0.02))
        return highlights
    return [_swipe_single_highlight(scene, target, color, run_time)]


def present_question(
    scene,
    header,
    question,
    highlight_indices,
    dock_width=5.35,
    highlight_pause=QUESTION_PAUSE,
    initial_pause=None,
    swipe_time=QUESTION_SWIPE_TIME,
    dock_pause=0.7,
):
    question.move_to(DOWN * 0.2)
    if question.height > 5.45:
        question.scale_to_fit_height(5.45)
        question.move_to(DOWN * 0.2)

    scene.play(FadeIn(question, shift=UP * 0.15), run_time=1.3)
    scene.wait(QUESTION_PAUSE + 0.5 if initial_pause is None else initial_pause)

    highlight = None
    for index in highlight_indices:
        if highlight is not None:
            scene.play(*[FadeOut(h) for h in highlight], run_time=0.25)
        highlight = swipe_in_highlight(scene, question.rows[index], run_time=swipe_time)
        scene.wait(highlight_pause)

    if highlight is not None:
        scene.play(*[FadeOut(h) for h in highlight], run_time=0.45)

    scale_factor = min(1, dock_width / question.width)
    scene.play(
        question.animate.scale(scale_factor).next_to(header, DOWN, buff=0.36).to_edge(LEFT, buff=0.34),
        run_time=1.3,
    )
    scene.wait(dock_pause)
    return question


def make_knowns_panel(items, title="Diketahui"):
    header = Text(title, font_size=24, color=PRIMARY, weight=BOLD)
    rows = VGroup(
        *[MathTex(item, font_size=29, color=TEXT) for item in items]
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
    content = VGroup(header, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
    if content.width > 3.7:
        content.scale_to_fit_width(3.7)
    box = RoundedRectangle(
        width=max(3.9, content.width + 0.45),
        height=content.height + 0.45,
        corner_radius=0.14,
        stroke_color=PANEL_STROKE,
        stroke_width=1.4,
        fill_color=PANEL,
        fill_opacity=0.72,
    )
    content.move_to(box)
    content.align_to(box, LEFT).shift(RIGHT * 0.25)
    return VGroup(box, content)


def place_knowns(panel, side=RIGHT, y_shift=0.2):
    panel.to_edge(side, buff=0.42).shift(UP * y_shift)
    return panel


def make_answer_box(*mobjects, color=GOOD):
    content = VGroup(*mobjects).arrange(DOWN, buff=0.18)
    box = RoundedRectangle(
        width=content.width + 0.75,
        height=content.height + 0.45,
        corner_radius=0.16,
        stroke_color=color,
        stroke_width=2.6,
        fill_color="#10231a",
        fill_opacity=0.95,
    )
    content.move_to(box)
    return VGroup(box, content)


def make_var_legend(items):
    """items: list of (latex_symbol, plain_text_description)"""
    rows = VGroup(*[
        VGroup(
            MathTex(sym, font_size=19, color=DIM),
            Text(": " + desc, font_size=16, color=DIM),
        ).arrange(RIGHT, buff=0.12, aligned_edge=DOWN)
        for sym, desc in items
    ]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    return rows


def show_knowns(scene, items, side=RIGHT, y_shift=0.25, wait_time=STEP_PAUSE):
    panel = place_knowns(make_knowns_panel(items), side=side, y_shift=y_shift)
    shift = LEFT * 0.2 if side is RIGHT else RIGHT * 0.2
    scene.play(FadeIn(panel, shift=shift), run_time=1.3)
    scene.wait(wait_time)
    return panel


class Intro(Scene):
    def construct(self):
        begin_scene(self)

        title = Text("Pembahasan Soal Fisika", font_size=52, color=TEXT, weight=BOLD)
        subtitle = Text("Gelombang dan Gerak Harmonik", font_size=34, color=PRIMARY, weight=BOLD)
        level = Text("Tingkat SMA Kelas 11", font_size=24, color=DIM)
        title_group = VGroup(title, subtitle, level).arrange(DOWN, buff=0.28).move_to(UP * 1.25)

        wave = FunctionGraph(
            lambda x: 0.35 * np.sin(1.8 * x),
            x_range=[-6, 6],
            color=ACCENT,
            stroke_width=3,
        ).shift(DOWN * 2.25)

        self.play(Write(title), run_time=2.2)
        self.wait(0.8)
        self.play(FadeIn(subtitle, shift=UP * 0.18), run_time=1.2)
        self.wait(0.6)
        self.play(FadeIn(level, shift=UP * 0.18), run_time=1.0)
        self.wait(0.5)
        self.play(Create(wave), run_time=3.5)
        self.wait(INTRO_HOLD)
        end_scene(self, run_time=1.3)


class Soal1(MovingCameraScene):
    def construct(self):
        begin_scene(self)

        header = make_header("SOAL 1", "Gelombang Berjalan")
        self.play(FadeIn(header), run_time=1.0)
        self.wait(0.5)

        question = make_question_screenshot(
            "Soal 1: Gelombang Berjalan",
            rows=[
                q_text("Gelombang transversal merambat sepanjang tali AB. Persamaan gelombang di titik B dinyatakan sebagai berikut:"),
                q_math(r"y_B = 0{,}04\sin 8\pi\!\left(t_A + \dfrac{x}{2}\right)"),
                q_text("Semua besaran menggunakan satuan dasar SI. Jika x adalah jarak AB, perhatikan pernyataan berikut:"),
                q_text("(A)  Gelombang memiliki amplitudo 4 cm"),
                q_text("(B)  Gelombang memiliki frekuensi 4 Hz"),
                q_text("(C)  Gelombang memiliki periode 0,5 sekon"),
                q_text("(D)  Cepat rambat gelombang 2 m/s"),
                q_text("Pernyataan yang benar adalah . . ."),
            ],
        )
        present_question(
            self,
            header,
            question,
            [0, 1, 3, 4, 5, 6, 7],
            dock_width=5.35,
            highlight_pause=SOAL1_HIGHLIGHT_PAUSE,
            initial_pause=3.2,
            swipe_time=0.95,
            dock_pause=1.2,
        )

        knowns = show_knowns(
            self,
            [
                r"A = 0{,}04\,\text{m}",
                r"\omega = 8\pi\,\text{rad/s}",
                r"v = 2\,\text{m/s}",
            ],
            side=RIGHT,
            y_shift=0.35,
    )
        legend = make_var_legend([
            (r"A",       "amplitudo"),
            (r"\omega",  "kecepatan sudut"),
            (r"v",       "cepat rambat"),
            (r"f",       "frekuensi"),
            (r"T",       "periode"),
        ])
        legend.next_to(knowns, DOWN, buff=0.35)
        self.play(FadeIn(legend, shift=LEFT * 0.15), run_time=0.8)
        self.wait(1.0)
        self.play(FadeOut(question), run_time=0.85)
        self.wait(0.6)

        compare_title = Text("Bandingkan bentuk persamaan", font_size=22, color=PRIMARY, weight=BOLD)
        general = MathTex(
            r"y = A \sin \omega\left(t \pm \frac{x}{v}\right)",
            font_size=34,
            color=PRIMARY,
        )
        specific = MathTex(
            r"y_B = 0{,}04\sin 8\pi\left(t_A + \frac{x}{2}\right)",
            font_size=32,
            color=TEXT,
        )
        compare = VGroup(compare_title, general, specific).arrange(DOWN, buff=0.28)
        compare.to_edge(LEFT, buff=0.72).shift(UP * 0.2)
        self.play(FadeIn(compare_title, shift=UP * 0.1), run_time=1.0)
        self.wait(2.0)
        self.play(Write(general), run_time=1.7)
        self.wait(SOAL1_FORMULA_PAUSE)
        self.play(Write(specific), run_time=1.7)
        self.wait(SOAL1_FORMULA_PAUSE + 1.0)

        checks = [
            (
                MathTex(r"A = 0{,}04\,\text{m} = 4\,\text{cm}", font_size=26, color=TEXT),
                Text("(A) Benar", font_size=18, color=GOOD, weight=BOLD),
            ),
            (
                MathTex(r"f = \frac{\omega}{2\pi} = \frac{8\pi}{2\pi} = 4\,\text{Hz}", font_size=26, color=TEXT),
                Text("(B) Benar", font_size=18, color=GOOD, weight=BOLD),
            ),
            (
                MathTex(r"T = \frac{1}{f} = \frac{1}{4} = 0{,}25\,\text{s}", font_size=26, color=TEXT),
                Text("(C) Salah", font_size=18, color=BAD, weight=BOLD),
            ),
            (
                MathTex(r"v = 2\,\text{m/s}", font_size=26, color=TEXT),
                Text("(D) Benar", font_size=18, color=GOOD, weight=BOLD),
            ),
        ]

        check_rows = VGroup(*[
            VGroup(formula, verdict).arrange(RIGHT, buff=0.45)
            for formula, verdict in checks
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        check_rows.next_to(compare, DOWN, buff=0.4, aligned_edge=LEFT)

        for row in check_rows:
            self.play(FadeIn(row, shift=UP * 0.1), run_time=0.9)
            self.wait(SOAL1_STEP_PAUSE)

        answer = make_answer_box(Text("Jawaban: A, B, dan D", font_size=28, color=GOOD, weight=BOLD))
        answer.next_to(legend, DOWN, buff=0.3)
        self.play(FadeIn(answer, scale=0.95), run_time=1.3)
        self.wait(SOAL1_ANSWER_PAUSE)

        end_scene(self, run_time=1.2)


class Soal2(MovingCameraScene):
    def construct(self):
        begin_scene(self)

        header = make_header("SOAL 2", "Gelombang Stasioner")
        self.play(FadeIn(header), run_time=1.0)
        self.wait(0.5)

        question = make_question_screenshot(
            "Soal 2: Gelombang Stasioner",
            rows=[
                q_text("Seutas tali panjang 4 m, salah satu ujungnya diikat dan ujung yang lain digetarkan terus menerus sehingga membentuk gelombang stasioner."),
                q_text("Pada tali terbentuk 2 gelombang penuh."),
                q_text("Bila diukur dari ujung terikat, maka perut yang ketiga terletak pada jarak . . ."),
            ],
        )
        present_question(
            self,
            header,
            question,
            [0, 1, 2],
            dock_width=5.25,
            highlight_pause=SOAL2_HIGHLIGHT_PAUSE,
            initial_pause=3.0,
            swipe_time=0.95,
            dock_pause=1.0,
        )

        knowns = show_knowns(
            self,
            [
                r"L = 4\,\text{m}",
                r"2\,\text{gelombang penuh}",
                r"\lambda = 2\,\text{m}",
                r"n = 3",
            ],
            side=RIGHT,
            y_shift=0.35,
        )
        legend = make_var_legend([
            (r"L",       "panjang tali"),
            (r"\lambda", "panjang gelombang"),
            (r"n",       "nomor perut"),
            (r"x_n",     "letak perut ke-n"),
        ])
        legend.next_to(knowns, DOWN, buff=0.35)
        self.play(FadeIn(legend, shift=LEFT * 0.15), run_time=0.8)
        self.wait(1.0)
        self.play(FadeOut(question), run_time=0.85)
        self.wait(0.6)

        L_screen = 5.4
        x_start = -3.45
        wave_y = -0.35
        meter_scale = L_screen / 4

        wave = StandingWave(
            n=4,
            length=L_screen,
            period=2.8,
            amplitude=0.58,
            color=ACCENT,
            stroke_width=4,
        ).shift(DOWN * 0.35)

        base_line = DashedLine(
            [x_start, wave_y, 0],
            [x_start + L_screen, wave_y, 0],
            color=DIM,
            dash_length=0.1,
        )
        fixed_end = VGroup(
            Line([x_start, wave_y - 0.55, 0], [x_start, wave_y + 0.55, 0], color=SECONDARY, stroke_width=4),
            *[
                Line(
                    [x_start - 0.22, wave_y - 0.55 + i * 0.22, 0],
                    [x_start, wave_y - 0.38 + i * 0.22, 0],
                    color=SECONDARY,
                    stroke_width=2,
                )
                for i in range(6)
            ],
        )
        fixed_label = Text("ujung terikat", font_size=18, color=SECONDARY).next_to(fixed_end, DOWN, buff=0.22)
        drive_label = Text("digetarkan", font_size=18, color=PRIMARY).next_to(
            np.array([x_start + L_screen, wave_y, 0]), DOWN, buff=0.35
        )

        self.play(Create(base_line), FadeIn(fixed_end), Write(fixed_label), Write(drive_label), run_time=1.5)
        self.wait(1.5)
        self.play(Create(wave), run_time=1.6)
        wave.start_wave()
        # VO cue: pause narration here and let the standing wave move visually.
        self.wait(SOAL2_SILENT_WAVE_TIME)

        antinode_offsets = [0.5, 1.5, 2.5, 3.5]
        dots = VGroup()
        labels = VGroup()
        for i, offset in enumerate(antinode_offsets):
            x_pos = x_start + offset * meter_scale
            dot = Dot([x_pos, wave_y, 0], color=GOOD, radius=0.085)
            label = Text(f"P{i + 1}", font_size=20, color=GOOD, weight=BOLD).next_to(dot, UP, buff=0.3)
            dots.add(dot)
            labels.add(label)

        self.play(FadeIn(dots), FadeIn(labels), run_time=1.3)
        self.wait(SOAL2_STEP_PAUSE)

        third_x = x_start + 2.5 * meter_scale
        highlight = Circle(radius=0.34, color=BAD, stroke_width=4).move_to([third_x, wave_y, 0])
        self.play(Create(highlight), run_time=0.85)
        self.wait(SOAL2_STEP_PAUSE)

        measure = DoubleArrow(
            [x_start, wave_y - 1.25, 0],
            [third_x, wave_y - 1.25, 0],
            color=ACCENT,
            stroke_width=3,
            buff=0,
        )
        measure_label = MathTex(r"x_3 = 2{,}5\,\text{m}", font_size=30, color=ACCENT).next_to(measure, DOWN, buff=0.18)
        self.play(Create(measure), Write(measure_label), run_time=1.4)
        self.wait(SOAL2_STEP_PAUSE)

        wave.stop_wave()
        self.play(
            FadeOut(VGroup(wave, base_line, fixed_end, fixed_label, drive_label, dots, labels, highlight, measure, measure_label)),
            run_time=1.1,
        )
        self.wait(0.5)

        steps = VGroup(
            MathTex(r"\lambda = \frac{L}{n_{\text{gel}}} = \frac{4}{2} = 2\,\text{m}", font_size=34, color=TEXT),
            MathTex(r"x_n = (2n - 1)\frac{\lambda}{4}", font_size=34, color=PRIMARY),
            MathTex(r"x_3 = (2 \cdot 3 - 1)\frac{2}{4}", font_size=34, color=TEXT),
            MathTex(r"x_3 = 2{,}5\,\text{m}", font_size=38, color=GOOD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        steps.to_edge(LEFT, buff=0.8).shift(DOWN * 0.3)

        for step in steps:
            self.play(Write(step), run_time=1.5)
            self.wait(SOAL2_FORMULA_PAUSE)

        answer = make_answer_box(Text("Jawaban: 2,5 m", font_size=30, color=GOOD, weight=BOLD))
        answer.next_to(legend, DOWN, buff=0.3)
        self.play(FadeIn(answer, scale=0.95), run_time=1.2)
        self.wait(SOAL2_ANSWER_PAUSE)

        end_scene(self, run_time=1.2)


class Soal3(MovingCameraScene):
    def construct(self):
        begin_scene(self)

        header = make_header("SOAL 3", "Percepatan Gerak Harmonik")
        self.play(FadeIn(header), run_time=1.0)
        self.wait(0.5)

        question = make_question_screenshot(
            "Soal 3: Percepatan Gerak Harmonik",
            rows=[
                q_text("Sebuah benda melakukan gerak harmonik arah vertikal dengan frekuensi 5 Hz."),
                q_text("Tepat saat menyimpang 2 cm di atas titik seimbang, benda tersebut mendapat percepatan yang nilai dan arahnya . . ."),
            ],
        )
        present_question(
            self,
            header,
            question,
            [0, 1],
            dock_width=5.25,
            highlight_pause=SOAL3_HIGHLIGHT_PAUSE,
            initial_pause=2.8,
            swipe_time=0.9,
            dock_pause=0.9,
        )

        knowns = show_knowns(
            self,
            [
                r"f = 5\,\text{Hz}",
                r"y = 0{,}02\,\text{m}",
                r"a = -\omega^2 y",
            ],
            side=RIGHT,
            y_shift=0.35,
        )
        legend = make_var_legend([
            (r"f",      "frekuensi"),
            (r"\omega", "kecepatan sudut"),
            (r"y",      "simpangan"),
            (r"a",      "percepatan"),
        ])
        legend.next_to(knowns, DOWN, buff=0.35)
        self.play(FadeIn(legend, shift=LEFT * 0.15), run_time=0.8)
        self.wait(1.0)
        self.play(FadeOut(question), run_time=0.85)
        self.wait(0.6)

        equilibrium_y = -0.6
        amp = 0.95
        t_tracker = ValueTracker(0)
        spring_anchor = [-2.3, 1.65, 0]

        def get_mass_y():
            return equilibrium_y + amp * np.cos(2 * PI * t_tracker.get_value() / 2)

        def get_spring():
            mass_y = get_mass_y()
            return make_spring(spring_anchor, [-2.3, mass_y + 0.34, 0])

        def get_mass():
            mass_y = get_mass_y()
            return Square(
                side_length=0.68,
                color=PRIMARY,
                fill_color=PRIMARY,
                fill_opacity=0.75,
            ).move_to([-2.3, mass_y, 0])

        equilibrium_line = DashedLine([-3.65, equilibrium_y, 0], [-0.95, equilibrium_y, 0], color=DIM, dash_length=0.12)
        eq_label = Text("titik seimbang", font_size=18, color=DIM).next_to(equilibrium_line, RIGHT, buff=0.12)
        ceiling = Line([-3.25, 1.65, 0], [-1.35, 1.65, 0], color=TEXT, stroke_width=4)
        hatches = VGroup(
            *[
                Line([-3.25 + i * 0.22, 1.65, 0], [-3.1 + i * 0.22, 1.9, 0], color=TEXT, stroke_width=2)
                for i in range(9)
            ]
        )
        spring = always_redraw(get_spring)
        mass = always_redraw(get_mass)

        self.play(Create(equilibrium_line), FadeIn(eq_label), Create(ceiling), Create(hatches), run_time=1.4)
        self.wait(1.0)
        # Draw static initial-state versions (t=0: mass at top of swing)
        init_mass_y = equilibrium_y + amp
        init_spring = make_spring(spring_anchor, [-2.3, init_mass_y + 0.34, 0])
        init_mass = Square(side_length=0.68, color=PRIMARY, fill_color=PRIMARY, fill_opacity=0.75).move_to([-2.3, init_mass_y, 0])
        self.play(Create(init_spring), GrowFromCenter(init_mass), run_time=1.0)
        self.wait(0.4)
        # Swap to always_redraw versions in one frame — positions are identical at t=0
        self.remove(init_spring, init_mass)
        self.add(spring, mass)
        # VO cue: narrate the observation while the object oscillates.
        self.play(t_tracker.animate.set_value(3.2), run_time=SOAL3_OSCILLATION_TIME, rate_func=linear)
        self.play(t_tracker.animate.set_value(3.5), run_time=1.4, rate_func=smooth)
        self.wait(1.0)

        position_arrow = Arrow([-1.55, equilibrium_y, 0], [-1.55, equilibrium_y + 0.85, 0], color=PRIMARY, buff=0, stroke_width=4)
        position_label = MathTex(r"y = +2\,\text{cm}", font_size=25, color=PRIMARY).next_to(position_arrow, RIGHT, buff=0.16)
        accel_arrow = Arrow([-2.95, equilibrium_y + 0.85, 0], [-2.95, equilibrium_y + 0.15, 0], color=SECONDARY, buff=0, stroke_width=5)
        accel_label = MathTex(r"\vec{a}", font_size=32, color=SECONDARY).next_to(accel_arrow, LEFT, buff=0.15)

        self.play(GrowArrow(position_arrow), Write(position_label), run_time=1.3)
        self.wait(SOAL3_STEP_PAUSE)
        self.play(GrowArrow(accel_arrow), Write(accel_label), run_time=1.3)
        self.wait(SOAL3_STEP_PAUSE)

        # Clear always_redraw updaters so the spring/mass can be faded out cleanly,
        # freeing the left side for the algebraic steps.
        spring.clear_updaters()
        mass.clear_updaters()
        self.play(
            FadeOut(spring), FadeOut(mass),
            FadeOut(ceiling), FadeOut(hatches),
            run_time=0.8,
        )

        steps = VGroup(
            MathTex(r"\omega = 2\pi f = 2\pi(5) = 10\pi\,\text{rad/s}", font_size=30, color=TEXT),
            MathTex(r"a = -\omega^2 y", font_size=36, color=PRIMARY),
            MathTex(r"a = -(10\pi)^2(0{,}02)", font_size=34, color=TEXT),
            MathTex(r"a = -2\pi^2\,\text{m/s}^2", font_size=36, color=ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        steps.to_edge(LEFT, buff=0.72).shift(DOWN * 2.3)

        for step in steps:
            self.play(Write(step), run_time=1.4)
            self.wait(SOAL3_FORMULA_PAUSE)

        answer = make_answer_box(
            MathTex(r"|a| = 2\pi^2 \approx 19{,}74\,\text{m/s}^2", font_size=26, color=GOOD),
            Text("Arah ke bawah, menuju titik seimbang", font_size=21, color=GOOD, weight=BOLD),
        )
        answer.next_to(legend, DOWN, buff=0.3)
        self.play(FadeIn(answer, scale=0.95), run_time=1.3)
        self.wait(SOAL3_ANSWER_PAUSE)

        end_scene(self, run_time=1.2)


class Soal4(MovingCameraScene):
    def construct(self):
        begin_scene(self)

        header = make_header("SOAL 4", "Energi Kinetik")
        self.play(FadeIn(header), run_time=1.0)
        self.wait(0.5)

        question = make_question_screenshot(
            "Soal 4: Energi Kinetik",
            rows=[
                q_text("Sebuah benda yang massanya 100 gram bergetar harmonik dengan periode 1/10 detik dan amplitudo 4 cm."),
                q_text("Besar energi kinetik pada saat simpangan 2 cm adalah . . . (satuan dalam Joule)"),
            ],
        )
        present_question(
            self,
            header,
            question,
            [0, 1],
            dock_width=5.25,
            highlight_pause=SOAL4_HIGHLIGHT_PAUSE,
            initial_pause=2.8,
            swipe_time=0.9,
            dock_pause=0.9,
        )

        knowns = show_knowns(
            self,
            [
                r"m = 0{,}1\,\text{kg}",
                r"T = 0{,}1\,\text{s}",
                r"A = 0{,}04\,\text{m}",
                r"y = 0{,}02\,\text{m}",
            ],
            side=RIGHT,
            y_shift=0.28,
        )
        legend = make_var_legend([
            (r"\omega", "kecepatan sudut"),
            (r"A",      "amplitudo"),
            (r"y",      "simpangan"),
            (r"E_k",    "energi kinetik"),
        ])
        legend.next_to(knowns, DOWN, buff=0.35)
        self.play(FadeIn(legend, shift=LEFT * 0.15), run_time=0.8)
        self.wait(1.0)
        self.play(FadeOut(question), run_time=0.85)
        self.wait(0.6)

        axes = Axes(
            x_range=[-0.05, 0.05, 0.02],
            y_range=[-0.055, 0.055, 0.02],
            x_length=6.0,
            y_length=2.1,
            axis_config={"color": DIM, "stroke_width": 1.4, "include_tip": False},
        ).move_to(LEFT * 1.8 + DOWN * 0.2)

        amp_val = 0.04
        target_y = 0.02
        amp_lines = VGroup(
            DashedLine(axes.c2p(-0.05, amp_val), axes.c2p(0.05, amp_val), color=DIM, dash_length=0.1),
            DashedLine(axes.c2p(-0.05, -amp_val), axes.c2p(0.05, -amp_val), color=DIM, dash_length=0.1),
        )
        target_line = DashedLine(
            axes.c2p(-0.05, target_y),
            axes.c2p(0.05, target_y),
            color=SECONDARY,
            dash_length=0.1,
            stroke_width=3,
        )
        amp_label = MathTex(r"A = 4\,\text{cm}", font_size=23, color=DIM).next_to(amp_lines[0], RIGHT, buff=0.1)
        y_label = MathTex(r"y = 2\,\text{cm}", font_size=23, color=SECONDARY).next_to(target_line, RIGHT, buff=0.1)
        dot = Dot(axes.c2p(0.01, target_y), color=PRIMARY, radius=0.1)

        self.play(Create(axes), run_time=1.1)
        self.wait(0.6)
        self.play(Create(amp_lines), Write(amp_label), run_time=1.2)
        self.wait(SOAL4_GRAPH_PAUSE - 1.0)
        self.play(Create(target_line), Write(y_label), FadeIn(dot, scale=1.5), run_time=1.3)
        self.wait(SOAL4_GRAPH_PAUSE)
        self.play(FadeOut(VGroup(axes, amp_lines, target_line, amp_label, y_label, dot)), run_time=1.0)
        # VO cue: explain why Ek depends on (A^2 - y^2) while the graph disappears.
        self.wait(3.5)

        steps = VGroup(
            MathTex(r"\omega = \frac{2\pi}{T} = \frac{2\pi}{0{,}1} = 20\pi\,\text{rad/s}", font_size=30, color=TEXT),
            MathTex(r"E_k = \frac{1}{2}m\omega^2(A^2 - y^2)", font_size=34, color=PRIMARY),
            MathTex(r"E_k = \frac{1}{2}(0{,}1)(20\pi)^2\bigl[(0{,}04)^2-(0{,}02)^2\bigr]", font_size=26, color=TEXT),
            MathTex(r"E_k = 0{,}024\pi^2\,\text{J}", font_size=36, color=ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        steps.to_edge(LEFT, buff=0.72).shift(DOWN * 0.3)

        for step in steps:
            self.play(Write(step), run_time=1.4)
            self.wait(SOAL4_FORMULA_PAUSE)

        answer = make_answer_box(
            MathTex(r"E_k = 0{,}024\pi^2\,\text{J}", font_size=28, color=GOOD),
            MathTex(r"\approx 0{,}237\,\text{J}", font_size=26, color=GOOD),
        )
        answer.next_to(legend, DOWN, buff=0.3)
        self.play(FadeIn(answer, scale=0.95), run_time=1.2)
        self.wait(SOAL4_ANSWER_PAUSE)

        end_scene(self, run_time=1.2)


class Soal5(MovingCameraScene):
    def construct(self):
        begin_scene(self)

        header = make_header("SOAL 5", "Energi Potensial")
        self.play(FadeIn(header), run_time=1.0)
        self.wait(0.5)

        question = make_question_screenshot(
            "Soal 5: Energi Potensial",
            rows=[
                q_text("Sebuah partikel bermassa 50 gram bergetar harmonis dengan frekuensi 100 Hz dan amplitudo 2 cm,"),
                q_text("maka besar energi potensial pada saat sudut fasenya 30° adalah . . . joule."),
            ],
        )
        present_question(
            self,
            header,
            question,
            [0, 1],
            dock_width=5.25,
            highlight_pause=SOAL5_HIGHLIGHT_PAUSE,
            initial_pause=2.8,
            swipe_time=0.9,
            dock_pause=0.9,
        )

        knowns = show_knowns(
            self,
            [
                r"m = 0{,}05\,\text{kg}",
                r"f = 100\,\text{Hz}",
                r"A = 0{,}02\,\text{m}",
                r"\theta = 30^\circ",
            ],
            side=RIGHT,
            y_shift=0.32,
        )
        self.wait(1.0)

        legend = make_var_legend([
            (r"\omega", "kecepatan sudut"),
            (r"\theta", "sudut fase"),
            (r"y",      "simpangan"),
            (r"E_p",    "energi potensial"),
        ])
        legend.next_to(knowns, DOWN, buff=0.35)
        self.play(FadeIn(legend, shift=LEFT * 0.15), run_time=0.8)

        self.play(FadeOut(question), run_time=0.85)
        self.wait(0.6)

        circle_radius = 1.15
        circle_center = LEFT * 2.75 + DOWN * 0.2
        ref_circle = Circle(radius=circle_radius, color=DIM, stroke_width=2).move_to(circle_center)
        x_axis = Line(circle_center + LEFT * 1.55, circle_center + RIGHT * 1.55, color=DIM, stroke_width=1)
        y_axis = Line(circle_center + DOWN * 1.55, circle_center + UP * 1.55, color=DIM, stroke_width=1)

        angle = 30 * DEGREES
        endpoint = circle_center + circle_radius * np.array([np.cos(angle), np.sin(angle), 0])
        radius_line = Line(circle_center, endpoint, color=ACCENT, stroke_width=3)
        angle_arc = Arc(radius=0.35, angle=angle, color=PRIMARY, stroke_width=3).shift(circle_center)
        angle_label = MathTex(r"30^\circ", font_size=22, color=PRIMARY).next_to(angle_arc, RIGHT, buff=0.05)
        proj_dot = Dot(endpoint, color=SECONDARY, radius=0.085)
        proj_line = DashedLine(endpoint, circle_center + RIGHT * circle_radius * np.cos(angle), color=SECONDARY, dash_length=0.08)
        y_proj = circle_radius * np.sin(angle)
        y_proj_line = Line(circle_center, circle_center + UP * y_proj, color=SECONDARY, stroke_width=4)
        y_proj_label = MathTex(r"y", font_size=24, color=SECONDARY).next_to(y_proj_line, LEFT, buff=0.1)
        caption = Text("simpangan dari fase", font_size=18, color=DIM).next_to(ref_circle, DOWN, buff=0.18)

        self.play(Create(ref_circle), Create(x_axis), Create(y_axis), FadeIn(caption), run_time=1.3)
        self.wait(0.8)
        self.play(Create(radius_line), Create(angle_arc), Write(angle_label), run_time=1.3)
        self.wait(1.0)
        self.play(FadeIn(proj_dot), Create(proj_line), Create(y_proj_line), Write(y_proj_label), run_time=1.4)
        # VO cue: explain that the vertical projection gives y = A sin(theta).
        self.wait(SOAL5_DIAGRAM_PAUSE)

        y_steps = VGroup(
            MathTex(r"y = A\sin\theta", font_size=31, color=PRIMARY),
            MathTex(r"y = 0{,}02\sin 30^\circ", font_size=31, color=TEXT),
            MathTex(r"y = 0{,}01\,\text{m}", font_size=34, color=ACCENT),
        ).arrange(DOWN, buff=0.22).move_to(RIGHT * 1.05 + DOWN * 1.25)
        for step in y_steps:
            self.play(FadeIn(step, shift=UP * 0.1), run_time=1.1)
            self.wait(SOAL5_DIAGRAM_PAUSE - 2.0)

        self.wait(0.5)
        self.play(
            FadeOut(VGroup(ref_circle, x_axis, y_axis, radius_line, angle_arc, angle_label, proj_dot, proj_line, y_proj_line, y_proj_label, caption, y_steps)),
            run_time=1.1,
        )
        self.wait(0.5)

        steps = VGroup(
            MathTex(r"\omega = 2\pi f = 2\pi(100) = 200\pi\,\text{rad/s}", font_size=30, color=TEXT),
            MathTex(r"y = A\sin\theta = 0{,}02\sin 30^\circ = 0{,}01\,\text{m}", font_size=30, color=TEXT),
            MathTex(r"E_p = \frac{1}{2}m\omega^2 y^2", font_size=34, color=PRIMARY),
            MathTex(r"E_p = \frac{1}{2}(0{,}05)(200\pi)^2(0{,}01)^2", font_size=28, color=TEXT),
            MathTex(r"E_p = 0{,}1\pi^2\,\text{J}", font_size=36, color=ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        steps.to_edge(LEFT, buff=0.72).shift(DOWN * 0.2)

        for step in steps:
            self.play(Write(step), run_time=1.4)
            self.wait(SOAL5_FORMULA_PAUSE)

        answer = make_answer_box(
            MathTex(r"E_p = 0{,}1\pi^2\,\text{J}", font_size=28, color=GOOD),
            MathTex(r"\approx 0{,}987\,\text{J}", font_size=26, color=GOOD),
        )
        answer.next_to(legend, DOWN, buff=0.3)
        self.play(FadeIn(answer, scale=0.95), run_time=1.2)
        self.wait(SOAL5_ANSWER_PAUSE)

        end_scene(self, run_time=1.2)


class FullVideo(MovingCameraScene):
    def construct(self):
        for scene_class in [Intro, Soal1, Soal2, Soal3, Soal4, Soal5]:
            scene_class.construct(self)
            self.clear()
            reset_camera_frame(self)
