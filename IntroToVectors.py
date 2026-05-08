from manim import *

from VectorProducts import DotProductScene


class IntroScene(Scene):
    def construct(self):
        title = Text("Vectors", font_size=48)
        subtitle = Text("Geometry to Abstraction", font_size=32, color=GRAY)
        subtitle.next_to(title, DOWN, buff=0.4)

        self.play(Write(title), run_time=2)
        self.play(FadeIn(subtitle, shift=UP*0.3))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle))


class EuclideanVectorScene(Scene):
    def construct(self):
        title = Text("Euclidean Vectors", font_size=40).to_edge(UP)
        self.play(Write(title))

        plane = NumberPlane(
            x_range=[-6, 6, 1],
            y_range=[-4, 4, 1],
            background_line_style={"stroke_opacity": 0.4},
        )
        self.play(Create(plane), run_time=2)

        vector = Arrow(start=plane.c2p(0, 0), end=plane.c2p(3, 2), buff=0, color=YELLOW)
        vector_label = MathTex(r"\vec{v}", color=YELLOW).next_to(
            vector.get_center(), UP + LEFT, buff=0.1
        )

        self.play(GrowArrow(vector), Write(vector_label))
        self.wait(1)

        components = MathTex(
            r"\vec{v} = \begin{pmatrix} 3 \\ 2 \end{pmatrix}", font_size=36
        ).to_corner(UR).shift(DOWN*0.5)
        self.play(Write(components))
        self.wait(1)

        magnitude = MathTex(
            r"\|\vec{v}\| = \sqrt{3^2 + 2^2} = \sqrt{13}", font_size=32
        ).to_corner(DR)
        self.play(Write(magnitude))
        self.wait(2)

        self.play(FadeOut(magnitude), FadeOut(components))

        free_text = Text("'Free' Vector: position is not important", font_size=28).to_edge(DOWN)
        self.play(Write(free_text))

        copy1 = Arrow(start=plane.c2p(-4, -2), end=plane.c2p(-1, 0), buff=0, color=YELLOW)
        copy2 = Arrow(start=plane.c2p(1, -3), end=plane.c2p(4, -1), buff=0, color=YELLOW)

        self.play(TransformFromCopy(vector, copy1), TransformFromCopy(vector, copy2))
        self.wait(2)

        self.play(*[FadeOut(m) for m in self.mobjects])


class VectorOperationsScene(Scene):
    def construct(self):
        title = Text("Vector Operations", font_size=40).to_edge(UP)
        self.play(Write(title))

        plane = NumberPlane(
            x_range=[-6, 6, 1],
            y_range=[-4, 4, 1],
            background_line_style={"stroke_opacity": 0.3},
        )
        self.play(Create(plane), run_time=1.5)

        u = Arrow(start=plane.c2p(0, 0), end=plane.c2p(2, 1), buff=0, color=BLUE)
        v = Arrow(start=plane.c2p(0, 0), end=plane.c2p(1, 2), buff=0, color=GREEN)
        u_label = MathTex(r"\vec{u}", color=BLUE).next_to(u.get_end(), DOWN + RIGHT, buff=0.1)
        v_label = MathTex(r"\vec{v}", color=GREEN).next_to(v.get_end(), UP + LEFT, buff=0.1)

        self.play(GrowArrow(u), Write(u_label))
        self.play(GrowArrow(v), Write(v_label))
        self.wait(1)

        addition_text = Text("Parallelogram Law of Vector Addition", font_size=28).to_edge(DOWN)
        self.play(Write(addition_text))

        v_shifted = Arrow(
            start=u.get_end(),
            end=u.get_end() + (v.get_end() - v.get_start()),
            buff=0,
            color=GREEN,
        )
        u_shifted = Arrow(
            start=v.get_end(),
            end=v.get_end() + (u.get_end() - u.get_start()),
            buff=0,
            color=BLUE,
        )
        self.play(TransformFromCopy(v, v_shifted))
        self.play(TransformFromCopy(u, u_shifted))

        sum_vector = Arrow(start=plane.c2p(0, 0), end=plane.c2p(3, 3), buff=0, color=RED)
        sum_label = MathTex(r"\vec{u} + \vec{v}", color=RED).next_to(
            sum_vector.get_end(), UP + RIGHT, buff=0.1
        )

        self.play(GrowArrow(sum_vector), Write(sum_label))
        self.wait(2)

        self.play(
            FadeOut(v_shifted),
            FadeOut(u_shifted),
            FadeOut(sum_vector),
            FadeOut(sum_label),
            FadeOut(addition_text),
            FadeOut(v),
            FadeOut(v_label),
        )

        scalar_text = Text("Scalar Multiplication", font_size=28).to_edge(DOWN)
        self.play(Write(scalar_text))

        u_doubled = Arrow(start=plane.c2p(0, 0), end=plane.c2p(4, 2), buff=0, color=BLUE)
        u_double_label = MathTex(r"2\vec{u}", color=BLUE).next_to(u_doubled.get_end(), RIGHT)

        self.play(Transform(u, u_doubled), Transform(u_label, u_double_label))
        self.wait(1.5)

        u_negative = Arrow(start=plane.c2p(0, 0), end=plane.c2p(-2, -1), buff=0, color=BLUE)
        u_neg_label = MathTex(r"-\vec{u}", color=BLUE).next_to(u_negative.get_end(), DOWN + LEFT)

        self.play(Transform(u, u_negative), Transform(u_label, u_neg_label))
        self.wait(2)

        self.play(*[FadeOut(m) for m in self.mobjects])


