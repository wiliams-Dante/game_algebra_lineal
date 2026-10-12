import pygame
import sys
import math
from src.algebra.vector import Vector
from src.algebra.base import Base2D

# ==================================================
# CONFIGURACION
# ==================================================
ANCHO, ALTO = 1300, 700
PANEL_X = 900
FPS = 60

VELOCIDAD = 2.0
VELOCIDAD_GIRO = 1.2
ESCALA_MUNDO = 70.0

COLOR_FONDO = (20, 20, 30)
COLOR_PANEL = (30, 30, 45)
COLOR_SEPARADOR = (80, 80, 120)
COLOR_TITULO = (255, 220, 100)
COLOR_MODO = (100, 200, 255)
COLOR_TEXTO = (220, 220, 220)
COLOR_TEXTO_DIM = (120, 120, 140)
COLOR_TEORIA = (180, 180, 200)
COLOR_OK = (100, 255, 100)
COLOR_ERROR = (255, 100, 100)

COLOR_V1 = (255, 140, 200)
COLOR_V2 = (140, 240, 255)
COLOR_P_CANONICA = (255, 255, 100)
COLOR_P_BASE = (100, 200, 255)
COLOR_RECON = (200, 200, 220)
COLOR_RECON2 = (140, 200, 160)
COLOR_ORIGEN = (255, 255, 255)

# Rosa tenue para las rectas generadas
COLOR_RECTA_V1 = (140, 80, 110)
COLOR_RECTA_V2 = (90, 130, 160)

R45 = math.sqrt(2) / 2

# ==================================================
# ORIGEN DEL MUNDO
# ==================================================
ORIGEN_MUNDO = Vector(PANEL_X / 2, ALTO / 2)


def a_pantalla(p):
    return (int(ORIGEN_MUNDO.x + p.x * ESCALA_MUNDO),
            int(ORIGEN_MUNDO.y - p.y * ESCALA_MUNDO))


# ==================================================
# HELPERS
# ==================================================
def texto(pantalla, txt, fuente, color, x, y, salto=22):
    pantalla.blit(fuente.render(txt, True, color), (x, y))
    return y + salto


def sep(pantalla, x, y):
    pygame.draw.line(pantalla, COLOR_SEPARADOR,
                     (x, y), (ANCHO - 12, y), 1)
    return y + 6


def linea_discontinua(pantalla, a, b, color, dash=8, gap=5):
    dx = b[0] - a[0]
    dy = b[1] - a[1]
    largo = (dx * dx + dy * dy) ** 0.5
    if largo == 0:
        return
    ux, uy = dx / largo, dy / largo
    pos = 0
    while pos < largo:
        fin = min(pos + dash, largo)
        p1 = (int(a[0] + ux * pos), int(a[1] + uy * pos))
        p2 = (int(a[0] + ux * fin), int(a[1] + uy * fin))
        pygame.draw.line(pantalla, color, p1, p2, 1)
        pos += dash + gap


def rotar_vector(vec, angulo):
    c = math.cos(angulo)
    s = math.sin(angulo)
    return Vector(vec.x * c - vec.y * s,
                  vec.x * s + vec.y * c)


# ==================================================
# DIBUJO
# ==================================================
def flecha(pantalla, origen, vector, color, grosor=3, radio_punta=5):
    fin = origen + vector
    pygame.draw.line(pantalla, color,
                     a_pantalla(origen), a_pantalla(fin), grosor)
    pygame.draw.circle(pantalla, color, a_pantalla(fin), radio_punta)


def dibujar_ejes(pantalla):
    pygame.draw.line(pantalla, (50, 50, 70),
                     a_pantalla(Vector(-4.5, 0)),
                     a_pantalla(Vector(4.5, 0)), 1)
    pygame.draw.line(pantalla, (50, 50, 70),
                     a_pantalla(Vector(0, -4)),
                     a_pantalla(Vector(0, 4)), 1)


def dibujar_recta_generada(pantalla, v, color, grosor=1):
    # Recta infinita que pasa por el origen con direccion de v
    if v.magnitud() < 1e-6:
        return
    d = v.normalizar()
    L = 8.0
    pygame.draw.line(pantalla, color,
                     a_pantalla(d * (-L)), a_pantalla(d * (L)), grosor)


