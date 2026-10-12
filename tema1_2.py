import pygame
import sys
import math
from src.algebra.vector import Vector

# ==================================================
# CONFIGURACION
# ==================================================
ANCHO, ALTO = 1250, 700
PANEL_X = 1000
FPS = 60

VELOCIDAD = 2.0
ESCALA_MUNDO = 70.0
LARGO_RECTA = 18.0    # recta muy larga (cruza toda la pantalla)

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
COLOR_ESCALAR_TXT = (255, 220, 150)

COLOR_U = (255, 100, 100)
COLOR_V = (100, 255, 100)
COLOR_Z = (100, 200, 255)
COLOR_Z_EN_W = (100, 255, 100)
COLOR_SUMA = (255, 220, 100)
COLOR_ESCALAR = (100, 180, 255)
COLOR_ESCALAR_8 = (150, 220, 255)
COLOR_INVERSO = (180, 100, 255)
COLOR_DOBLE = (255, 100, 200)
COLOR_NARANJA = (255, 180, 100)
COLOR_AXIOMA_3 = (255, 200, 100)

COLOR_PARALELO = (90, 90, 120)
COLOR_PARALELO2 = (130, 70, 110)

COLOR_RECTA = (100, 200, 255)
COLOR_RECTA_AFIN = (120, 120, 150)
COLOR_ORIGEN = (255, 255, 255)

C_ESCALAR = 1.5
D_ESCALAR = 2.0

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


def dibujar_recta_infinita(pantalla, direccion, color, grosor=2):
    d = direccion.normalizar()
    p1 = d * (-LARGO_RECTA)
    p2 = d * (LARGO_RECTA)
    pygame.draw.line(pantalla, color,
                     a_pantalla(p1), a_pantalla(p2), grosor)


def dibujar_recta_por_punto(pantalla, punto, direccion, color, grosor=1):
    d = direccion.normalizar()
    p1 = punto + d * (-LARGO_RECTA)
    p2 = punto + d * (LARGO_RECTA)
    pygame.draw.line(pantalla, color,
                     a_pantalla(p1), a_pantalla(p2), grosor)


def determinante(u, v):
    return u.x * v.y - u.y * v.x


# ==================================================
# DIBUJO DEL AREA DE JUEGO
# ==================================================
def dibujar_area(pantalla, u, v, z, en_w):
    o = Vector(0, 0)
    c = C_ESCALAR
    d = D_ESCALAR

    dibujar_ejes(pantalla)

    # Recta contraejemplo (afin)
    dibujar_recta_por_punto(pantalla, Vector(0, 1), Vector(1, 1),
                            COLOR_RECTA_AFIN, 1)

    # Recta W
    dibujar_recta_infinita(pantalla, v, COLOR_RECTA, 2)

    # Paralelogramo u, v
    suma = u + v
    pygame.draw.line(pantalla, COLOR_PARALELO,
                     a_pantalla(v), a_pantalla(suma), 1)
    pygame.draw.line(pantalla, COLOR_PARALELO,
                     a_pantalla(u), a_pantalla(suma), 1)

    # Paralelogramo escalado
    u_c = u * c
    v_c = v * c
    suma_c = u_c + v_c
    pygame.draw.line(pantalla, COLOR_PARALELO2,
                     a_pantalla(v_c), a_pantalla(suma_c), 1)
    pygame.draw.line(pantalla, COLOR_PARALELO2,
                     a_pantalla(u_c), a_pantalla(suma_c), 1)

    # Linea de u
    u_cd = u * (c * d)
    pygame.draw.line(pantalla, (55, 55, 80),
                     a_pantalla(u * (-0.5)),
                     a_pantalla(u_cd + u * 0.5), 1)

    # Lineas discontinuas axioma 3
    suma_z = suma + z
    linea_discontinua(pantalla,
                      a_pantalla(suma), a_pantalla(suma_z),
                      COLOR_AXIOMA_3)
    linea_discontinua(pantalla,
                      a_pantalla(z), a_pantalla(suma_z),
                      COLOR_AXIOMA_3)

    # --- Flechas ---
    flecha(pantalla, o, u, COLOR_U, 4, 6)
    flecha(pantalla, o, v, COLOR_V, 4, 6)

    color_z = COLOR_Z_EN_W if en_w else COLOR_Z
    flecha(pantalla, o, z, color_z, 4, 6)

    flecha(pantalla, o, suma, COLOR_SUMA, 2, 4)
    flecha(pantalla, o, u_c, COLOR_ESCALAR, 2, 4)
    flecha(pantalla, o, u * (c + d), COLOR_ESCALAR_8, 2, 4)
    flecha(pantalla, o, u * (-1), COLOR_INVERSO, 2, 4)
    flecha(pantalla, o, suma_c, COLOR_DOBLE, 2, 4)
    flecha(pantalla, o, u_cd, COLOR_NARANJA, 2, 4)
    flecha(pantalla, o, suma_z, COLOR_AXIOMA_3, 2, 4)

    pygame.draw.circle(pantalla, COLOR_ORIGEN, a_pantalla(o), 6)

    # --- Etiquetas ---
    f_et = pygame.font.SysFont("Arial", 14, bold=True)

    def etiq(txt, vec, color, dx=10, dy=-14):
        px, py = a_pantalla(vec)
        pantalla.blit(f_et.render(txt, True, color),
                      (px + dx, py + dy))

    etiq("u", u, COLOR_U)
    etiq("v", v, COLOR_V)
    etiq("z", z, color_z)
    etiq("1,2", suma, COLOR_SUMA)
    etiq("3", suma_z, COLOR_AXIOMA_3)
    etiq("6", u_c, COLOR_ESCALAR)
    etiq("8", u * (c + d), COLOR_ESCALAR_8)
    etiq("5", u * (-1), COLOR_INVERSO)
    etiq("7", suma_c, COLOR_DOBLE)
    etiq("9", u_cd, COLOR_NARANJA)

    # Etiqueta recta contraejemplo
    f_afin = pygame.font.SysFont("Arial", 13, bold=True)
    px, py = a_pantalla(Vector(2.5, 3.5))
    sup = f_afin.render("y = x + 1  (afin, NO subespacio)",
                        True, COLOR_RECTA_AFIN)
    pantalla.blit(sup, (px, py))

    # Indicador grande si z esta en W
    if en_w:
        f_big = pygame.font.SysFont("Arial", 22, bold=True)
        sup = f_big.render("z PERTENECE a W  (subespacio)", True, COLOR_OK)
        pantalla.blit(sup, (30, 30))