class AlgebraicVectorScene(Scene):
    def construct(self):
        title = Text("Algebraic Representation", font_size=40).to_edge(UP)
        self.play(Write(title))

        column_vec = MathTex(
            r"\vec{v} = \begin{pmatrix} v_1 \\ v_2 \\ \vdots \\ v_n \end{pmatrix}",
            font_size=56,
        ).shift(LEFT * 3.5)

        self.play(Write(column_vec))
        self.wait(1)

        rn_def = MathTex(
            r"\mathbb{R}^n = \{(x_1, x_2, \dots, x_n) \mid x_i \in \mathbb{R}\}",
            font_size=34,
        ).shift(RIGHT * 1.5 + UP * 0.5)

        rn_explain = VGroup(
            Tex(r"$\mathbb{R}$: Real Numbers", font_size=30),
            Tex(r"$n$: Dimension (Number of Components)", font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(rn_def, DOWN, buff=0.6)

        self.play(Write(rn_def))
        self.wait(1)
        self.play(Write(rn_explain))
        self.wait(2)

        self.play(FadeOut(column_vec), FadeOut(rn_def), FadeOut(rn_explain))

        examples_title = Text("Examples:", font_size=32).shift(UP * 2.5)
        r2_example = MathTex(
            r"\mathbb{R}^2: \quad \vec{v} = \begin{pmatrix} 3 \\ 2 \end{pmatrix}",
            font_size=40,
        ).shift(UP * 0.7)
        r3_example = MathTex(
            r"\mathbb{R}^3: \quad \vec{v} = \begin{pmatrix} 1 \\ 4 \\ 2 \end{pmatrix}",
            font_size=40,
        ).shift(DOWN * 1.3)

        self.play(Write(examples_title))
        self.play(Write(r2_example))
        self.play(Write(r3_example))
        self.wait(2)

        self.play(*[FadeOut(m) for m in self.mobjects])


class AbstractVectorSpaceScene(Scene):
    def construct(self):
        title = Text("Abstract Vector Spaces", font_size=40).to_edge(UP)
        self.play(Write(title))

        statement = Text(
            "A vector is an element of a vector space.",
            font_size=32,
        )
        self.play(Write(statement))
        self.wait(2)
        self.play(statement.animate.scale(0.8).next_to(title, DOWN, buff=0.4))

        examples_title = Text("Examples: Functions as Vectors", font_size=28, color=YELLOW)
        examples_title.next_to(statement, DOWN, buff=0.4)
        self.play(Write(examples_title))

        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-1, 4, 1],
            x_length=7,
            y_length=4,
            tips=False,
        ).shift(DOWN * 0.8)

        f_graph = axes.plot(lambda x: 0.4 * x ** 2, color=BLUE, x_range=[-2.5, 2.5])
        g_graph = axes.plot(lambda x: 0.5 * x + 1, color=GREEN, x_range=[-2.5, 2.5])
        sum_graph = axes.plot(
            lambda x: 0.4 * x ** 2 + 0.5 * x + 1, color=RED, x_range=[-2.5, 2.5]
        )

        f_label = MathTex("f(x)", color=BLUE, font_size=28).to_corner(DL).shift(UP * 1.8 + RIGHT * 0.3)
        g_label = MathTex("g(x)", color=GREEN, font_size=28).next_to(f_label, DOWN, aligned_edge=LEFT)
        sum_label = MathTex("(f+g)(x)", color=RED, font_size=28).next_to(g_label, DOWN, aligned_edge=LEFT)

        self.play(Create(axes))
        self.play(Create(f_graph), Write(f_label))
        self.play(Create(g_graph), Write(g_label))
        self.wait(0.5)
        self.play(Create(sum_graph), Write(sum_label))
        self.wait(2.5)

        self.play(*[FadeOut(m) for m in self.mobjects])


