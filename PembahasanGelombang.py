from manim import *
from manim_physics import StandingWave, Pendulum, SpaceScene
import numpy as np
 
BG_COLOR = "#0f1729"
PRIMARY = "#4dabf7"
SECONDARY = "#ff6b6b"
ACCENT = "#ffd43b"
CORRECT = "#51cf66"
INCORRECT = "#ff8787"
TEXT = "#f8f9fa"
DIM = "#adb5bd"
 
config.background_color = BG_COLOR
 
 
def make_header(num, title):
    num_text = Text(num, font_size=24, color=PRIMARY, weight=BOLD)
    title_text = Text(title, font_size=32, color=TEXT, weight=BOLD)
    line = Line(LEFT * 3, RIGHT * 3, color=PRIMARY, stroke_width=2)
    group = VGroup(num_text, title_text, line).arrange(DOWN, buff=0.15)
    return group.to_edge(UP, buff=0.4)
 
 
def make_spring(start, end, num_coils=8, width=0.3):
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
        point = start + direction * length * t + perp * width * sign
        points.append(point)
    points.append(end)
    return VMobject(color=DIM, stroke_width=3).set_points_as_corners(points)
 
 
class Intro(Scene):
    def construct(self):
        title = Text("Pembahasan Soal Fisika", font_size=56, color=TEXT, weight=BOLD)
        subtitle = Text("Gelombang & Gerak Harmonik", font_size=42, color=PRIMARY)
        subtitle.next_to(title, DOWN, buff=0.4)
        level = Text("Tingkat SMA Kelas 11", font_size=28, color=DIM)
        level.next_to(subtitle, DOWN, buff=0.4)
 
        wave = always_redraw(lambda: FunctionGraph(
            lambda x: 0.4 * np.sin(2 * x),
            x_range=[-6, 6],
            color=ACCENT,
            stroke_width=3
        ).shift(DOWN * 2.5))
 
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle, shift=UP * 0.3))
        self.play(FadeIn(level))
        self.add(wave)
        self.wait(2)
        self.play(FadeOut(VGroup(title, subtitle, level, wave)))
 
 
