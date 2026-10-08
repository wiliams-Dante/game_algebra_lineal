import pygame
import sys
from src.algebra.vector import Vector
from src.algebra.base import Base2D
import variables as v


# ============================================================
# Textos de cada modo
# ============================================================
def nombre_modo(m):
    return {
        v.MODO_ROTADA:    "1. Base ortonormal rotada",
        v.MODO_NO_ORT:    "2. Base NO ortogonal",
        v.MODO_LD:        "3. Base LD (NO es base)",
        v.MODO_INVERTIDA: "4. Base ortonormal invertida",
    }[m]


def descripcion_modo(m):
    return {
        v.MODO_ROTADA: [
            "La base gira con el movimiento.",
            "El cuadrado NO se deforma.",
            "Base valida y ortogonal.",
        ],
        v.MODO_NO_ORT: [
            "v1 y v2 NO son perpendiculares.",
            "<v1,v2> != 0.",
            "El cuadrado se deforma en",
            "paralelogramo.",
        ],
        v.MODO_LD: [
            "v1 y v2 son PARALELOS.",
            "det(B) = 0 => NO es base.",
            "El cuadrado COLAPSA a",
            "una linea.",
        ],
        v.MODO_INVERTIDA: [
            "Base ortonormal pero v2",
            "invertido respecto a Y.",
            "det(B) = -1 (reflexion).",
            "El cuadrado se espeja.",
        ],
    }[m]


# ============================================================
# Dibujo
# ============================================================
def dibujar(pantalla, posicion, base, modo, fuentes):
    fuente, fuente_peq, fuente_tit = fuentes

    # --- Área del juego ---
    pantalla.fill(v.COLOR_FONDO)
    pygame.draw.rect(pantalla, v.COLOR_FONDO, (0, 0, v.PANEL_X, v.HEIGHT))

    # Grid
    for x in range(0, v.PANEL_X, 50):
        pygame.draw.line(pantalla, v.COLOR_GRID, (x, 0), (x, v.HEIGHT))
    for y in range(0, v.HEIGHT, 50):
        pygame.draw.line(pantalla, v.COLOR_GRID, (0, y), (v.PANEL_X, y))

    # Ejes de la base
    fin_v1 = posicion + base.v1 * 80
    pygame.draw.line(pantalla, v.COLOR_EJE_V1,
                     (posicion.x, posicion.y), (fin_v1.x, fin_v1.y), 3)

    fin_v2 = posicion + base.v2 * 80
    pygame.draw.line(pantalla, v.COLOR_EJE_V2,
                     (posicion.x, posicion.y), (fin_v2.x, fin_v2.y), 3)

    # Cuadrado transformado por la base
    mitad = v.TAMANO_JUGADOR / 2
    esquinas_locales = [
        (-mitad, -mitad), (mitad, -mitad),
        (mitad, mitad), (-mitad, mitad),
    ]
    esquinas_mundo = []
    for cx, cy in esquinas_locales:
        e = posicion + base.reconstruir_desde_base(cx, cy)
        esquinas_mundo.append((e.x, e.y))

    pygame.draw.polygon(pantalla, v.COLOR_CUADRO[modo], esquinas_mundo)
    pygame.draw.polygon(pantalla, (255, 255, 255), esquinas_mundo, 1)

    # Texto de control
    t = fuente_peq.render(
        "Mover: WASD | Modo: 1,2,3,4 | Salir: ESC",
        True, v.COLOR_TEXTO_DIM)
    pantalla.blit(t, (15, v.HEIGHT - 25))

    # --- Panel lateral ---
    pygame.draw.rect(pantalla, v.COLOR_PANEL,
                     (v.PANEL_X, 0, v.WIDTH - v.PANEL_X, v.HEIGHT))
    pygame.draw.line(pantalla, v.COLOR_SEPARADOR,
                     (v.PANEL_X, 0), (v.PANEL_X, v.HEIGHT), 2)

    y = 15
    t = fuente_tit.render("GRUPO I - DEMO", True, v.COLOR_TITULO)
    pantalla.blit(t, (v.PANEL_X + 15, y)); y += 28

    t = fuente_peq.render("Modos con 1, 2, 3, 4", True, v.COLOR_TEXTO_DIM)
    pantalla.blit(t, (v.PANEL_X + 15, y)); y += 25

    t = fuente.render(nombre_modo(modo), True, v.COLOR_MODO)
    pantalla.blit(t, (v.PANEL_X + 15, y)); y += 30

    pygame.draw.line(pantalla, v.COLOR_SEPARADOR,
                     (v.PANEL_X + 15, y), (v.WIDTH - 15, y), 1)
    y += 10

    datos = [
        f"v1 = ({base.v1.x:.2f}, {base.v1.y:.2f})",
        f"v2 = ({base.v2.x:.2f}, {base.v2.y:.2f})",
        f"<v1,v2> = {base.v1.producto_punto(base.v2):.2f}",
        f"det(B)  = {base.determinante():.2f}",
    ]
    for txt in datos:
        t = fuente_peq.render(txt, True, v.COLOR_TEXTO)
        pantalla.blit(t, (v.PANEL_X + 15, y)); y += 22

    y += 8
    es_ort = base.es_conjunto_ortogonal()
    t = fuente_peq.render(f"Ortogonal: {'SI' if es_ort else 'NO'}",
                          True, v.COLOR_OK if es_ort else v.COLOR_ERROR)
    pantalla.blit(t, (v.PANEL_X + 15, y)); y += 22

    t = fuente_peq.render(f"Es base:   {'SI' if base.es_valida else 'NO'}",
                          True, v.COLOR_OK if base.es_valida else v.COLOR_ERROR)
    pantalla.blit(t, (v.PANEL_X + 15, y)); y += 22

    es_on = base.es_base_ortonormal()
    t = fuente_peq.render(f"Ortonormal:{'SI' if es_on else 'NO'}",
                          True, v.COLOR_OK if es_on else v.COLOR_ERROR)
    pantalla.blit(t, (v.PANEL_X + 15, y)); y += 30

    pygame.draw.line(pantalla, v.COLOR_SEPARADOR,
                     (v.PANEL_X + 15, y), (v.WIDTH - 15, y), 1)
    y += 15

    t = fuente_tit.render("Explicacion:", True, (200, 200, 200))
    pantalla.blit(t, (v.PANEL_X + 15, y)); y += 25

    for linea in descripcion_modo(modo):
        t = fuente_peq.render(linea, True, (180, 180, 180))
        pantalla.blit(t, (v.PANEL_X + 15, y)); y += 20