class AxiomsScene(Scene):
    def construct(self):
        title = Text("Axioms of a Vector Space", font_size=40).to_edge(UP)
        self.play(Write(title))

        setup = MathTex(
            r"\forall \vec{u}, \vec{v}, \vec{w} \in V, \quad \forall c, d \in F",
            font_size=30,
        ).next_to(title, DOWN, buff=0.3)
        self.play(Write(setup))

        axioms = VGroup(
            MathTex(r"1.\; \vec{u} + \vec{v} = \vec{v} + \vec{u}", font_size=26),
            MathTex(r"2.\; (\vec{u} + \vec{v}) + \vec{w} = \vec{u} + (\vec{v} + \vec{w})", font_size=26),
            MathTex(r"3.\; \exists!\, \vec{0} \in V : \vec{v} + \vec{0} = \vec{v}", font_size=26),
            MathTex(r"4.\; \forall \vec{v},\; \exists!\, {-\vec{v}} : \vec{v} + (-\vec{v}) = \vec{0}", font_size=26),
            MathTex(r"5.\; c(d\vec{v}) = (cd)\vec{v}", font_size=26),
            MathTex(r"6.\; 1 \cdot \vec{v} = \vec{v}", font_size=26),
            MathTex(r"7.\; c(\vec{u} + \vec{v}) = c\vec{u} + c\vec{v}", font_size=26),
            MathTex(r"8.\; (c+d)\vec{v} = c\vec{v} + d\vec{v}", font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(setup, DOWN, buff=0.4)

        for axiom in axioms:
            self.play(Write(axiom), run_time=0.6)

        self.wait(3)
        self.play(*[FadeOut(m) for m in self.mobjects])

class DotProductScene(ThreeDScene):
    def construct(self):
        self.dot_intro()
        self.clear()
        self.dot_projection()
        self.clear()
        self.dot_angle_sweep()

    def dot_intro(self):
        title = Text("Dot Product", font_size=48).to_edge(UP)
        formula1 = MathTex(
            r"\vec{a} \cdot \vec{b} = \|\vec{a}\|\,\|\vec{b}\|\cos\theta"
        ).scale(0.9)
        formula2 = MathTex(
            r"\vec{a} \cdot \vec{b} = a_1 b_1 + a_2 b_2 + a_3 b_3"
        ).scale(0.9)
        formula1.next_to(title, DOWN, buff=0.8)
        formula2.next_to(formula1, DOWN, buff=0.5)
        self.play(Write(title))
        self.play(Write(formula1))
        self.play(Write(formula2))
        self.wait(2)

    def dot_projection(self):
        plane = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-3, 3, 1],
            background_line_style={"stroke_opacity": 0.3},
        )
        self.add(plane)

        a_vec = np.array([3.0, 1.0, 0.0])
        b_vec = np.array([2.0, 2.0, 0.0])

        a_arrow = Arrow(ORIGIN, a_vec, buff=0, color=BLUE, stroke_width=6)
        b_arrow = Arrow(ORIGIN, b_vec, buff=0, color=YELLOW, stroke_width=6)

        a_label = MathTex(r"\vec{a}", color=BLUE).next_to(a_arrow.get_end(), RIGHT)
        b_label = MathTex(r"\vec{b}", color=YELLOW).next_to(b_arrow.get_end(), UP)

        self.play(GrowArrow(a_arrow), Write(a_label))
        self.play(GrowArrow(b_arrow), Write(b_label))
        self.wait(0.5)

        a_unit = a_vec / np.linalg.norm(a_vec)
        proj_len = np.dot(b_vec, a_unit)
        proj_point = proj_len * a_unit

        proj_line = DashedLine(b_vec, proj_point, color=GREEN)
        proj_arrow = Arrow(ORIGIN, proj_point, buff=0, color=GREEN, stroke_width=8)

        proj_label = Text("projection of b onto a", font_size=24, color=GREEN)
        proj_label.next_to(proj_arrow, DOWN, buff=0.3)

        self.play(Create(proj_line))
        self.play(GrowArrow(proj_arrow))
        self.play(Write(proj_label))
        self.wait(1)

        dot_value = np.dot(a_vec, b_vec)
        result = MathTex(
            r"\vec{a} \cdot \vec{b} = " + f"{dot_value:.1f}",
            color=WHITE,
        ).to_corner(UR)
        self.play(Write(result))
        self.wait(2)

    def dot_angle_sweep(self):
        plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            background_line_style={"stroke_opacity": 0.3},
        )
        self.add(plane)

        a_vec = np.array([3.0, 0.0, 0.0])
        a_arrow = Arrow(ORIGIN, a_vec, buff=0, color=BLUE, stroke_width=6)
        a_label = MathTex(r"\vec{a}", color=BLUE).next_to(a_arrow, DOWN)

        theta = ValueTracker(0.5)

        def get_b():
            ang = theta.get_value()
            end = 3 * np.array([np.cos(ang), np.sin(ang), 0.0])
            return Arrow(ORIGIN, end, buff=0, color=YELLOW, stroke_width=6)

        def get_b_label():
            ang = theta.get_value()
            end = 3 * np.array([np.cos(ang), np.sin(ang), 0.0])
            return MathTex(r"\vec{b}", color=YELLOW).next_to(end, UP + RIGHT, buff=0.1)

        def get_dot_text():
            ang = theta.get_value()
            value = 3 * 3 * np.cos(ang)
            return MathTex(
                r"\vec{a} \cdot \vec{b} = " + f"{value:.2f}"
            ).to_corner(UR)

        b_arrow = always_redraw(get_b)
        b_label = always_redraw(get_b_label)
        dot_text = always_redraw(get_dot_text)

        self.play(GrowArrow(a_arrow), Write(a_label))
        self.add(b_arrow, b_label, dot_text)
        self.wait(0.5)
        self.play(theta.animate.set_value(PI), run_time=4, rate_func=smooth)
        self.wait(0.5)
        self.play(theta.animate.set_value(2 * PI), run_time=4, rate_func=smooth)
        self.wait(2)

        self.play(*[FadeOut(m) for m in self.mobjects])