class Soal1(Scene):
    def construct(self):
        header = make_header("SOAL 1", "Gelombang Berjalan")
        self.play(FadeIn(header))
 
        equation = MathTex(
            r"y_B = 0{,}04 \sin 8\pi \left(t_A + \frac{x}{2}\right)",
            font_size=48,
            color=TEXT
        ).move_to(UP * 1.5)
 
        unit_note = Text("Semua besaran dalam SI", font_size=22, color=DIM)
        unit_note.next_to(equation, DOWN, buff=0.3)
 
        self.play(Write(equation))
        self.play(FadeIn(unit_note))
        self.wait(1)
 
        wave_axes = Axes(
            x_range=[0, 10, 1],
            y_range=[-0.08, 0.08, 0.04],
            x_length=10,
            y_length=2,
            axis_config={"color": DIM, "stroke_width": 2}
        ).shift(DOWN * 1.5)
 
        t_tracker = ValueTracker(0)
        wave_curve = always_redraw(lambda: wave_axes.plot(
            lambda x: 0.04 * np.sin(8 * PI * (t_tracker.get_value() + x / 2)),
            color=ACCENT,
            stroke_width=4
        ))
 
        label_A = Text("A", font_size=28, color=CORRECT, weight=BOLD).next_to(wave_axes, LEFT, buff=0.3)
        label_B = Text("B", font_size=28, color=SECONDARY, weight=BOLD).next_to(wave_axes, RIGHT, buff=0.3)
 
        self.play(Create(wave_axes), Write(label_A), Write(label_B))
        self.add(wave_curve)
        self.play(t_tracker.animate.set_value(2), run_time=4, rate_func=linear)
 
        self.play(FadeOut(VGroup(equation, unit_note, wave_axes, wave_curve, label_A, label_B)))
 
        general_form = MathTex(
            r"y = A \sin \omega \left(t \pm \frac{x}{v}\right)",
            font_size=44,
            color=PRIMARY
        ).move_to(UP * 2.5)
        general_label = Text("Bentuk umum:", font_size=24, color=DIM).next_to(general_form, UP, buff=0.2)
 
        eq2 = MathTex(
            r"y_B = 0{,}04 \sin 8\pi \left(t_A + \frac{x}{2}\right)",
            font_size=40,
            color=TEXT
        ).move_to(UP * 1.0)
 
        self.play(FadeIn(general_label), Write(general_form))
        self.play(Write(eq2))
        self.wait(1)
 
        analyses = VGroup(
            self._make_check(r"A = 0{,}04 \text{ m} = 4 \text{ cm}", "Pernyataan A: Benar", CORRECT),
            self._make_check(r"f = \frac{\omega}{2\pi} = \frac{8\pi}{2\pi} = 4 \text{ Hz}", "Pernyataan B: Benar", CORRECT),
            self._make_check(r"T = \frac{1}{f} = 0{,}25 \text{ s}", "Pernyataan C: Salah (bukan 0,5 s)", INCORRECT),
            self._make_check(r"v = 2 \text{ m/s}", "Pernyataan D: Benar", CORRECT),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).scale(0.75).move_to(DOWN * 0.5)
 
        for item in analyses:
            self.play(FadeIn(item, shift=RIGHT * 0.3), run_time=0.8)
            self.wait(0.5)
 
        self.wait(1)
        answer_text = Text("Jawaban: A, B, dan D", font_size=40, color=BG_COLOR, weight=BOLD)
        answer_box = SurroundingRectangle(answer_text, color=CORRECT, fill_color=CORRECT, fill_opacity=1, buff=0.4, corner_radius=0.2)
        answer_group = VGroup(answer_box, answer_text)
 
        self.play(FadeOut(VGroup(general_label, general_form, eq2, analyses)))
        self.play(FadeIn(answer_group, scale=0.8))
        self.wait(2)
        self.play(FadeOut(VGroup(header, answer_group)))
 
    def _make_check(self, formula, status, color):
        f = MathTex(formula, font_size=32, color=TEXT)
        s = Text(status, font_size=22, color=color, weight=BOLD)
        return VGroup(f, s).arrange(RIGHT, buff=0.5)
 
 