# ==================================================
# DIBUJO DEL AREA DE JUEGO
# ==================================================
def dibujar_area(pantalla, base, P, c1, c2):
    o = Vector(0, 0)
    v1 = base.v1
    v2 = base.v2

    dibujar_ejes(pantalla)

    # Rectas generadas por v1 y v2 (rosa tenue)
    dibujar_recta_generada(pantalla, v1, COLOR_RECTA_V1, 1)
    dibujar_recta_generada(pantalla, v2, COLOR_RECTA_V2, 1)

    # Reconstruccion
    if base.es_valida and c1 is not None and c2 is not None:
        fin1 = v1 * c1
        fin2 = v2 * c2
        linea_discontinua(pantalla, a_pantalla(o), a_pantalla(fin1),
                          COLOR_RECON, 8, 5)
        linea_discontinua(pantalla, a_pantalla(fin1), a_pantalla(P),
                          COLOR_RECON, 8, 5)
        linea_discontinua(pantalla, a_pantalla(o), a_pantalla(fin2),
                          COLOR_RECON2, 6, 6)
        linea_discontinua(pantalla, a_pantalla(fin2), a_pantalla(P),
                          COLOR_RECON2, 6, 6)

    # Base
    flecha(pantalla, o, v1, COLOR_V1, 4, 6)
    flecha(pantalla, o, v2, COLOR_V2, 4, 6)

    # Punto P
    px, py = a_pantalla(P)
    pygame.draw.circle(pantalla, COLOR_P_CANONICA, (px, py), 9)
    pygame.draw.circle(pantalla, (30, 30, 30), (px, py), 9, 2)

    # Origen
    pygame.draw.circle(pantalla, COLOR_ORIGEN, a_pantalla(o), 6)

    # Etiquetas
    f_et = pygame.font.SysFont("Arial", 15, bold=True)

    def etiq(txt, vec, color, dx=10, dy=-14):
        px, py = a_pantalla(vec)
        pantalla.blit(f_et.render(txt, True, color),
                      (px + dx, py + dy))

    etiq("v1", v1, COLOR_V1)
    etiq("v2", v2, COLOR_V2)
    etiq("P", P, COLOR_P_CANONICA, 12, 10)


# ==================================================
# PANEL
# ==================================================
def dibujar_panel(pantalla, fuentes, base, P, c1, c2, angulo_base):
    f_tit, f_txt = fuentes
    x = PANEL_X + 15
    y = 10

    v1 = base.v1
    v2 = base.v2
    base_valida = base.es_valida
    det_B = base.determinante()

    # Titulo
    y = texto(pantalla, "TEMA 3: Bases y cambio de base",
              f_tit, COLOR_MODO, x, y, 22)

    y = sep(pantalla, x, y + 4)

    # --- AVISO SI NO ES BASE ---
    if not base_valida:
        y = texto(pantalla, "!! NO ES BASE !!",
                  f_tit, COLOR_ERROR, x, y, 20)
        y = texto(pantalla, "v1 y v2 paralelos (det = 0)",
                  f_txt, COLOR_ERROR, x, y, 14)
        y = sep(pantalla, x, y + 4)

    # --- Base actual ---
    y = texto(pantalla, "Base actual:",
              f_tit, COLOR_TITULO, x, y, 18)
    y = texto(pantalla, f"v1 = ({v1.x:5.2f}, {v1.y:5.2f})",
              f_txt, COLOR_V1, x, y, 16)
    y = texto(pantalla, f"v2 = ({v2.x:5.2f}, {v2.y:5.2f})",
              f_txt, COLOR_V2, x, y, 16)

    if base_valida:
        y = texto(pantalla,
                  f"det(B) = {det_B:6.3f}   base valida",
                  f_txt, COLOR_OK, x, y, 14)
    else:
        y = texto(pantalla,
                  f"det(B) = {det_B:6.3f}   NO es base",
                  f_txt, COLOR_ERROR, x, y, 14)

    if base.es_conjunto_ortogonal():
        y = texto(pantalla, "  Ortogonal: SI",
                  f_txt, COLOR_OK, x, y, 14)
    else:
        y = texto(pantalla, "  Ortogonal: NO",
                  f_txt, COLOR_TEXTO_DIM, x, y, 14)

    if base.es_base_ortonormal():
        y = texto(pantalla, "  Ortonormal: SI",
                  f_txt, COLOR_OK, x, y, 14)
    else:
        y = texto(pantalla, "  Ortonormal: NO",
                  f_txt, COLOR_TEXTO_DIM, x, y, 14)

    y = sep(pantalla, x, y + 6)

    # --- Punto P ---
    y = texto(pantalla, "El mismo punto P:",
              f_tit, COLOR_TITULO, x, y, 18)

    y = texto(pantalla,
              f"  P (canonica) = ({P.x:5.2f}, {P.y:5.2f})",
              f_txt, COLOR_P_CANONICA, x, y, 16)
    y = texto(pantalla,
              "    coef. de e1=(1,0) y e2=(0,1)",
              f_txt, COLOR_TEXTO_DIM, x, y, 13)

    if base_valida and c1 is not None and c2 is not None:
        y = texto(pantalla,
                  f"  P (base B)   = ({c1:5.2f}, {c2:5.2f})",
                  f_txt, COLOR_P_BASE, x, y, 16)
        y = texto(pantalla,
                  "    coef. de v1 y v2",
                  f_txt, COLOR_TEXTO_DIM, x, y, 13)
    else:
        y = texto(pantalla,
                  "  P (base B)   = no definido (LD)",
                  f_txt, COLOR_ERROR, x, y, 16)

    y = sep(pantalla, x, y + 6)

    # --- Reconstruccion ---
    y = texto(pantalla, "Reconstruccion:",
              f_tit, COLOR_TITULO, x, y, 18)
    y = texto(pantalla, "P = c1*v1 + c2*v2",
              f_txt, COLOR_TEORIA, x, y, 15)

    if base_valida and c1 is not None and c2 is not None:
        y = texto(pantalla,
                  f"  c1 = {c1:5.2f}   c2 = {c2:5.2f}",
                  f_txt, COLOR_TEORIA, x, y, 14)
        rec = base.reconstruir_desde_base(c1, c2)
        y = texto(pantalla,
                  f"  = ({rec.x:5.2f}, {rec.y:5.2f}) = P",
                  f_txt, COLOR_OK, x, y, 14)

    y = sep(pantalla, x, y + 6)

    # ==================================================
    # LAS 4 BASES
    # ==================================================
    y = texto(pantalla, "Las 4 bases a demostrar:",
              f_tit, COLOR_TITULO, x, y, 18)

    y = texto(pantalla, "  1. Canonica",
              f_txt, COLOR_TEXTO, x, y, 15)
    y = texto(pantalla, "  2. Rotada 45",
              f_txt, COLOR_TEXTO, x, y, 15)
    y = texto(pantalla, "  3. No ortogonal",
              f_txt, COLOR_TEXTO, x, y, 15)
    y = texto(pantalla, "  4. Invertida",
              f_txt, COLOR_TEXTO, x, y, 15)

    y = sep(pantalla, x, y + 6)

    # --- Controles ---
    y = texto(pantalla, "Controles:",
              f_tit, COLOR_TITULO, x, y, 18)
    for linea in [
        "WASD    mover P",
        "Flechas mover v1",
        "IJKL    mover v2",
        "Q / E   rotar base",
        "R       resetear",
        "ESC     salir",
    ]:
        y = texto(pantalla, linea, f_txt, COLOR_TEXTO_DIM, x, y, 14)