# ==================================================
# PANEL
# ==================================================
def dibujar_panel(pantalla, fuentes, u, v, z, en_w):
    f_tit, f_txt = fuentes
    x = PANEL_X + 15
    y = 8

    # Vectores
    y = texto(pantalla,
              f"u = ({u.x:5.2f},{u.y:5.2f})   "
              f"v = ({v.x:5.2f},{v.y:5.2f})",
              f_txt, COLOR_TEXTO, x, y, 16)
    y = texto(pantalla,
              f"z = ({z.x:5.2f},{z.y:5.2f})   "
              f"c = {C_ESCALAR}   d = {D_ESCALAR}",
              f_txt, COLOR_ESCALAR_TXT, x, y, 16)

    y = sep(pantalla, x, y + 4)

    # ==================================================
    # TEMA 1
    # ==================================================
    y = texto(pantalla, "TEMA 1: Espacio vectorial",
              f_tit, COLOR_MODO, x, y, 20)

    c = C_ESCALAR
    d = D_ESCALAR
    cero = Vector(0, 0)
    suma = u + v
    suma_inv = v + u
    neutro_a = u + cero
    inverso_a = u + (u * (-1))
    doble_u = u * c
    dist1_izq = (u + v) * c
    dist1_der = u * c + v * c
    dist2_izq = u * (c + d)
    dist2_der = u * c + u * d
    asoc_izq = u * (c * d)
    asoc_der = (u * c) * d
    neutro_e = u * 1
    asoc_suma_izq = (u + v) + z
    asoc_suma_der = u + (v + z)

    axiomas = [
        ("1", "Cerradura +",
         "u + v  pertenece a  V",
         f"({suma.x:.2f},{suma.y:.2f})  OK", COLOR_SUMA),
        ("2", "Conmutativa",
         "u + v = v + u",
         f"({suma.x:.2f},{suma.y:.2f}) = "
         f"({suma_inv.x:.2f},{suma_inv.y:.2f})",
         COLOR_SUMA),
        ("3", "Asociativa +",
         "(u+v)+z = u+(v+z)",
         f"({asoc_suma_izq.x:.2f},{asoc_suma_izq.y:.2f}) = "
         f"({asoc_suma_der.x:.2f},{asoc_suma_der.y:.2f})",
         COLOR_AXIOMA_3),
        ("4", "Neutro +",
         "u + 0 = u",
         f"({neutro_a.x:.2f},{neutro_a.y:.2f}) = "
         f"({u.x:.2f},{u.y:.2f})",
         COLOR_U),
        ("5", "Inverso +",
         "u + (-u) = 0",
         f"({inverso_a.x:.2f},{inverso_a.y:.2f}) = (0.00,0.00)",
         COLOR_INVERSO),
        ("6", "Cerradura *",
         "c * u  pertenece a  V",
         f"({doble_u.x:.2f},{doble_u.y:.2f})  OK",
         COLOR_ESCALAR),
        ("7", "Distributiva 1",
         "c*(u+v) = c*u + c*v",
         f"({dist1_izq.x:.2f},{dist1_izq.y:.2f}) = "
         f"({dist1_der.x:.2f},{dist1_der.y:.2f})",
         COLOR_DOBLE),
        ("8", "Distributiva 2",
         "(c+d)*u = c*u + d*u",
         f"({dist2_izq.x:.2f},{dist2_izq.y:.2f}) = "
         f"({dist2_der.x:.2f},{dist2_der.y:.2f})",
         COLOR_ESCALAR_8),
        ("9", "Asociativa *",
         "c*(d*u) = (c*d)*u",
         f"({asoc_izq.x:.2f},{asoc_izq.y:.2f}) = "
         f"({asoc_der.x:.2f},{asoc_der.y:.2f})",
         COLOR_NARANJA),
        ("10", "Neutro *",
         "1 * u = u",
         f"({neutro_e.x:.2f},{neutro_e.y:.2f}) = "
         f"({u.x:.2f},{u.y:.2f})",
         COLOR_U),
    ]

    for num, nombre, formula, valor, color in axiomas:
        sup_n = f_txt.render(f"{num:>2}.", True, color)
        pantalla.blit(sup_n, (x, y))
        sup_nom = f_txt.render(nombre, True, color)
        pantalla.blit(sup_nom, (x + 25, y))
        y += 15
        sup_f = f_txt.render(f"     {formula}", True, COLOR_TEORIA)
        pantalla.blit(sup_f, (x, y))
        y += 14
        sup_v = f_txt.render(f"     {valor}", True, COLOR_OK)
        pantalla.blit(sup_v, (x, y))
        y += 21

    y = sep(pantalla, x, y + 4)

    # ==================================================
    # TEMA 2
    # ==================================================
    y = texto(pantalla, "TEMA 2: Subespacio vectorial",
              f_tit, COLOR_MODO, x, y, 20)

    y = texto(pantalla, "W = gen{v} = { t*v : t en R }",
              f_txt, COLOR_RECTA, x, y, 16)
    y = texto(pantalla, "Test:  z en W <=> det(z,v)=0",
              f_txt, COLOR_TEORIA, x, y, 14)
    y = texto(pantalla,
              f"  det(z,v) = {determinante(z, v):6.3f}",
              f_txt, COLOR_TEXTO, x, y, 14)

    if en_w:
        y = texto(pantalla, "  z PERTENECE a W",
                  f_txt, COLOR_OK, x, y, 18)
    else:
        y = texto(pantalla, "  z NO pertenece a W",
                  f_txt, COLOR_ERROR, x, y, 18)