class Soal2(Scene):
    """Menggunakan StandingWave dari manim-physics untuk gelombang stasioner."""
    def construct(self):
        header = make_header("SOAL 2", "Gelombang Stasioner")
        self.play(FadeIn(header))
 
        problem = VGroup(
            Text("Tali panjang 4 m, satu ujung diikat", font_size=26, color=TEXT),
            Text("Terbentuk 2 gelombang penuh", font_size=26, color=TEXT),
            Text("Cari letak perut ke-3 dari ujung terikat", font_size=26, color=ACCENT),
        ).arrange(DOWN, buff=0.2).move_to(UP * 2)
 
        for line in problem:
            self.play(FadeIn(line, shift=UP * 0.2), run_time=0.6)
        self.wait(1)
 
        L_screen = 8
        n_harmonic = 4
        x_start = -L_screen / 2
        wave_y_offset = -0.5
        scale_factor = 2
 
        wave = StandingWave(
            n=n_harmonic,
            length=L_screen,
            period=2.5,
            amplitude=0.7,
            color=ACCENT,
            stroke_width=4
        ).shift(UP * wave_y_offset)
 
        eq_line = DashedLine(
            [x_start, wave_y_offset, 0],
            [x_start + L_screen, wave_y_offset, 0],
            color=DIM,
            dash_length=0.1
        )
 
        fixed_end = VGroup(
            Line([x_start, wave_y_offset - 0.6, 0], [x_start, wave_y_offset + 0.6, 0],
                 color=SECONDARY, stroke_width=4),
            *[Line(
                [x_start - 0.25, wave_y_offset - 0.6 + i * 0.24, 0],
                [x_start, wave_y_offset - 0.4 + i * 0.24, 0],
                color=SECONDARY, stroke_width=2
            ) for i in range(6)]
        )
        fixed_label = Text("ujung terikat", font_size=18, color=SECONDARY).next_to(fixed_end, DOWN, buff=0.3)
        free_end_label = Text("digetarkan", font_size=18, color=PRIMARY).next_to(
            [x_start + L_screen, wave_y_offset, 0], DOWN, buff=0.5)
 
        self.play(FadeOut(problem))
        self.play(Create(eq_line), FadeIn(fixed_end), Write(fixed_label), Write(free_end_label))
 
        self.add(wave)
        wave.start_wave()
        self.wait(4)
 
        antinode_offsets_m = [0.5, 1.5, 2.5, 3.5]
        antinode_dots = VGroup()
        antinode_labels = VGroup()
        for i, offset_m in enumerate(antinode_offsets_m):
            x_pos = x_start + offset_m * scale_factor
            dot = Dot([x_pos, wave_y_offset, 0], color=CORRECT, radius=0.1)
            label = Text(f"P{i+1}", font_size=22, color=CORRECT, weight=BOLD).next_to(dot, UP, buff=0.4)
            antinode_dots.add(dot)
            antinode_labels.add(label)
 
        self.play(FadeIn(antinode_dots), FadeIn(antinode_labels))
        self.wait(1)
 
        third_x = x_start + 2.5 * scale_factor
        highlight = Circle(radius=0.4, color=INCORRECT, stroke_width=4).move_to([third_x, wave_y_offset, 0])
        self.play(Create(highlight))
        self.wait(0.5)
 
        measure_line = DoubleArrow(
            [x_start, wave_y_offset - 1.5, 0],
            [third_x, wave_y_offset - 1.5, 0],
            color=ACCENT, stroke_width=3, buff=0
        )
        measure_label = MathTex(r"x_3 = 2{,}5 \text{ m}", font_size=32, color=ACCENT).next_to(
            measure_line, DOWN, buff=0.2)
 
        self.play(GrowArrow(measure_line))
        self.play(Write(measure_label))
        self.wait(2)
 
        wave.stop_wave()
        self.play(FadeOut(VGroup(
            eq_line, fixed_end, fixed_label, free_end_label, wave,
            antinode_dots, antinode_labels, highlight, measure_line, measure_label
        )))
 
        solution_steps = VGroup(
            MathTex(r"\lambda = \frac{L}{n} = \frac{4}{2} = 2 \text{ m}", font_size=40, color=TEXT),
            MathTex(r"x_n = (2n-1) \cdot \frac{\lambda}{4}", font_size=40, color=TEXT),
            MathTex(r"x_3 = (2 \cdot 3 - 1) \cdot \frac{2}{4} = \frac{5 \cdot 2}{4}", font_size=40, color=TEXT),
            MathTex(r"x_3 = 2{,}5 \text{ m}", font_size=44, color=ACCENT),
        ).arrange(DOWN, buff=0.4).move_to(ORIGIN)
 
        for step in solution_steps:
            self.play(Write(step), run_time=1)
            self.wait(0.3)
 
        self.wait(2)
        self.play(FadeOut(VGroup(header, solution_steps)))
 
 