# ============================================================
# Bucle principal
# ============================================================
def main():
    pygame.init()
    pantalla = pygame.display.set_mode((v.WIDTH, v.HEIGHT))
    pygame.display.set_caption("Grupo I - Demo")
    reloj = pygame.time.Clock()

    fuentes = (
        pygame.font.SysFont("Arial", 18),
        pygame.font.SysFont("Arial", 14),
        pygame.font.SysFont("Arial", 16, bold=True),
    )

    posicion = Vector(v.PANEL_X / 2, v.HEIGHT / 2)
    velocidad = Vector(0, 0)
    modo_actual = v.MODO_ROTADA
    modo_anterior = None
    base_actual = Base2D(Vector(1, 0), Vector(0, 1))

    while True:
        dt = reloj.tick(v.FPS) / 1000.0

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1: modo_actual = v.MODO_ROTADA
                elif evento.key == pygame.K_2: modo_actual = v.MODO_NO_ORT
                elif evento.key == pygame.K_3: modo_actual = v.MODO_LD
                elif evento.key == pygame.K_4: modo_actual = v.MODO_INVERTIDA
                elif evento.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()

        # Física
        teclas = pygame.key.get_pressed()
        velocidad = Vector(0, 0)
        if teclas[pygame.K_LEFT]  or teclas[pygame.K_a]:
            velocidad = velocidad + Vector(-v.VELOCIDAD_MOV, 0)
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            velocidad = velocidad + Vector(v.VELOCIDAD_MOV, 0)
        if teclas[pygame.K_UP]    or teclas[pygame.K_w]:
            velocidad = velocidad + Vector(0, -v.VELOCIDAD_MOV)
        if teclas[pygame.K_DOWN]  or teclas[pygame.K_s]:
            velocidad = velocidad + Vector(0, v.VELOCIDAD_MOV)

        posicion = posicion + velocidad * dt

        # Álgebra: elegir la base según el modo
        if modo_actual != modo_anterior:
            if modo_actual == v.MODO_ROTADA:
                base_actual = Base2D(Vector(1, 0), Vector(0, 1))
            elif modo_actual == v.MODO_NO_ORT:
                base_actual = Base2D(Vector(1, 0), Vector(1, 1))
            elif modo_actual == v.MODO_LD:
                base_actual = Base2D(Vector(1, 1), Vector(2, 2))
            elif modo_actual == v.MODO_INVERTIDA:
                base_actual = Base2D(Vector(1, 0), Vector(0, -1))
            modo_anterior = modo_actual

        if modo_actual == v.MODO_ROTADA and velocidad.magnitud() > 0:
            v1 = velocidad.normalizar()
            v2 = Vector(-v1.y, v1.x)
            base_actual = Base2D(v1, v2)

        # Dibujar
        dibujar(pantalla, posicion, base_actual, modo_actual, fuentes)
        pygame.display.flip()


if __name__ == "__main__":
    main()