# ==================================================
# MAIN
# ==================================================
def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Tema 1 y 2: espacio + subespacio")
    reloj = pygame.time.Clock()

    f_tit = pygame.font.SysFont("Arial", 15, bold=True)
    f_txt = pygame.font.SysFont("Arial", 13)
    fuentes = (f_tit, f_txt)

    u = Vector(2.0, 1.0)
    v = Vector(1.0, 0.5)
    z = Vector(-1.0, 1.5)

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
                    u = Vector(2.0, 1.0)
                    v = Vector(1.0, 0.5)
                    z = Vector(-1.0, 1.5)

        # Mover u con WASD
        vel_u = Vector(0, 0)
        if teclas[pygame.K_a]:
            vel_u.x -= 1
        if teclas[pygame.K_d]:
            vel_u.x += 1
        if teclas[pygame.K_w]:
            vel_u.y += 1
        if teclas[pygame.K_s]:
            vel_u.y -= 1
        u = u + vel_u * (VELOCIDAD * dt)

        # Mover v con flechas
        vel_v = Vector(0, 0)
        if teclas[pygame.K_LEFT]:
            vel_v.x -= 1
        if teclas[pygame.K_RIGHT]:
            vel_v.x += 1
        if teclas[pygame.K_UP]:
            vel_v.y += 1
        if teclas[pygame.K_DOWN]:
            vel_v.y -= 1
        v = v + vel_v * (VELOCIDAD * dt)

        # Mover z con IJKL
        vel_z = Vector(0, 0)
        if teclas[pygame.K_j]:
            vel_z.x -= 1
        if teclas[pygame.K_l]:
            vel_z.x += 1
        if teclas[pygame.K_i]:
            vel_z.y += 1
        if teclas[pygame.K_k]:
            vel_z.y -= 1
        z = z + vel_z * (VELOCIDAD * dt)

        # Test: z esta en W = gen{v}?
        dz = determinante(z, v)
        en_w = abs(dz) < 0.05

        # --- Dibujar ---
        pantalla.fill(COLOR_FONDO)

        dibujar_area(pantalla, u, v, z, en_w)

        pygame.draw.rect(pantalla, COLOR_PANEL,
                         (PANEL_X, 0, ANCHO - PANEL_X, ALTO))
        pygame.draw.line(pantalla, COLOR_SEPARADOR,
                         (PANEL_X, 0), (PANEL_X, ALTO), 2)
        dibujar_panel(pantalla, fuentes, u, v, z, en_w)

        pygame.display.flip()


if __name__ == "__main__":
    main()