class Soal3(Scene):
    def construct(self):
        header = make_header("SOAL 3", "Percepatan Gerak Harmonik")
        self.play(FadeIn(header))
 
        given = VGroup(
            Text("Gerak harmonik vertikal", font_size=26, color=TEXT),
            MathTex(r"f = 5 \text{ Hz}", font_size=32, color=TEXT),
            MathTex(r"y = 2 \text{ cm di atas titik seimbang}", font_size=32, color=TEXT),
            Text("Cari: nilai dan arah percepatan", font_size=26, color=ACCENT),
        ).arrange(DOWN, buff=0.25).move_to(UP * 1.5)
 
        for item in given:
            self.play(FadeIn(item, shift=UP * 0.2), run_time=0.6)
        self.wait(1)
        self.play(FadeOut(given))
 
        equilibrium_y = -0.5
        amp = 1.5
 
        equilibrium_line = DashedLine(
            [-2, equilibrium_y, 0],
            [2, equilibrium_y, 0],
            color=DIM, dash_length=0.15
        )
        eq_label = Text("titik seimbang", font_size=20, color=DIM).next_to(equilibrium_line, RIGHT, buff=0.2)
 
        self.play(Create(equilibrium_line), FadeIn(eq_label))
 
        t_tracker = ValueTracker(0)
        spring_anchor = [0, 3, 0]
 
        def get_mass_pos():
            return equilibrium_y + amp * np.cos(2 * PI * t_tracker.get_value() / 2)
 
        def get_spring():
            mass_y = get_mass_pos()
            return make_spring(spring_anchor, [0, mass_y + 0.4, 0])
 
        def get_mass():
            mass_y = get_mass_pos()
            return Square(side_length=0.8, color=PRIMARY,
                          fill_color=PRIMARY, fill_opacity=0.7).move_to([0, mass_y, 0])
 
        spring = always_redraw(get_spring)
        mass = always_redraw(get_mass)
 
        ceiling = Line([-1.5, 3, 0], [1.5, 3, 0], color=TEXT, stroke_width=4)
        hatches = VGroup(*[
            Line([-1.5 + i * 0.3, 3, 0], [-1.5 + i * 0.3 + 0.2, 3.3, 0],
                 color=TEXT, stroke_width=2)
            for i in range(11)
        ])
 
        self.play(Create(ceiling), Create(hatches))
        self.add(spring, mass)
        self.play(t_tracker.animate.set_value(1.5), run_time=3, rate_func=linear)
        self.play(t_tracker.animate.set_value(2.0), run_time=1, rate_func=smooth)
 
        position_arrow = Arrow(
            [0.7, equilibrium_y, 0],
            [0.7, equilibrium_y + 1.0, 0],
            color=PRIMARY, buff=0, stroke_width=4
        )
        position_label = MathTex(r"y = +2 \text{ cm}", font_size=28, color=PRIMARY).next_to(
            position_arrow, RIGHT, buff=0.2)
 
        self.play(GrowArrow(position_arrow), Write(position_label))
        self.wait(1)
 
        accel_arrow = Arrow(
            [-0.7, equilibrium_y + 1.0, 0],
            [-0.7, equilibrium_y + 0.2, 0],
            color=SECONDARY, buff=0, stroke_width=6
        )
        accel_label = MathTex(r"\vec{a}", font_size=36, color=SECONDARY).next_to(
            accel_arrow, LEFT, buff=0.2)
 
        self.play(GrowArrow(accel_arrow), Write(accel_label))
        self.wait(1)
 
        self.remove(spring, mass)
        static_spring = make_spring(spring_anchor, [0, equilibrium_y + 1.0 + 0.4, 0])
        static_mass = Square(side_length=0.8, color=PRIMARY,
                             fill_color=PRIMARY, fill_opacity=0.7).move_to([0, equilibrium_y + 1.0, 0])
        self.add(static_spring, static_mass)
 
        self.play(FadeOut(VGroup(
            equilibrium_line, eq_label, ceiling, hatches,
            static_spring, static_mass, position_arrow, position_label,
            accel_arrow, accel_label
        )))
 
        solution = VGroup(
            MathTex(r"a = -\omega^2 \cdot y", font_size=44, color=PRIMARY),
            MathTex(r"\omega = 2\pi f = 2\pi \cdot 5 = 10\pi \text{ rad/s}", font_size=36, color=TEXT),
            MathTex(r"a = -(10\pi)^2 \cdot 0{,}02", font_size=36, color=TEXT),
            MathTex(r"a = -100\pi^2 \cdot 0{,}02 = -2\pi^2 \text{ m/s}^2", font_size=40, color=ACCENT),
        ).arrange(DOWN, buff=0.4).move_to(ORIGIN)
 
        for step in solution:
            self.play(Write(step), run_time=1)
            self.wait(0.3)
 
        self.wait(1)
 
        conclusion = VGroup(
            MathTex(r"|a| = 2\pi^2 \text{ m/s}^2 \approx 19{,}74 \text{ m/s}^2", font_size=36, color=CORRECT),
            Text("Arah ke bawah (menuju titik seimbang)", font_size=28, color=CORRECT),
        ).arrange(DOWN, buff=0.3).move_to(DOWN * 2.8)
 
        self.play(FadeOut(solution))
        self.play(FadeIn(conclusion))
        self.wait(3)
        self.play(FadeOut(VGroup(header, conclusion)))
 
 
