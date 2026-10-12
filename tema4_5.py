import pygame
import sys
import math
from src.algebra.vector import Vector

# ==================================================
# CONFIGURACION
# ==================================================
ANCHO, ALTO = 1100, 700
PANEL_X = 800
FPS = 60

VELOCIDAD = 2.0
ESCALA_MUNDO = 70.0
LARGO_EJES = 5.0

RADIO_HITBOX_A = 1.5
RADIO_HITBOX_B = 0.6

LIMITE_MUNDO = 5.5

PARED_X = 3.0
PLATAFORMA_Y = -3.0
GROSOR_COLISION = 0.3

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

COLOR_ORIGEN = (255, 255, 255)
COLOR_P_A = (255, 100, 100)
COLOR_P_B = (100, 200, 255)
COLOR_IMPACTO = (255, 220, 100)

COLOR_PARED = (140, 140, 180)
COLOR_PLATAFORMA = (100, 150, 200)
COLOR_NORMAL = (255, 220, 100)

COLOR_VEC_D = (255, 255, 255)

COLOR_RECTA_DIR_PARED = (100, 100, 140)
COLOR_RECTA_NOR_PARED = (140, 120, 70)
COLOR_RECTA_DIR_PLAT = (70, 100, 140)
COLOR_RECTA_NOR_PLAT = (140, 120, 70)

# ==================================================
# ORIGEN DEL MUNDO
# ==================================================
ORIGEN_MUNDO = Vector(PANEL_X / 2, ALTO / 2)


def a_pantalla(p):
    return (int(ORIGEN_MUNDO.x + p.x * ESCALA_MUNDO),
            int(ORIGEN_MUNDO.y - p.y * ESCALA_MUNDO))


def clamp(v, minimo, maximo):
    return max(minimo, min(maximo, v))


# ==================================================
# HELPERS
# ==================================================
def texto(pantalla, txt, fuente, color, x, y, salto=18):
    pantalla.blit(fuente.render(txt, True, color), (x, y))
    return y + salto


def sep(pantalla, x, y):
    pygame.draw.line(pantalla, COLOR_SEPARADOR,
                     (x, y), (ANCHO - 12, y), 1)
    return y + 8


def flecha(pantalla, origen, vector, color, grosor=3, radio_punta=5):
    fin = origen + vector
    pygame.draw.line(pantalla, color,
                     a_pantalla(origen), a_pantalla(fin), grosor)
    pygame.draw.circle(pantalla, color, a_pantalla(fin), radio_punta)


def dibujar_ejes(pantalla):
    pygame.draw.line(pantalla, (50, 50, 70),
                     a_pantalla(Vector(-LARGO_EJES, 0)),
                     a_pantalla(Vector(LARGO_EJES, 0)), 1)
    pygame.draw.line(pantalla, (50, 50, 70),
                     a_pantalla(Vector(0, -LARGO_EJES)),
                     a_pantalla(Vector(0, LARGO_EJES)), 1)


def dibujar_recta_pasando_por(pantalla, punto, direccion, color, grosor=1):
    if direccion.magnitud() < 1e-6:
        return
    d = direccion.normalizar()
    L = 8.0
    p1 = punto + d * (-L)
    p2 = punto + d * (L)
    pygame.draw.line(pantalla, color,
                     a_pantalla(p1), a_pantalla(p2), grosor)


# ==================================================
# COLISIONES
# ==================================================
def borde_pared_izquierdo():
    return PARED_X - GROSOR_COLISION / 2.0


def borde_plataforma_superior():
    return PLATAFORMA_Y + GROSOR_COLISION / 2.0


def resolver_colision_hitbox(pos, otro, radio, radio_otro):
    diff = pos - otro
    dist = diff.magnitud()
    dist_min = radio + radio_otro
    if dist < dist_min:
        if dist < 1e-6:
            return otro + Vector(dist_min, 0), True, Vector(1, 0)
        d = diff.normalizar()
        return otro + d * dist_min, True, d
    return pos, False, None