# ==================================================
# MAIN
# ==================================================
def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Tema 3: controlas base y vectores")
    reloj = pygame.time.Clock()

    f_tit = pygame.font.SysFont("Arial", 16, bold=True)
    f_txt = pygame.font.SysFont("Arial", 13)
    fuentes = (f_tit, f_txt)

    v1 = Vector(1.0, 0.0)   
    v2 = Vector(0.0, 1.0)   
    #v1 = Vector(3.0, 1.0)
    #v2 = Vector(6.0, 2.0)
    P = Vector(4.0, 2.0)

    angulo_base = 0.0

    while True:
        dt = reloj.tick(FPS) / 1000.0
        teclas = pygame.key.get_pressed()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                if e.key == pygame.K_r:
                    v1 = Vector(1.0, 0.0)
                    v2 = Vector(0.0, 1.0)
                    P = Vector(4.0, 2.0)
                    angulo_base = 0.0

        # Rotar base
        if teclas[pygame.K_q]:
            delta = VELOCIDAD_GIRO * dt
            v1 = rotar_vector(v1, delta)
            v2 = rotar_vector(v2, delta)
            angulo_base += delta
        if teclas[pygame.K_e]:
            delta = -VELOCIDAD_GIRO * dt
            v1 = rotar_vector(v1, delta)
            v2 = rotar_vector(v2, delta)
            angulo_base += delta

        # Mover P
        vel_p = Vector(0, 0)
        if teclas[pygame.K_a]: vel_p.x -= 1
        if teclas[pygame.K_d]: vel_p.x += 1
        if teclas[pygame.K_w]: vel_p.y += 1
        if teclas[pygame.K_s]: vel_p.y -= 1
        P = P + vel_p * (VELOCIDAD * dt)

        # Mover v1
        vel_v1 = Vector(0, 0)
        if teclas[pygame.K_LEFT]:  vel_v1.x -= 1
        if teclas[pygame.K_RIGHT]: vel_v1.x += 1
        if teclas[pygame.K_UP]:    vel_v1.y += 1
        if teclas[pygame.K_DOWN]:  vel_v1.y -= 1
        v1 = v1 + vel_v1 * (VELOCIDAD * dt)

        # Mover v2
        vel_v2 = Vector(0, 0)
        if teclas[pygame.K_j]: vel_v2.x -= 1
        if teclas[pygame.K_l]: vel_v2.x += 1
        if teclas[pygame.K_i]: vel_v2.y += 1
        if teclas[pygame.K_k]: vel_v2.y -= 1
        v2 = v2 + vel_v2 * (VELOCIDAD * dt)

        # Base y cambio
        base = Base2D(v1, v2)
        if base.es_valida:
            c = base.cambiar_de_base(P)
            c1, c2 = c.x, c.y
        else:
            c1, c2 = None, None

        # Dibujar
        pantalla.fill(COLOR_FONDO)
        dibujar_area(pantalla, base, P, c1, c2)

        pygame.draw.rect(pantalla, COLOR_PANEL,
                         (PANEL_X, 0, ANCHO - PANEL_X, ALTO))
        pygame.draw.line(pantalla, COLOR_SEPARADOR,
                         (PANEL_X, 0), (PANEL_X, ALTO), 2)
        dibujar_panel(pantalla, fuentes, base, P, c1, c2, angulo_base)

        pygame.display.flip()


if __name__ == "__main__":
    main()