class Soal4(Scene):
    def construct(self):
        header = make_header("SOAL 4", "Energi Kinetik Gerak Harmonik")
        self.play(FadeIn(header))
 
        given = VGroup(
            MathTex(r"m = 100 \text{ g} = 0{,}1 \text{ kg}", font_size=32, color=TEXT),
            MathTex(r"T = \frac{1}{10} \text{ s} = 0{,}1 \text{ s}", font_size=32, color=TEXT),
            MathTex(r"A = 4 \text{ cm} = 0{,}04 \text{ m}", font_size=32, color=TEXT),
            MathTex(r"y = 2 \text{ cm} = 0{,}02 \text{ m}", font_size=32, color=TEXT),
            Text("Cari: Energi Kinetik (E_k)", font_size=26, color=ACCENT),
        ).arrange(DOWN, buff=0.25).move_to(UP * 0.5)
 
        for item in given:
            self.play(FadeIn(item, shift=RIGHT * 0.2), run_time=0.5)
        self.wait(1.5)
        self.play(FadeOut(given))
 
        axes = Axes(
            x_range=[-0.05, 0.05, 0.02],
            y_range=[-0.06, 0.06, 0.02],
            x_length=8,
            y_length=2.5,
            axis_config={"color": DIM, "stroke_width": 1.5, "include_tip": False}
        ).shift(UP * 0.5)
 
        amp_val = 0.04
        target_y = 0.02
 
        amp_lines = VGroup(
            DashedLine(axes.c2p(-0.05, amp_val), axes.c2p(0.05, amp_val),
                       color=DIM, dash_length=0.1),
            DashedLine(axes.c2p(-0.05, -amp_val), axes.c2p(0.05, -amp_val),
                       color=DIM, dash_length=0.1),
        )
        target_line = DashedLine(
            axes.c2p(-0.05, target_y), axes.c2p(0.05, target_y),
            color=SECONDARY, dash_length=0.1, stroke_width=3
        )
 
        amp_label = MathTex(r"A = 4\text{ cm}", font_size=24, color=DIM).next_to(
            amp_lines[0], RIGHT, buff=0.1)
        y_label = MathTex(r"y = 2\text{ cm}", font_size=24, color=SECONDARY).next_to(
            target_line, RIGHT, buff=0.1)
 
        self.play(Create(axes))
        self.play(Create(amp_lines), Write(amp_label))
        self.play(Create(target_line), Write(y_label))
 
        dot = Dot(axes.c2p(0.01, target_y), color=PRIMARY, radius=0.12)
        self.play(FadeIn(dot, scale=2))
        self.wait(1)
 
        self.play(FadeOut(VGroup(axes, amp_lines, target_line, amp_label, y_label, dot)))
 
        formula = MathTex(
            r"E_k = \frac{1}{2} m \omega^2 (A^2 - y^2)",
            font_size=44, color=PRIMARY
        ).move_to(UP * 1.8)
        self.play(Write(formula))
        self.wait(1)
 
        omega_calc = MathTex(
            r"\omega = \frac{2\pi}{T} = \frac{2\pi}{0{,}1} = 20\pi \text{ rad/s}",
            font_size=36, color=TEXT
        ).move_to(UP * 0.5)
        self.play(Write(omega_calc))
        self.wait(1)
 
        substitution = MathTex(
            r"E_k = \frac{1}{2}(0{,}1)(20\pi)^2 \left[(0{,}04)^2 - (0{,}02)^2\right]",
            font_size=32, color=TEXT
        ).move_to(DOWN * 0.6)
        self.play(Write(substitution))
        self.wait(1)
 
        calc1 = MathTex(
            r"= \frac{1}{2}(0{,}1)(400\pi^2)(0{,}0012)",
            font_size=32, color=TEXT
        ).move_to(DOWN * 1.6)
        self.play(Write(calc1))
        self.wait(1)
 
        result = MathTex(
            r"E_k = 0{,}024\pi^2 \text{ J} \approx 0{,}237 \text{ J}",
            font_size=40, color=ACCENT
        ).move_to(DOWN * 2.7)
        result_box = SurroundingRectangle(result, color=CORRECT, buff=0.2,
                                          corner_radius=0.15, stroke_width=3)
 
        self.play(Write(result), Create(result_box))
        self.wait(3)
        self.play(FadeOut(VGroup(header, formula, omega_calc, substitution,
                                 calc1, result, result_box)))
 
 
