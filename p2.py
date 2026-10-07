from manim import *

class ExplicacionBase2D(Scene):
    def construct(self):
        # 1. Escenario / Plano cartesiano
        grid = NumberPlane(
            x_range=[-3, 6, 1],
            y_range=[-3, 5, 1],
            axis_config={"include_numbers": True}
        )
        self.add(grid)

        # Caja de texto informativa arriba en la pantalla
        caja_info = Rectangle(width=13, height=1.6, color=WHITE, fill_color=BLACK, fill_opacity=0.85).to_edge(UP)
        texto_metodo = Text("MÉTODO DE LA CLASE Base2D", font_size=18, color=YELLOW).move_to(caja_info.get_center() + UP * 0.45)
        texto_explicacion = Text("Explicación paso a paso", font_size=15, color=WHITE).move_to(caja_info.get_center() + DOWN * 0.15)
        
        self.add(caja_info, texto_metodo, texto_explicacion)

        # -------------------------------------------------------------
        # 1. __init__ y __repr__
        # -------------------------------------------------------------
        texto_metodo.become(Text("1. __init__(v1, v2) y __repr__()", font_size=18, color=YELLOW).move_to(caja_info.get_center() + UP * 0.45))
        texto_explicacion.become(Text("Definimos la Base B = {v1=(2, 1), v2=(1, 3)} con dos vectores", font_size=15, color=WHITE).move_to(caja_info.get_center() + DOWN * 0.15))

        v1_vec = Arrow(grid.c2p(0, 0), grid.c2p(2, 1), buff=0, color=BLUE, stroke_width=5)
        label_v1 = MathTex(r"\vec{v}_1 = (2, 1)", color=BLUE, font_size=20).next_to(v1_vec.get_end(), DR)

        v2_vec = Arrow(grid.c2p(0, 0), grid.c2p(1, 3), buff=0, color=GREEN, stroke_width=5)
        label_v2 = MathTex(r"\vec{v}_2 = (1, 3)", color=GREEN, font_size=20).next_to(v2_vec.get_end(), UL)

        self.play(GrowArrow(v1_vec), Write(label_v1), GrowArrow(v2_vec), Write(label_v2))
        self.wait(2)

        # -------------------------------------------------------------
        # 2. determinante()
        # -------------------------------------------------------------
        texto_metodo.become(Text("2. determinante(): det = v1_x*v2_y - v1_y*v2_x", font_size=18, color=YELLOW).move_to(caja_info.get_center() + UP * 0.45))
        texto_explicacion.become(Text("det(B) = (2)(3) - (1)(1) = 5 -> Es el ÁREA del paralelogramo que forman", font_size=15, color=WHITE).move_to(caja_info.get_center() + DOWN * 0.15))

        # Paralelogramo de área del determinante
        paralelogramo = Polygon(
            grid.c2p(0, 0),
            grid.c2p(2, 1),
            grid.c2p(3, 4),
            grid.c2p(1, 3),
            color=YELLOW, fill_color=YELLOW, fill_opacity=0.3
        )
        label_area = MathTex(r"\text{Área} = 5", color=YELLOW, font_size=22).move_to(grid.c2p(1.5, 2))

        self.play(DrawBorderThenFill(paralelogramo), Write(label_area))
        self.wait(2.5)
        self.play(FadeOut(paralelogramo), FadeOut(label_area))

        # -------------------------------------------------------------
        # 3. es_linealmente_dependiente()
        # -------------------------------------------------------------
        texto_metodo.become(Text("3. es_linealmente_dependiente(): abs(det) == 0", font_size=18, color=YELLOW).move_to(caja_info.get_center() + UP * 0.45))
        texto_explicacion.become(Text("Como det(B) = 5 != 0, los vectores NO están colineales -> Son LI (Base válida)", font_size=15, color=WHITE).move_to(caja_info.get_center() + DOWN * 0.15))

        self.wait(2.5)

        # -------------------------------------------------------------
        # 4. es_conjunto_ortogonal()
        # -------------------------------------------------------------
        texto_metodo.become(Text("4. es_conjunto_ortogonal(): v1.producto_punto(v2) == 0", font_size=18, color=YELLOW).move_to(caja_info.get_center() + UP * 0.45))
        texto_explicacion.become(Text("v1 · v2 = (2)(1) + (1)(3) = 5 != 0 -> NO forman 90º (No es ortogonal)", font_size=15, color=WHITE).move_to(caja_info.get_center() + DOWN * 0.15))

        # Muestra el ángulo entre v1 y v2
        angulo = Angle(v1_vec, v2_vec, radius=0.6, color=RED)
        label_angulo = MathTex(r"\theta \neq 90^\circ", color=RED, font_size=20).next_to(angulo, UR, buff=0.1)

        self.play(Create(angulo), Write(label_angulo))
        self.wait(2.5)
        self.play(FadeOut(angulo), FadeOut(label_angulo))

        # -------------------------------------------------------------
        # 5. cambiar_de_base(v)
        # -------------------------------------------------------------
        texto_metodo.become(Text("5. cambiar_de_base(v = Vector(4, 7)) -> [v]_B", font_size=18, color=YELLOW).move_to(caja_info.get_center() + UP * 0.45))
        texto_explicacion.become(Text("¿Cuántos v1 y v2 necesito para llegar al Vector v? -> Regla de Cramer: (c1=1, c2=2)", font_size=15, color=WHITE).move_to(caja_info.get_center() + DOWN * 0.15))

        # Vector en base estándar v = (4, 7)
        v_canonica = Arrow(grid.c2p(0, 0), grid.c2p(4, 7), buff=0, color=RED, stroke_width=6)
        label_v = MathTex(r"\vec{v} = (4, 7)", color=RED, font_size=20).next_to(v_canonica.get_end(), UR)

        self.play(GrowArrow(v_canonica), Write(label_v))
        self.wait(1.5)

        # -------------------------------------------------------------
        # 6. reconstruir_desde_base(c1, c2)
        # -------------------------------------------------------------
        texto_metodo.become(Text("6. reconstruir_desde_base(c1=1, c2=2) -> c1*v1 + c2*v2", font_size=18, color=YELLOW).move_to(caja_info.get_center() + UP * 0.45))
        texto_explicacion.become(Text("Comprobación: 1 * (2, 1) + 2 * (1, 3) = (2, 1) + (2, 6) = (4, 7)", font_size=15, color=WHITE).move_to(caja_info.get_center() + DOWN * 0.15))

        # 1*v1
        paso_v1 = Arrow(grid.c2p(0, 0), grid.c2p(2, 1), buff=0, color=BLUE_A, stroke_width=4)
        label_paso_v1 = MathTex(r"1 \cdot \vec{v}_1", color=BLUE_A, font_size=18).next_to(paso_v1.get_center(), DR)

        # + 2*v2 (desde la punta de v1 hasta v)
        paso_v2 = Arrow(grid.c2p(2, 1), grid.c2p(4, 7), buff=0, color=GREEN_A, stroke_width=4)
        label_paso_v2 = MathTex(r"2 \cdot \vec{v}_2", color=GREEN_A, font_size=18).next_to(paso_v2.get_center(), UL)

        self.play(Create(paso_v1), Write(label_paso_v1))
        self.play(Create(paso_v2), Write(label_paso_v2))
        self.wait(3)