def resolver_colision_pared(pos, radio):
    limite = borde_pared_izquierdo() - radio
    if pos.x > limite:
        return Vector(limite, pos.y), True, Vector(-1, 0)
    return pos, False, None


def resolver_colision_plataforma(pos, radio):
    limite = borde_plataforma_superior() + radio
    if pos.y < limite:
        return Vector(pos.x, limite), True, Vector(0, 1)
    return pos, False, None


def resolver_colisiones(pos, radio, otro, radio_otro):
    contacto = None

    pos, col, d = resolver_colision_hitbox(pos, otro, radio, radio_otro)
    if col:
        punto_contacto = otro + d * radio_otro
        contacto = (punto_contacto, d, "hitbox")

    pos, col, d = resolver_colision_pared(pos, radio)
    if col and contacto is None:
        punto_contacto = Vector(borde_pared_izquierdo(), pos.y)
        contacto = (punto_contacto, d, "pared")

    pos, col, d = resolver_colision_plataforma(pos, radio)
    if col and contacto is None:
        punto_contacto = Vector(pos.x, borde_plataforma_superior())
        contacto = (punto_contacto, d, "plataforma")

    return pos, contacto


# ==================================================
# DIBUJO DEL AREA DE JUEGO
# ==================================================
def dibujar_area(pantalla, p_A, p_B, contacto_A, contacto_B):
    o = Vector(0, 0)
    dibujar_ejes(pantalla)

    dir_pared = Vector(0, 1)
    normal_pared = Vector(-1, 0)
    dir_plat = Vector(1, 0)
    normal_plat = Vector(0, 1)

    dibujar_recta_pasando_por(pantalla, o, dir_pared,
                              COLOR_RECTA_DIR_PARED, 1)
    dibujar_recta_pasando_por(pantalla, o, normal_pared,
                              COLOR_RECTA_NOR_PARED, 1)
    dibujar_recta_pasando_por(pantalla, o, dir_plat,
                              COLOR_RECTA_DIR_PLAT, 1)
    dibujar_recta_pasando_por(pantalla, o, normal_plat,
                              COLOR_RECTA_NOR_PLAT, 1)

    # PARED
    ancho_par_px = max(2, int(GROSOR_COLISION * ESCALA_MUNDO))
    x_par_centro_px = ORIGEN_MUNDO.x + PARED_X * ESCALA_MUNDO
    pygame.draw.rect(pantalla, COLOR_PARED,
                     (int(x_par_centro_px - ancho_par_px / 2),
                      int(ORIGEN_MUNDO.y - 4.0 * ESCALA_MUNDO),
                      ancho_par_px,
                      int(8.0 * ESCALA_MUNDO)))

    # PLATAFORMA
    alto_plat_px = max(2, int(GROSOR_COLISION * ESCALA_MUNDO))
    y_plat_centro_px = ORIGEN_MUNDO.y - PLATAFORMA_Y * ESCALA_MUNDO
    pygame.draw.rect(pantalla, COLOR_PLATAFORMA,
                     (int(ORIGEN_MUNDO.x - 4.0 * ESCALA_MUNDO),
                      int(y_plat_centro_px - alto_plat_px / 2),
                      int(8.0 * ESCALA_MUNDO),
                      alto_plat_px))

    # HITBOXES
    pygame.draw.circle(pantalla, COLOR_P_A,
                       a_pantalla(p_A),
                       int(RADIO_HITBOX_A * ESCALA_MUNDO), 2)
    pygame.draw.circle(pantalla, COLOR_P_B,
                       a_pantalla(p_B),
                       int(RADIO_HITBOX_B * ESCALA_MUNDO), 2)

    # Vector d
    flecha(pantalla, p_B, p_A - p_B, COLOR_VEC_D, 2, 4)

    # Puntos
    pygame.draw.circle(pantalla, COLOR_P_A, a_pantalla(p_A), 6)
    pygame.draw.circle(pantalla, (255, 255, 255), a_pantalla(p_A), 6, 2)
    pygame.draw.circle(pantalla, COLOR_P_B, a_pantalla(p_B), 6)
    pygame.draw.circle(pantalla, (30, 30, 30), a_pantalla(p_B), 6, 2)
    pygame.draw.circle(pantalla, COLOR_ORIGEN, a_pantalla(o), 5)

    # Etiquetas
    f_et = pygame.font.SysFont("Arial", 14, bold=True)
    px, py = a_pantalla(p_A)
    pantalla.blit(f_et.render("p_A", True, COLOR_P_A), (px + 10, py + 8))
    px, py = a_pantalla(p_B)
    pantalla.blit(f_et.render("p_B", True, COLOR_P_B), (px + 12, py - 20))

    # Normal solo en contacto
    for contacto in (contacto_A, contacto_B):
        if contacto is not None:
            punto, normal, _ = contacto
            dibujar_recta_pasando_por(pantalla, punto, normal,
                                      COLOR_NORMAL, 2)
            pygame.draw.circle(pantalla, COLOR_IMPACTO,
                               a_pantalla(punto), 5)

    # Cartel impacto
    d = p_A - p_B
    impacto = d.magnitud() <= RADIO_HITBOX_A + RADIO_HITBOX_B
    if impacto:
        f_big = pygame.font.SysFont("Arial", 24, bold=True)
        sup = f_big.render("IMPACTO!", True, COLOR_IMPACTO)
        pygame.draw.rect(pantalla, (60, 50, 10),
                         (30, 30, sup.get_width() + 20, 40))
        pygame.draw.rect(pantalla, COLOR_IMPACTO,
                         (30, 30, sup.get_width() + 20, 40), 2)
        pantalla.blit(sup, (40, 36))


