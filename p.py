from manim import *
import math

class ExplicacionDetalladaVector(Scene):
    def construct(self):
        # 1. Escenario
        grid = NumberPlane(
            x_range=[-4, 6, 1],
            y_range=[-3, 4, 1],
            axis_config={"include_numbers": True}
        )
        self.add(grid)

        # Caja de texto explicativa arriba en la pantalla
        caja_info = Rectangle(width=12, height=1.5, color=WHITE, fill_color=BLACK, fill_opacity=0.8).to_edge(UP)
        texto_metodo = Text("MÉTODO DE TU CLASE", font_size=20, color=YELLOW).move_to(caja_info.get_center() + UP * 0.4)
        texto_explicacion = Text("Explicación de qué hace en el juego", font_size=16, color=WHITE).move_to(caja_info.get_center() + DOWN * 0.2)
        
        self.add(caja_info, texto_metodo, texto_explicacion)

        # -------------------------------------------------------------
        # PASO 1: __init__ y __repr__
        # -------------------------------------------------------------
        texto_metodo.become(Text("1. __init__(x, y) y __repr__()", font_size=20, color=YELLOW).move_to(caja_info.get_center() + UP * 0.4))
        texto_explicacion.become(Text("Aparece el personaje 'Zombie' en la posición (3, 1)", font_size=16, color=WHITE).move_to(caja_info.get_center() + DOWN * 0.2))

        pos_zombie = Dot(grid.c2p(3, 1), color=RED, radius=0.25)
        label_zombie = Text("Zombie (3, 1)", font_size=14, color=RED).next_to(pos_zombie, UR)

        self.play(FadeIn(pos_zombie), Write(label_zombie))
        self.wait(2)

        # -------------------------------------------------------------
        # PASO 2: magnitud()
        # -------------------------------------------------------------
        texto_metodo.become(Text("2. magnitud(): pos.magnitud()", font_size=20, color=YELLOW).move_to(caja_info.get_center() + UP * 0.4))
        texto_explicacion.become(Text("¿A qué distancia está el Zombie del punto (0,0)? -> Teorema de Pitágoras", font_size=16, color=WHITE).move_to(caja_info.get_center() + DOWN * 0.2))

        linea_distancia = Line(grid.c2p(0, 0), grid.c2p(3, 1), color=YELLOW)
        label_dist = MathTex(r"\text{Distancia} = \sqrt{3^2 + 1^2} \approx 3.16", color=YELLOW, font_size=24).move_to(grid.c2p(1.5, -1))

        self.play(Create(linea_distancia), Write(label_dist))
        self.wait(2)
        self.play(FadeOut(linea_distancia), FadeOut(label_dist))

        # -------------------------------------------------------------
        # PASO 3: normalizar()
        # -------------------------------------------------------------
        texto_metodo.become(Text("3. normalizar(): pos.normalizar()", font_size=20, color=YELLOW).move_to(caja_info.get_center() + UP * 0.4))
        texto_explicacion.become(Text("Extrae SOLO LA DIRECCIÓN a la que mira el Zombie (una flecha de tamaño 1)", font_size=16, color=WHITE).move_to(caja_info.get_center() + DOWN * 0.2))

        # Flecha de dirección unitaria
        mag = math.sqrt(3**2 + 1**2)
        flecha_dir = Arrow(grid.c2p(3, 1), grid.c2p(3 + 3/mag, 1 + 1/mag), buff=0, color=ORANGE)
        label_dir = Text("Dirección pura", font_size=12, color=ORANGE).next_to(flecha_dir, DR)

        self.play(GrowArrow(flecha_dir), Write(label_dir))
        self.wait(2)

        # -------------------------------------------------------------
        # PASO 4: __mul__ (Multiplicación por escalar)
        # -------------------------------------------------------------
        texto_metodo.become(Text("4. __mul__: direccion * rapidez", font_size=20, color=YELLOW).move_to(caja_info.get_center() + UP * 0.4))
        texto_explicacion.become(Text("Estira la flecha de dirección según la velocidad a la que camina el Zombie", font_size=16, color=WHITE).move_to(caja_info.get_center() + DOWN * 0.2))

        rapidez = 1.8
        flecha_vel = Arrow(grid.c2p(3, 1), grid.c2p(3 + (3/mag)*rapidez, 1 + (1/mag)*rapidez), buff=0, color=TEAL)
        label_vel = Text("Velocidad de paso", font_size=12, color=TEAL).next_to(flecha_vel, DR)

        self.play(Transform(flecha_dir, flecha_vel), Transform(label_dir, label_vel))
        self.wait(2)

        # -------------------------------------------------------------
        # PASO 5: __add__ (Suma de vectores)
        # -------------------------------------------------------------
        texto_metodo.become(Text("5. __add__: pos_nueva = pos_actual + velocidad", font_size=20, color=YELLOW).move_to(caja_info.get_center() + UP * 0.4))
        texto_explicacion.become(Text("Suma el paso a la posición actual para MOVER AL ZOMBIE en pantalla", font_size=16, color=WHITE).move_to(caja_info.get_center() + DOWN * 0.2))

        nueva_x = 3 + (3/mag)*rapidez
        nueva_y = 1 + (1/mag)*rapidez

        self.play(
            pos_zombie.animate.move_to(grid.c2p(nueva_x, nueva_y)),
            label_zombie.animate.next_to(grid.c2p(nueva_x, nueva_y), UR),
            FadeOut(flecha_dir),
            FadeOut(label_dir)
        )
        self.wait(2)

        # -------------------------------------------------------------
        # PASO 6: __sub__ (Resta de vectores)
        # -------------------------------------------------------------
        texto_metodo.become(Text("6. __sub__: direccion = pos_jugador - pos_zombie", font_size=20, color=YELLOW).move_to(caja_info.get_center() + UP * 0.4))
        texto_explicacion.become(Text("Calcula la flecha que apunta directamente desde el Zombie hacia el Jugador", font_size=16, color=WHITE).move_to(caja_info.get_center() + DOWN * 0.2))

        # Crear Jugador
        pos_jugador = Dot(grid.c2p(-1, 3), color=GREEN, radius=0.25)
        label_jugador = Text("Jugador (-1, 3)", font_size=14, color=GREEN).next_to(pos_jugador, UL)
        self.play(FadeIn(pos_jugador), Write(label_jugador))

        # Vector persecución: Jugador - Zombie
        flecha_persecucion = Arrow(grid.c2p(nueva_x, nueva_y), grid.c2p(-1, 3), buff=0.25, color=PURPLE)
        label_pers = Text("Vector para perseguir", font_size=12, color=PURPLE).next_to(flecha_persecucion.get_center(), UP)

        self.play(GrowArrow(flecha_persecucion), Write(label_pers))
        self.wait(2)
        self.play(FadeOut(flecha_persecucion), FadeOut(label_pers))

        # -------------------------------------------------------------
        # PASO 7: producto_punto()
        # -------------------------------------------------------------
        texto_metodo.become(Text("7. producto_punto(otro_vector)", font_size=20, color=YELLOW).move_to(caja_info.get_center() + UP * 0.4))
        texto_explicacion.become(Text("¿El Zombie está viendo al Jugador? (Resultado negativo = está a sus espaldas)", font_size=16, color=WHITE).move_to(caja_info.get_center() + DOWN * 0.2))

        # Mira del Zombie (hacia la derecha)
        mira = Arrow(grid.c2p(nueva_x, nueva_y), grid.c2p(nueva_x + 1.5, nueva_y), buff=0, color=RED)
        label_mira = Text("Mira del Zombie", font_size=12, color=RED).next_to(mira, RIGHT)

        # Línea de visión hacia el jugador
        linea_vision = DashedLine(grid.c2p(nueva_x, nueva_y), grid.c2p(-1, 3), color=GREEN)

        self.play(GrowArrow(mira), Write(label_mira), Create(linea_vision))
        self.wait(3)