class CrossProductScene(ThreeDScene):
    def construct(self):
        self.cross_intro()
        self.clear()
        self.cross_3d_demo()

    def cross_intro(self):
        title = Text("Cross Product", font_size=48).to_edge(UP)
        formula1 = MathTex(
            r"\|\vec{a} \times \vec{b}\| = \|\vec{a}\|\,\|\vec{b}\|\sin\theta"
        ).scale(0.9)
        formula2 = MathTex(
            r"\vec{a} \times \vec{b} = ",
            r"(a_2 b_3 - a_3 b_2,\;",
            r"a_3 b_1 - a_1 b_3,\;",
            r"a_1 b_2 - a_2 b_1)",
        ).scale(0.75)
        formula1.next_to(title, DOWN, buff=0.8)
        formula2.next_to(formula1, DOWN, buff=0.5)
        self.play(Write(title))
        self.play(Write(formula1))
        self.play(Write(formula2))
        self.wait(2)

    def cross_3d_demo(self):
        axes = ThreeDAxes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            z_range=[-4, 4, 1],
        )
        self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES)
        self.add(axes)

        a_vec = np.array([2.5, 0.5, 0.0])
        b_vec = np.array([0.5, 2.5, 0.0])
        c_vec = np.cross(a_vec, b_vec)

        a_arrow = Arrow3D(ORIGIN, a_vec, color=BLUE, thickness=0.03)
        b_arrow = Arrow3D(ORIGIN, b_vec, color=YELLOW, thickness=0.03)
        c_arrow = Arrow3D(ORIGIN, c_vec, color=RED, thickness=0.03)

        parallelogram = Polygon(
            ORIGIN,
            a_vec,
            a_vec + b_vec,
            b_vec,
            color=GREEN,
            fill_opacity=0.3,
            stroke_width=2,
        )

        a_label = MathTex(r"\vec{a}", color=BLUE).move_to(a_vec + 0.3 * UP)
        b_label = MathTex(r"\vec{b}", color=YELLOW).move_to(b_vec + 0.3 * UP)
        c_label = MathTex(r"\vec{a}\times\vec{b}", color=RED).move_to(c_vec + 0.4 * RIGHT)

        self.play(Create(a_arrow))
        self.play(Create(b_arrow))
        self.add_fixed_orientation_mobjects(a_label, b_label)
        self.play(Write(a_label), Write(b_label))
        self.wait(0.5)

        self.play(Create(parallelogram))
        area_text = Text(
            f"Area = |a x b| = {np.linalg.norm(c_vec):.2f}",
            font_size=28,
        ).to_corner(UL)
        self.add_fixed_in_frame_mobjects(area_text)
        self.play(Write(area_text))
        self.wait(1)

        self.play(Create(c_arrow))
        self.add_fixed_orientation_mobjects(c_label)
        self.play(Write(c_label))
        self.wait(1)

        self.begin_ambient_camera_rotation(rate=0.3)
        self.wait(8)
        self.stop_ambient_camera_rotation()
        self.wait(1)

        self.play(*[FadeOut(m) for m in self.mobjects])