# ==================================================
# PANEL
# ==================================================
def dibujar_panel(pantalla, fuentes, p_A, p_B, contacto_A, contacto_B):
    f_tit, f_txt = fuentes
    x = PANEL_X + 15
    y = 10

    # ==================================================
    # TITULO
    # ==================================================
    y = texto(pantalla, "TEMA 4 + 5: PRODUCTO INTERNO",
              f_tit, COLOR_MODO, x, y, 22)
    y = texto(pantalla, "  <u, v> = u.x*v.x + u.y*v.y",
              f_txt, COLOR_TEORIA, x, y, 15)
    y = sep(pantalla, x, y + 4)

    # ==================================================
    # FORMULA DE LA PLATAFORMA
    # ==================================================
    y = texto(pantalla, "FORMULA DE LA PLATAFORMA:",
              f_tit, COLOR_TITULO, x, y, 17)

    y = texto(pantalla,
              "  punto(t) = origen + t * dir",
              f_txt, COLOR_MODO, x, y, 15)
    y = texto(pantalla,
              "  con  0 <= t <= longitud",
              f_txt, COLOR_TEORIA, x, y, 14)
    y = texto(pantalla,
              "  dir = direccion normalizada",
              f_txt, COLOR_TEORIA, x, y, 14)
    y = texto(pantalla,
              "  normal = perpendicular a dir",
              f_txt, COLOR_TEORIA, x, y, 14)

    y += 4
    y = texto(pantalla, "  Plat. horizontal (y = -3):",
              f_txt, COLOR_PLATAFORMA, x, y, 14)
    y = texto(pantalla,
              f"    origen = (-4.0, {PLATAFORMA_Y:.1f})",
              f_txt, COLOR_TEXTO_DIM, x, y, 13)
    y = texto(pantalla,
              "    dir    = (1.0, 0.0)",
              f_txt, COLOR_TEXTO_DIM, x, y, 13)
    y = texto(pantalla,
              "    long.  = 8.0",
              f_txt, COLOR_TEXTO_DIM, x, y, 13)

    y += 2
    y = texto(pantalla, "  Pared vertical (x = 3):",
              f_txt, COLOR_PARED, x, y, 14)
    y = texto(pantalla,
              f"    origen = ({PARED_X:.1f}, -4.0)",
              f_txt, COLOR_TEXTO_DIM, x, y, 13)
    y = texto(pantalla,
              "    dir    = (0.0, 1.0)",
              f_txt, COLOR_TEXTO_DIM, x, y, 13)
    y = texto(pantalla,
              "    long.  = 8.0",
              f_txt, COLOR_TEXTO_DIM, x, y, 13)

    y = sep(pantalla, x, y + 6)

    # ==================================================
    # APLICACION 1: HITBOX
    # ==================================================
    y = texto(pantalla, "[1] HITBOX (colision circulo)",
              f_tit, COLOR_TITULO, x, y, 17)
    y = texto(pantalla, "    Se calcula <d, d> para ||d||",
              f_txt, COLOR_TEORIA, x, y, 14)

    d = p_A - p_B
    dd = d.x * d.x + d.y * d.y
    dist = d.magnitud()
    r_suma = RADIO_HITBOX_A + RADIO_HITBOX_B
    impacto = dist <= r_suma

    y += 4
    y = texto(pantalla, f"  d = p_A - p_B = ({d.x:6.2f}, {d.y:6.2f})",
              f_txt, COLOR_TEXTO, x, y, 15)
    y = texto(pantalla,
              f"  <d, d> = ({d.x:.1f})^2 + ({d.y:.1f})^2 = {dd:.3f}",
              f_txt, COLOR_MODO, x, y, 15)
    y = texto(pantalla, f"  ||d||  = sqrt({dd:.3f}) = {dist:.3f}",
              f_txt, COLOR_TEXTO, x, y, 15)
    y = texto(pantalla, f"  rA+rB  = {r_suma:.3f}",
              f_txt, COLOR_TITULO, x, y, 15)

    if impacto:
        y = texto(pantalla, "  => IMPACTO (||d|| <= rA+rB)",
                  f_txt, COLOR_OK, x, y, 16)
    else:
        y = texto(pantalla, "  => SIN IMPACTO (||d|| > rA+rB)",
                  f_txt, COLOR_ERROR, x, y, 16)

    y = sep(pantalla, x, y + 4)

    # ==================================================
    # APLICACION 2: ORTOGONALIDAD
    # ==================================================
    y = texto(pantalla, "[2] ORTOGONALIDAD (superficies)",
              f_tit, COLOR_TITULO, x, y, 17)
    y = texto(pantalla, "    Se calcula <dir, normal> = 0",
              f_txt, COLOR_TEORIA, x, y, 14)

    # Pared
    dir_par = Vector(0, 1)
    nor_par = Vector(-1, 0)
    pip = dir_par.x * nor_par.x + dir_par.y * nor_par.y

    y += 4
    y = texto(pantalla, "  PARED (x = 3):",
              f_txt, COLOR_PARED, x, y, 15)
    y = texto(pantalla,
              f"    <dir, n> = {dir_par.x:.1f}*{nor_par.x:.1f} + "
              f"{dir_par.y:.1f}*{nor_par.y:.1f} = {pip:.2f}",
              f_txt, COLOR_MODO, x, y, 13)
    y = texto(pantalla, "    => perpendiculares (producto = 0)",
              f_txt, COLOR_OK, x, y, 13)

    # Plataforma
    dir_pl = Vector(1, 0)
    nor_pl = Vector(0, 1)
    pipl = dir_pl.x * nor_pl.x + dir_pl.y * nor_pl.y

    y += 4
    y = texto(pantalla, "  PLATAFORMA (y = -3):",
              f_txt, COLOR_PLATAFORMA, x, y, 15)
    y = texto(pantalla,
              f"    <dir, n> = {dir_pl.x:.1f}*{nor_pl.x:.1f} + "
              f"{dir_pl.y:.1f}*{nor_pl.y:.1f} = {pipl:.2f}",
              f_txt, COLOR_MODO, x, y, 13)
    y = texto(pantalla, "    => perpendiculares (producto = 0)",
              f_txt, COLOR_OK, x, y, 13)

    y = sep(pantalla, x, y + 6)

    # ==================================================
    # ESTADO ACTUAL
    # ==================================================
    y = texto(pantalla, "ESTADO ACTUAL:", f_tit, COLOR_TITULO, x, y, 16)

    c_a = COLOR_P_A if contacto_A else COLOR_TEXTO_DIM
    c_b = COLOR_P_B if contacto_B else COLOR_TEXTO_DIM
    tipo_a = contacto_A[2] if contacto_A else "ninguno"
    tipo_b = contacto_B[2] if contacto_B else "ninguno"

    y = texto(pantalla, f"  p_A toca: {tipo_a}",
              f_txt, c_a, x, y, 14)
    y = texto(pantalla, f"  p_B toca: {tipo_b}",
              f_txt, c_b, x, y, 14)

    if contacto_A or contacto_B:
        y = texto(pantalla, "  (normal dibujada en amarillo)",
                  f_txt, COLOR_NORMAL, x, y, 13)




