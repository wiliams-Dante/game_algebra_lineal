import pygame
import sys
import os
from src.algebra.vector import Vector
from src.algebra.base import Base2D
import variables as v

sys.stdout = open(os.devnull, "w")

INFO_MODO = {
    v.MODO_ROTADA: ("1. Base ortonormal rotada",
                    ["La base gira con el movimiento.",
                     "El cuadrado NO se deforma.",
                     "v1 y v2 forman un conjunto ortogonal."],
                    lambda: Base2D(Vector(1, 0), Vector(0, 1))),
    v.MODO_NO_ORT: ("2. Base NO ortogonal",
                    ["v1 y v2 NO son perpendiculares.",
                     "El producto interno no es cero.",
                     "El cuadrado se deforma en",
                     "paralelogramo."],
                    lambda: Base2D(Vector(1, 0), Vector(1, 1))),
    v.MODO_LD: ("3. Base LD (NO es base)",
                ["v1 y v2 son PARALELOS.",
                 "det(B) = 0 => NO es base.",
                 "Generan solo un SUBESPACIO",
                 "de dimension 1 (una recta).",
                 "El cuadrado COLAPSA a",
                 "una linea."],
                lambda: Base2D(Vector(1, 1), Vector(2, 2))),
    v.MODO_INVERTIDA: ("4. Base ortonormal invertida",
                       ["Base ortonormal pero v2",
                        "invertido respecto a Y.",
                        "Orientacion NEGATIVA (det < 0).",
                        "El cuadrado se espeja."],
                       lambda: Base2D(Vector(1, 0), Vector(0, -1))),
}


def texto(pantalla, txt, fuente, color, x, y, salto=22):
    pantalla.blit(fuente.render(txt, True, color), (x, y))
    return y + salto


def sep(pantalla, x, y):
    pygame.draw.line(pantalla, v.COLOR_SEPARADOR,
                     (x, y), (v.WIDTH - 15, y), 1)
    return y + 10


def dibujar(pantalla, pos, base, modo, fuentes):
    f, fp, ft = fuentes
    pantalla.fill(v.COLOR_FONDO)

    for vector, color in [(base.v1, v.COLOR_EJE_V1), (base.v2, v.COLOR_EJE_V2)]:
        fin = pos + vector * 80
        pygame.draw.line(pantalla, color, (pos.x, pos.y), (fin.x, fin.y), 3)

    m = v.TAMANO_JUGADOR / 2
    poligono = [(pos + base.reconstruir_desde_base(cx, cy))
                for cx, cy in [(-m, -m), (m, -m), (m, m), (-m, m)]]
    poligono = [(p.x, p.y) for p in poligono]

    pygame.draw.polygon(pantalla, v.COLOR_CUADRO[modo], poligono)
    pygame.draw.polygon(pantalla, v.COLOR_TEXTO, poligono, 1)
    pygame.draw.circle(pantalla, v.COLOR_TEXTO, (int(pos.x), int(pos.y)), 3)

    pygame.draw.rect(pantalla, v.COLOR_PANEL,
                     (v.PANEL_X, 0, v.WIDTH - v.PANEL_X, v.HEIGHT))
    pygame.draw.line(pantalla, v.COLOR_SEPARADOR,
                     (v.PANEL_X, 0), (v.PANEL_X, v.HEIGHT), 2)

    x, y = v.PANEL_X + 15, 15
    y = texto(pantalla, INFO_MODO[modo][0], f, v.COLOR_MODO, x, y, 30)
    y = sep(pantalla, x, y)

    y = texto(pantalla, "Posicion en tiempo real:", fp, v.COLOR_TITULO, x, y)
    y = texto(pantalla, f"P (mundo) = ({pos.x:.1f}, {pos.y:.1f})", fp,
              v.COLOR_TEXTO, x, y)

    if base.es_valida:
        c = base.cambiar_de_base(pos)
        y = texto(pantalla, f"P (base B) = ({c.x:.2f}, {c.y:.2f})", fp,
                  v.COLOR_MODO, x, y)
    else:
        y = texto(pantalla, "P (base B) = no definido (LD)", fp,
                  v.COLOR_ERROR, x, y)

    y = sep(pantalla, x, y + 8)

    for d in [f"v1 = ({base.v1.x:.2f}, {base.v1.y:.2f})",
              f"v2 = ({base.v2.x:.2f}, {base.v2.y:.2f})",
              f"<v1,v2> = {base.v1.producto_punto(base.v2):.2f}",
              f"det(B)  = {base.determinante():.2f}"]:
        y = texto(pantalla, d, fp, v.COLOR_TEXTO, x, y)

    y += 8
    for etiqueta, valor in [("Ortogonal:",  base.es_conjunto_ortogonal()),
                            ("Es base:  ",  base.es_valida),
                            ("Ortonormal:", base.es_base_ortonormal())]:
        color = v.COLOR_OK if valor else v.COLOR_ERROR
        y = texto(pantalla, f"{etiqueta} {'SI' if valor else 'NO'}", fp,
                  color, x, y)

    y = sep(pantalla, x, y + 15)
    y = texto(pantalla, "Explicacion:", ft, v.COLOR_TEXTO_DIM, x, y, 25)
    for linea in INFO_MODO[modo][1]:
        y = texto(pantalla, linea, fp, v.COLOR_TEXTO_DIM, x, y, 20)


def main():
    pygame.init()
    pantalla = pygame.display.set_mode((v.WIDTH, v.HEIGHT))
    pygame.display.set_caption("Grupo I - Demo")
    reloj = pygame.time.Clock()
    fuentes = (pygame.font.SysFont("Arial", 18),
               pygame.font.SysFont("Arial", 14),
               pygame.font.SysFont("Arial", 16, bold=True))

    CONTROLES = [
        ((pygame.K_LEFT,  pygame.K_a), (-1, 0)),
        ((pygame.K_RIGHT, pygame.K_d), ( 1, 0)),
        ((pygame.K_UP,    pygame.K_w), ( 0,-1)),
        ((pygame.K_DOWN,  pygame.K_s), ( 0, 1)),
    ]
    TECLAS_MODO = {pygame.K_1: v.MODO_ROTADA, pygame.K_2: v.MODO_NO_ORT,
                   pygame.K_3: v.MODO_LD,     pygame.K_4: v.MODO_INVERTIDA}

    posicion = Vector(v.PANEL_X / 2, v.HEIGHT / 2)
    modo_actual, modo_anterior = v.MODO_ROTADA, None
    base_actual = Base2D(Vector(1, 0), Vector(0, 1))

    while True:
        dt = reloj.tick(v.FPS) / 1000.0

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key in TECLAS_MODO: modo_actual = TECLAS_MODO[e.key]
                elif e.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()

        teclas = pygame.key.get_pressed()
        velocidad = Vector(0, 0)
        for (k1, k2), (dx, dy) in CONTROLES:
            if teclas[k1] or teclas[k2]:
                velocidad = velocidad + Vector(dx * v.VELOCIDAD_MOV,
                                               dy * v.VELOCIDAD_MOV)
        posicion = posicion + velocidad * dt

        if modo_actual != modo_anterior:
            base_actual = INFO_MODO[modo_actual][2]()
            modo_anterior = modo_actual

        if modo_actual == v.MODO_ROTADA and velocidad.magnitud() > 0:
            v1 = velocidad.normalizar()
            base_actual = Base2D(v1, Vector(-v1.y, v1.x))

        dibujar(pantalla, posicion, base_actual, modo_actual, fuentes)
        pygame.display.flip()


if __name__ == "__main__":
    main()