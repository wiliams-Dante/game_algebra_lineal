from manim import *

class PresentacionCompleta(Scene):
    def construct(self):
        # ===========================================================
        # SECCIÓN 1: Espacios Vectoriales (R2) y Movimiento del Personaje
        # ===========================================================
        t1 = Text("Espacios Vectoriales (R²) y Movimiento del Personaje", font_size=26, color=BLUE_B).to_edge(UP)
        self.play(Write(t1))

        axes1 = Axes(
            x_range=[0, 18, 2],
            y_range=[-2, 10, 2],
            x_length=9,
            y_length=4,
            axis_config={"include_numbers": True}
        ).shift(LEFT * 1.5 + DOWN * 0.5)
        self.play(Create(axes1))

        # Panel explicativo lateral
        panel1 = Rectangle(width=3.8, height=4.5, color=WHITE, fill_opacity=0.1).to_edge(RIGHT)
        txt_box1 = VGroup(
            Text("Concepto Matemático:", font_size=15, color=YELLOW),
            Text("• Posición = Vector en R²", font_size=13),
            Text("• Desplazamiento =", font_size=13),
            Text("  Suma de Vectores:", font_size=13),
            MathTex("P_1 = P_0 + d_1", font_size=18, color=GREEN),
            Text("• Velocidad =", font_size=13),
            Text("  Escalado de Vectores", font_size=13)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(panel1)

        self.play(Create(panel1), Write(txt_box1))
        self.wait(2)

        p0_coord = axes1.c2p(2, 6)
        p1_coord = axes1.c2p(6, 6)
        p2_coord = axes1.c2p(12, 6)
        origin1 = axes1.c2p(0, 0)

        dot0 = Dot(p0_coord, color=BLUE, radius=0.25)
        dot1 = Dot(p1_coord, color=GREEN, radius=0.25)
        dot2 = Dot(p2_coord, color=PINK, radius=0.25)

        lbl0 = MathTex("P_0(2, 6)", font_size=18).next_to(dot0, UP)
        lbl1 = MathTex("P_1(6, 6)", font_size=18).next_to(dot1, UP)
        lbl2 = MathTex("P_2(12, 6)", font_size=18).next_to(dot2, UP)

        v_orig0 = Arrow(origin1, p0_coord, buff=0, color=TEAL, stroke_width=2)
        v_orig1 = Arrow(origin1, p1_coord, buff=0, color=GREEN_E, stroke_width=2)
        v_orig2 = Arrow(origin1, p2_coord, buff=0, color=MAROON, stroke_width=2)

        v_disp1 = Arrow(p0_coord, p1_coord, buff=0.2, color=GREEN, stroke_width=4)
        v_disp2 = Arrow(p1_coord, p2_coord, buff=0.2, color=PINK, stroke_width=4)

        lbl_v1 = MathTex("d_1 = 1.0 \\cdot (4,0)", font_size=16, color=GREEN).next_to(v_disp1, UP)
        lbl_v2 = MathTex("d_2 = 1.5 \\cdot (4,0)", font_size=16, color=PINK).next_to(v_disp2, UP)

        self.play(Create(v_orig0), FadeIn(dot0), Write(lbl0))
        self.wait(1.5)

        self.play(GrowArrow(v_disp1), Write(lbl_v1))
        self.play(Create(v_orig1), FadeIn(dot1), Write(lbl1))
        self.wait(1.5)

        self.play(GrowArrow(v_disp2), Write(lbl_v2))
        self.play(Create(v_orig2), FadeIn(dot2), Write(lbl2))
        self.wait(4)

        self.play(FadeOut(*self.mobjects))

        # ===========================================================
        # SECCIÓN 2: Subespacios Vectoriales y Plataformas del Juego
        # ===========================================================
        t2 = Text("Subespacios Vectoriales y Plataformas del Juego", font_size=26, color=BLUE_B).to_edge(UP)
        self.play(Write(t2))

        axes2 = Axes(
            x_range=[0, 28, 5],
            y_range=[0, 14, 2],
            x_length=9,
            y_length=4,
            axis_config={"include_numbers": True}
        ).shift(LEFT * 1.5 + DOWN * 0.5)
        self.play(Create(axes2))

        panel2 = Rectangle(width=3.8, height=4.5, color=WHITE, fill_opacity=0.1).to_edge(RIGHT)
        txt_box2 = VGroup(
            Text("Evaluación de Pertenencia:", font_size=15, color=YELLOW),
            Text("• Plataformas = Subespacios", font_size=13),
            MathTex("S_1 = \\{(x,y) \\in R^2 : y = 6\\}", font_size=14, color=PURPLE),
            MathTex("S_2 = \\{(x,y) \\in R^2 : y = 4\\}", font_size=14, color=BLUE),
            Text("• Si la posición (x,y) \\notin S:", font_size=13),
            Text("  se activa la física de CAÍDA.", font_size=13, color=RED)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(panel2)

        self.play(Create(panel2), Write(txt_box2))
        self.wait(2)

        plat1 = Rectangle(width=axes2.x_axis.unit_size * 12, height=0.25, color=PURPLE, fill_opacity=0.6).move_to(axes2.c2p(10, 6))
        plat2 = Rectangle(width=axes2.x_axis.unit_size * 10, height=0.25, color=BLUE, fill_opacity=0.6).move_to(axes2.c2p(19, 4))

        lbl_plat1 = Text("Subespacio S1 (y = 6)", font_size=14, color=PURPLE).next_to(plat1, UP)
        lbl_plat2 = Text("Subespacio S2 (y = 4)", font_size=14, color=BLUE).next_to(plat2, DOWN)

        self.play(FadeIn(plat1, plat2), Write(lbl_plat1), Write(lbl_plat2))
        self.wait(1.5)

        j1 = Dot(axes2.c2p(6, 6.4), color=GREEN, radius=0.25)
        lbl_j1 = Text("Jugador 1 [En S1]", font_size=13, color=GREEN).next_to(j1, UP)

        e1 = Dot(axes2.c2p(18, 4.4), color=TEAL, radius=0.25)
        lbl_e1 = Text("Enemigo 1 [En S2]", font_size=13, color=TEAL).next_to(e1, UP)

        e2 = Dot(axes2.c2p(18, 9.5), color=RED, radius=0.25)
        lbl_e2 = Text("Enemigo 2 [Sin Subespacio -> Caída]", font_size=13, color=RED).next_to(e2, UP)

        self.play(FadeIn(j1, lbl_j1))
        self.wait(1)
        self.play(FadeIn(e1, lbl_e1))
        self.wait(1)
        self.play(FadeIn(e2, lbl_e2))
        self.wait(4)

        self.play(FadeOut(*self.mobjects))

        # ===========================================================
        # SECCIÓN 3: Transformaciones Lineales y Cambio de Orientación
        # ===========================================================
        t3 = Text("Transformaciones Lineales y Cambio de Orientación", font_size=26, color=BLUE_B).to_edge(UP)
        self.play(Write(t3))

        axes3 = Axes(
            x_range=[-12, 12, 3],
            y_range=[-1, 10, 2],
            x_length=9,
            y_length=4,
            axis_config={"include_numbers": True}
        ).shift(LEFT * 1.5 + DOWN * 0.5)
        self.play(Create(axes3))

        panel3 = Rectangle(width=3.8, height=4.5, color=WHITE, fill_opacity=0.1).to_edge(RIGHT)
        txt_box3 = VGroup(
            Text("Matriz de Transformación:", font_size=15, color=YELLOW),
            Text("• Matriz de Inversión P:", font_size=13),
            MathTex("P = \\begin{bmatrix} -1 & 0 \\\\ 0 & 1 \\end{bmatrix}", font_size=16, color=RED),
            Text("• Invierte habilidades", font_size=13),
            Text("  y ataques del personaje", font_size=13),
            Text("  al girar a la izquierda.", font_size=13)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(panel3)

        self.play(Create(panel3), Write(txt_box3))
        self.wait(2)

        origin3 = axes3.c2p(0, 4)
        player = Dot(origin3, color=BLUE, radius=0.3)
        lbl_player = Text("Personaje (0, 4)", font_size=15, color=BLUE).next_to(player, UP)
        self.play(FadeIn(player), Write(lbl_player))

        a_proj = Arrow(origin3, axes3.c2p(9, 7), color=YELLOW, buff=0)
        a_espada = Arrow(origin3, axes3.c2p(6, 5), color=GREEN, buff=0)
        lbl_proj = Text("Proyectil (9, 3)", font_size=13, color=YELLOW).next_to(a_proj.get_end(), RIGHT)
        lbl_espada = Text("Espada (6, 1)", font_size=13, color=GREEN).next_to(a_espada.get_end(), RIGHT)

        self.play(GrowArrow(a_proj), Write(lbl_proj))
        self.play(GrowArrow(a_espada), Write(lbl_espada))
        self.wait(2)

        a_proj_inv = Arrow(origin3, axes3.c2p(-9, 7), color=RED, buff=0)
        a_espada_inv = Arrow(origin3, axes3.c2p(-6, 5), color=RED, buff=0)
        lbl_proj_i = Text("P·Proyectil (-9, 3)", font_size=13, color=RED).next_to(a_proj_inv.get_end(), LEFT)
        lbl_espada_i = Text("P·Espada (-6, 1)", font_size=13, color=RED).next_to(a_espada_inv.get_end(), LEFT)

        self.play(
            TransformFromCopy(a_proj, a_proj_inv), Write(lbl_proj_i),
            run_time=2
        )
        self.play(
            TransformFromCopy(a_espada, a_espada_inv), Write(lbl_espada_i),
            run_time=2
        )
        self.wait(4)

        self.play(FadeOut(*self.mobjects))

        # ===========================================================
        # SECCIÓN 4: Norma Euclidiana y Detección de Colisiones (Hitboxes)
        # ===========================================================
        t4 = Text("Norma Euclidiana y Detección de Colisiones (Hitboxes)", font_size=25, color=BLUE_B).to_edge(UP)
        self.play(Write(t4))

        axes4 = Axes(
            x_range=[0, 22, 2],
            y_range=[2, 20, 2],
            x_length=8,
            y_length=4.5
        ).shift(LEFT * 1.5 + DOWN * 0.3)
        self.play(Create(axes4))

        panel4 = Rectangle(width=3.8, height=4.5, color=WHITE, fill_opacity=0.1).to_edge(RIGHT)
        txt_box4 = VGroup(
            Text("Cálculo de Distancia:", font_size=15, color=YELLOW),
            MathTex("d = \\|P_e - P_j\\|_2", font_size=16),
            MathTex("d = \\sqrt{\\Delta x^2 + \\Delta y^2}", font_size=15),
            Text("• Hitbox Circular r = 6.0", font_size=13, color=RED),
            Text("• d <= r -> IMPACTO", font_size=13, color=GREEN),
            Text("• d > r  -> FUERA", font_size=13, color=BLUE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(panel4)

        self.play(Create(panel4), Write(txt_box4))
        self.wait(2)

        p_pos = axes4.c2p(10, 10)
        p_dot = Dot(p_pos, color=PINK, radius=0.3)
        lbl_p = Text("Jugador (10, 10)", font_size=14, color=PINK).next_to(p_dot, DOWN)

        hitbox = Circle(radius=axes4.x_axis.unit_size * 6, color=RED, fill_opacity=0.2).move_to(p_pos)
        self.play(FadeIn(p_dot), Write(lbl_p), Create(hitbox))
        self.wait(1)

        e1_pos = axes4.c2p(14, 12)
        e3_pos = axes4.c2p(17, 7)

        e1 = Dot(e1_pos, color=GREEN, radius=0.25)
        e3 = Dot(e3_pos, color=BLUE, radius=0.25)

        lbl_e1 = Text("d = 4.47 [IMPACTO]", font_size=12, color=GREEN).next_to(e1, UP)
        lbl_e3 = Text("d = 7.62 [FUERA]", font_size=12, color=BLUE).next_to(e3, DOWN)

        line1 = DashedLine(p_pos, e1_pos, color=WHITE)
        line3 = DashedLine(p_pos, e3_pos, color=WHITE)

        self.play(Create(line1), FadeIn(e1), Write(lbl_e1))
        self.wait(1.5)
        self.play(Create(line3), FadeIn(e3), Write(lbl_e3))
        self.wait(4)

        self.play(FadeOut(*self.mobjects))

        # ===========================================================
        # SECCIÓN 5: Proyección Ortogonal y Física de Respuesta
        # ===========================================================
        t5 = Text("Proyección Ortogonal y Física de Respuesta", font_size=26, color=BLUE_B).to_edge(UP)
        self.play(Write(t5))

        axes5 = Axes(
            x_range=[-2, 24, 4],
            y_range=[-7, 7, 2],
            x_length=9,
            y_length=4,
            axis_config={"include_numbers": True}
        ).shift(LEFT * 1.5 + DOWN * 0.5)
        self.play(Create(axes5))

        panel5 = Rectangle(width=3.8, height=4.5, color=WHITE, fill_opacity=0.1).to_edge(RIGHT)
        txt_box5 = VGroup(
            Text("Descomposición Vectorial:", font_size=15, color=YELLOW),
            Text("• Colisión sobre la superficie:", font_size=13),
            MathTex("v = v_{\\perp} + v_{\\parallel}", font_size=16),
            Text("• v_perp (ortogonal) es", font_size=13),
            Text("  absorbida por el piso.", font_size=13, color=MAROON),
            Text("• v_paralelo genera el", font_size=13),
            Text("  deslizamiento continuo.", font_size=13, color=GREEN)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to(panel5)

        self.play(Create(panel5), Write(txt_box5))
        self.wait(2)

        piso = Line(axes5.c2p(-2, 0), axes5.c2p(24, 0), color=PURPLE, stroke_width=4)
        lbl_piso = Text("Superficie del Piso (y = 0)", font_size=14, color=PURPLE).next_to(piso, LEFT)
        self.play(Create(piso), Write(lbl_piso))

        normal = Arrow(axes5.c2p(2, 0), axes5.c2p(2, 4), color=WHITE, buff=0)
        lbl_normal = Text("Vector Normal n", font_size=12, color=WHITE).next_to(normal, UP)
        self.play(GrowArrow(normal), Write(lbl_normal))
        self.wait(1)

        p_a = axes5.c2p(5, 1)
        dot_a = Dot(p_a, color=TEAL, radius=0.25)

        v_caida_a = Arrow(p_a, axes5.c2p(10, -5), color=RED, buff=0)
        v_perp_a = Arrow(axes5.c2p(10, 1), axes5.c2p(10, -5), color=MAROON, buff=0)
        v_par_a = Arrow(p_a, axes5.c2p(10, 1), color=GREEN, buff=0)

        lbl_caida = Text("1. Vel. Incidente", font_size=12, color=RED).next_to(v_caida_a, DOWN)
        lbl_perp = Text("2. Comp. Ortogonal", font_size=11, color=MAROON).next_to(v_perp_a, RIGHT)
        lbl_par = Text("3. Deslizamiento", font_size=11, color=GREEN).next_to(v_par_a, UP)

        self.play(FadeIn(dot_a))
        self.play(GrowArrow(v_caida_a), Write(lbl_caida))
        self.wait(1.5)

        self.play(GrowArrow(v_perp_a), Write(lbl_perp))
        self.wait(1.5)

        self.play(GrowArrow(v_par_a), Write(lbl_par))
        self.wait(4)