class CombinedScene(ThreeDScene):
    def construct(self):
        title = Text("Dot vs Cross", font_size=56).to_edge(UP)
        self.play(Write(title))

        left = VGroup(
            Text("Dot Product", color=BLUE, font_size=36),
            MathTex(r"\vec{a}\cdot\vec{b} \in \mathbb{R}").scale(0.9),
            Text("scalar", font_size=24),
            Text("Zero if Perpendicular", font_size=22),
        ).arrange(DOWN, buff=0.4).shift(LEFT * 3.5)

        right = VGroup(
            Text("Cross Product", color=RED, font_size=36),
            MathTex(r"\vec{a}\times\vec{b} \in \mathbb{R}^3").scale(0.9),
            Text("Vector", font_size=24),
            Text("Zero if Parallel", font_size=22),
        ).arrange(DOWN, buff=0.4).shift(RIGHT * 3.5)

        self.play(Write(left), Write(right))
        self.wait(3)
        self.play(*[FadeOut(m) for m in self.mobjects])

class FullPresentation(ThreeDScene):
    def construct(self):
        for cls in [IntroScene, EuclideanVectorScene, VectorOperationsScene,
                    AlgebraicVectorScene, AbstractVectorSpaceScene, AxiomsScene,
                    DotProductScene, CrossProductScene, CombinedScene]:
            scene = cls.__new__(cls)
            scene.__dict__ = self.__dict__
            cls.construct(scene)