# ==================================================
# MAIN
# ==================================================
def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Tema 4 + 5: producto interno y ortogonalidad")
    reloj = pygame.time.Clock()

    f_tit = pygame.font.SysFont("Arial", 16, bold=True)
    f_txt = pygame.font.SysFont("Arial", 13)
    fuentes = (f_tit, f_txt)

    p_A = Vector(0.0, 0.0)
    p_B = Vector(4.0, 2.0)

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
                    p_A = Vector(0.0, 0.0)
                    p_B = Vector(4.0, 2.0)

        # Mover p_B con WASD
        vel_pB = Vector(0, 0)
        if teclas[pygame.K_a]: vel_pB.x -= 1
        if teclas[pygame.K_d]: vel_pB.x += 1
        if teclas[pygame.K_w]: vel_pB.y += 1
        if teclas[pygame.K_s]: vel_pB.y -= 1
        p_B = p_B + vel_pB * (VELOCIDAD * dt)

        # Mover p_A con flechas
        vel_pA = Vector(0, 0)
        if teclas[pygame.K_LEFT]:  vel_pA.x -= 1
        if teclas[pygame.K_RIGHT]: vel_pA.x += 1
        if teclas[pygame.K_UP]:    vel_pA.y += 1
        if teclas[pygame.K_DOWN]:  vel_pA.y -= 1
        p_A = p_A + vel_pA * (VELOCIDAD * dt)

        # Bounds
        p_A.x = clamp(p_A.x, -LIMITE_MUNDO, LIMITE_MUNDO)
        p_A.y = clamp(p_A.y, -LIMITE_MUNDO, LIMITE_MUNDO)
        p_B.x = clamp(p_B.x, -LIMITE_MUNDO, LIMITE_MUNDO)
        p_B.y = clamp(p_B.y, -LIMITE_MUNDO, LIMITE_MUNDO)

        # Colisiones
        p_A, contacto_A = resolver_colisiones(p_A, RADIO_HITBOX_A,
                                              p_B, RADIO_HITBOX_B)
        p_B, contacto_B = resolver_colisiones(p_B, RADIO_HITBOX_B,
                                              p_A, RADIO_HITBOX_A)

        # Dibujar
        pantalla.fill(COLOR_FONDO)
        dibujar_area(pantalla, p_A, p_B, contacto_A, contacto_B)

        pygame.draw.rect(pantalla, COLOR_PANEL,
                         (PANEL_X, 0, ANCHO - PANEL_X, ALTO))
        pygame.draw.line(pantalla, COLOR_SEPARADOR,
                         (PANEL_X, 0), (PANEL_X, ALTO), 2)
        dibujar_panel(pantalla, fuentes, p_A, p_B,
                      contacto_A, contacto_B)

        pygame.display.flip()


if __name__ == "__main__":
    main()