class Soal5(SpaceScene):
    """Menggunakan Pendulum dari manim-physics untuk visualisasi GHS."""
    def construct(self):
        header = make_header("SOAL 5", "Energi Potensial Gerak Harmonik")
        self.play(FadeIn(header))
 
        given = VGroup(
            MathTex(r"m = 50 \text{ g} = 0{,}05 \text{ kg}", font_size=32, color=TEXT),
            MathTex(r"f = 100 \text{ Hz}", font_size=32, color=TEXT),
            MathTex(r"A = 2 \text{ cm} = 0{,}02 \text{ m}", font_size=32, color=TEXT),
            MathTex(r"\theta = 30^\circ", font_size=32, color=TEXT),
            Text("Cari: Energi Potensial (E_p)", font_size=26, color=ACCENT),
        ).arrange(DOWN, buff=0.25).move_to(UP * 0.5)
 
        for item in given:
            self.play(FadeIn(item, shift=RIGHT * 0.2), run_time=0.5)
        self.wait(1.5)
        self.play(FadeOut(given))
 
        circle_radius = 1.3
        circle_center = LEFT * 3.5 + UP * 0.5
        ref_circle = Circle(radius=circle_radius, color=DIM, stroke_width=2).move_to(circle_center)
 
        x_axis = Line(circle_center + LEFT * 1.8, circle_center + RIGHT * 1.8,
                      color=DIM, stroke_width=1)
        y_axis = Line(circle_center + DOWN * 1.8, circle_center + UP * 1.8,
                      color=DIM, stroke_width=1)
 
        angle = 30 * DEGREES
        radius_line = Line(
            circle_center,
            circle_center + circle_radius * np.array([np.cos(angle), np.sin(angle), 0]),
            color=ACCENT, stroke_width=3
        )
        angle_arc = Arc(radius=0.35, angle=angle, color=PRIMARY,
                        stroke_width=3).shift(circle_center)
        angle_label = MathTex(r"30^\circ", font_size=22, color=PRIMARY).next_to(
            angle_arc, RIGHT, buff=0.05).shift(UP * 0.05)
 
        proj_dot = Dot(
            circle_center + circle_radius * np.array([np.cos(angle), np.sin(angle), 0]),
            color=SECONDARY, radius=0.09
        )
        proj_line = DashedLine(
            proj_dot.get_center(),
            circle_center + RIGHT * circle_radius * np.cos(angle),
            color=SECONDARY, dash_length=0.08
        )
        y_proj = circle_radius * np.sin(angle)
        y_proj_line = Line(
            circle_center,
            circle_center + UP * y_proj,
            color=SECONDARY, stroke_width=4
        )
        y_proj_label = MathTex(r"y", font_size=24, color=SECONDARY).next_to(
            y_proj_line, LEFT, buff=0.1)
 
        circle_label = Text("Lingkaran acuan", font_size=20, color=DIM).move_to(
            circle_center + DOWN * 2.0)
 
        self.play(Create(ref_circle), Create(x_axis), Create(y_axis), FadeIn(circle_label))
        self.play(Create(radius_line), Create(angle_arc), Write(angle_label))
        self.play(FadeIn(proj_dot), Create(proj_line))
        self.play(Create(y_proj_line), Write(y_proj_label))
        self.wait(0.5)
 
        pendulum_pivot = RIGHT * 3.5 + UP * 2.0
        pivot_line = Line(
            pendulum_pivot + LEFT * 0.6,
            pendulum_pivot + RIGHT * 0.6,
            color=TEXT, stroke_width=4
        )
        pivot_dot = Dot(pendulum_pivot, color=TEXT, radius=0.07)
 
        pendulum = Pendulum(
            initial_theta=PI / 6,
            length=2.2,
            weight_diameter=0.35,
            rod_style={"color": DIM, "stroke_width": 3},
            bob_style={"color": ACCENT, "fill_opacity": 0.9},
        )
        pendulum.move_to(pendulum_pivot + DOWN * 1.1)
 
        pendulum_caption = Text("contoh osilasi GHS", font_size=18, color=DIM).move_to(
            pendulum_pivot + DOWN * 3.2
        )
 
        self.add(pivot_line, pivot_dot, pendulum_caption)
        self.add(pendulum)
        try:
            self.make_rigid_body(pendulum.bobs)
        except Exception:
            pass
 
        self.wait(2)
 
        y_calc = VGroup(
            MathTex(r"y = A \sin \theta", font_size=28, color=TEXT),
            MathTex(r"y = 0{,}02 \cdot \sin 30^\circ", font_size=28, color=TEXT),
            MathTex(r"y = 0{,}01 \text{ m}", font_size=32, color=ACCENT),
        ).arrange(DOWN, buff=0.25).move_to(LEFT * 3.5 + DOWN * 2.8)
 
        for step in y_calc:
            self.play(Write(step), run_time=0.7)
            self.wait(0.2)
 
        self.wait(2)
        self.play(FadeOut(VGroup(
            ref_circle, x_axis, y_axis, radius_line, angle_arc, angle_label,
            proj_dot, proj_line, y_proj_line, y_proj_label, circle_label,
            y_calc, pendulum, pivot_dot, pivot_line, pendulum_caption
        )))
 
        formula = MathTex(r"E_p = \frac{1}{2} m \omega^2 y^2",
                          font_size=44, color=PRIMARY).move_to(UP * 2)
        self.play(Write(formula))
 
        omega_calc = MathTex(r"\omega = 2\pi f = 200\pi \text{ rad/s}",
                             font_size=36, color=TEXT).move_to(UP * 0.7)
        self.play(Write(omega_calc))
 
        substitution = MathTex(
            r"E_p = \frac{1}{2}(0{,}05)(200\pi)^2(0{,}01)^2",
            font_size=32, color=TEXT
        ).move_to(DOWN * 0.5)
        self.play(Write(substitution))
 
        calc = MathTex(
            r"= \frac{1}{2}(0{,}05)(40000\pi^2)(0{,}0001)",
            font_size=32, color=TEXT
        ).move_to(DOWN * 1.5)
        self.play(Write(calc))
 
        result = MathTex(r"E_p = 0{,}1\pi^2 \text{ J} \approx 0{,}987 \text{ J}",
                         font_size=40, color=ACCENT).move_to(DOWN * 2.7)
        result_box = SurroundingRectangle(result, color=CORRECT, buff=0.2,
                                          corner_radius=0.15, stroke_width=3)
        self.play(Write(result), Create(result_box))
        self.wait(3)
        self.play(FadeOut(VGroup(header, formula, omega_calc, substitution,
                                 calc, result, result_box)))
 

class FullVideo(Scene):
    def construct(self):
        Intro.construct(self)
        Soal1.construct(self)
        Soal2.construct(self)
        Soal3.construct(self)
        Soal4.construct(self)
        Soal5.construct(self)