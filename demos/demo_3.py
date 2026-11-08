# demos/demo_3.py
import pygame
from src.algebra.vector import Vector
from src.render import graficos as G
from src.entidades.plataforma import Plataforma

from src.render.graficos import ANCHO, ALTO, ESCALA, FPS, ESCALA_GLOBAL
from variables import DEMO_3_PANEL_BASE

PANEL_X = int(DEMO_3_PANEL_BASE * ESCALA_GLOBAL)

# Pared más larga y casi horizontal (solo 22° de inclinación)
PARED = Plataforma(Vector(-5.0, -3.0), Vector(1.0, 0.4), longitud=10.5, grosor=0.2)
NORMAL = PARED.normal().normalizar()

# Constantes de control reducidas (vectores más cortos)
ACELERACION = 3.0    # antes 8.0 → ahora la flecha crece lento
FRICCION = 0.94
VEL_MAX = 2.2        # antes 6.0 → ahora la flecha nunca es enorme

# ==================================================
# DIBUJO DEL PLANO
# ==================================================
def dibujar_area(pantalla, pos, vel, c_proy, c_orto, colisionando):
    G.ejes(pantalla)

    # Pared
    p1 = G.a_pantalla(PARED.origen)
    p2 = G.a_pantalla(PARED.extremo_final())
    pygame.draw.line(pantalla, G.COLOR_09, p1, p2, int(PARED.grosor * ESCALA) + 2)

    # Normal desde el centro de la pared
    centro_pared = PARED.origen + PARED.direccion * (PARED.longitud / 2)
    G.flecha(pantalla, centro_pared, NORMAL * 1.5, G.COLOR_12, 2, 4)

    # Objeto (círculo)
    px, py = G.a_pantalla(pos)
    pygame.draw.circle(pantalla, G.COLOR_08, (px, py), int(0.4 * ESCALA))
    pygame.draw.circle(pantalla, G.COLOR_15, (px, py), int(0.4 * ESCALA), 2)

    # Vector velocidad
    G.flecha(pantalla, pos, vel, G.COLOR_15, 3, 5)

    # Descomposición (si hay velocidad suficiente)
    if vel.magnitud() > 0.1:
        G.flecha(pantalla, pos, c_proy, G.COLOR_11, 2, 4)
        G.flecha(pantalla, pos, c_orto, G.COLOR_16, 2, 4)

        G.linea_discontinua(pantalla, pos + c_proy, pos + vel, G.COLOR_10, 6, 4)
        G.linea_discontinua(pantalla, pos + c_orto, pos + vel, G.COLOR_10, 6, 4)

        f_et = G.fuente(14, bold=True)
        pantalla.blit(f_et.render("v", True, G.COLOR_15), (px + int(10*ESCALA_GLOBAL), py - int(15*ESCALA_GLOBAL)))
        pantalla.blit(f_et.render("Proy", True, G.COLOR_11), (px + int(5*ESCALA_GLOBAL), py + int(5*ESCALA_GLOBAL)))
        pantalla.blit(f_et.render("v_orto", True, G.COLOR_16), (px - int(30*ESCALA_GLOBAL), py + int(10*ESCALA_GLOBAL)))

    # Indicador de colisión
    if colisionando:
        f_col = G.fuente(18, bold=True)
        sup = f_col.render("¡COLISIÓN!", True, G.COLOR_19)
        pantalla.blit(sup, (int(20*ESCALA_GLOBAL), int(20*ESCALA_GLOBAL)))

# ==================================================
# PANEL (TEMA 4 + 5) - SIEMPRE VISIBLE
# ==================================================
def dibujar_panel(pantalla, fuentes, vel, c_proy, c_orto, colisionando):
    f_tit, f_txt = fuentes
    x = PANEL_X + int(15 * ESCALA_GLOBAL)
    y = int(10 * ESCALA_GLOBAL)
    x_fin = ANCHO - int(12 * ESCALA_GLOBAL)

    y = G.texto(pantalla, "TEMA 4 + 5: PRODUCTO INTERNO", f_tit, G.COLOR_13, x, y, 22)
    y = G.sep(pantalla, x, y + int(4*ESCALA_GLOBAL), x_fin)

    # --- Vectores ---
    y = G.texto(pantalla, f"  v = ({vel.x:6.2f}, {vel.y:6.2f})", f_txt, G.COLOR_15, x, y, 15)
    y = G.texto(pantalla, f"  n = ({NORMAL.x:6.2f}, {NORMAL.y:6.2f})", f_txt, G.COLOR_12, x, y, 15)
    y = G.texto(pantalla, f"  ||v|| = {vel.magnitud():5.2f}", f_txt, G.COLOR_09, x, y, 14)

    y = G.sep(pantalla, x, y + int(4*ESCALA_GLOBAL), x_fin)

    # --- Producto interno ---
    dot = vel.producto_punto(NORMAL)
    y = G.texto(pantalla, "Producto Interno:", f_tit, G.COLOR_11, x, y, 15)
    y = G.texto(pantalla, f"  <v, n> = {dot:7.3f}", f_txt, G.COLOR_10, x, y, 14)

    y = G.sep(pantalla, x, y + int(4*ESCALA_GLOBAL), x_fin)

    # --- Proyección ---
    y = G.texto(pantalla, "Proyección sobre n:", f_tit, G.COLOR_11, x, y, 15)
    y = G.texto(pantalla, "  Proy_n(v) = <v,n> * n", f_txt, G.COLOR_10, x, y, 13)
    y = G.texto(pantalla, f"  Proy_n(v) = ({c_proy.x:6.2f}, {c_proy.y:6.2f})", f_txt, G.COLOR_11, x, y, 14)

    y = G.sep(pantalla, x, y + int(4*ESCALA_GLOBAL), x_fin)

    # --- Componente ortogonal ---
    y = G.texto(pantalla, "Componente ortogonal:", f_tit, G.COLOR_16, x, y, 15)
    y = G.texto(pantalla, "  v_orto = v - Proy_n(v)", f_txt, G.COLOR_10, x, y, 13)
    y = G.texto(pantalla, f"  v_orto = ({c_orto.x:6.2f}, {c_orto.y:6.2f})", f_txt, G.COLOR_16, x, y, 14)

    y = G.sep(pantalla, x, y + int(4*ESCALA_GLOBAL), x_fin)

    # --- Verificación ortogonalidad ---
    prueba = c_proy.producto_punto(c_orto)
    y = G.texto(pantalla, "Verificación ortogonalidad:", f_tit, G.COLOR_11, x, y, 15)
    y = G.texto(pantalla, "  <Proy_n(v), v_orto> = 0", f_txt, G.COLOR_10, x, y, 13)
    y = G.texto(pantalla, f"  Resultado = {prueba:10.6f}", f_txt, G.COLOR_08, x, y, 14)

    y = G.sep(pantalla, x, y + int(4*ESCALA_GLOBAL), x_fin)

    # --- Estado ---
    if colisionando:
        y = G.texto(pantalla, "¡COLISIÓN DETECTADA!", f_tit, G.COLOR_19, x, y, 18)
        y = G.texto(pantalla, "Nueva velocidad = v_orto", f_tit, G.COLOR_16, x, y, 15)
    else:
        y = G.texto(pantalla, "En movimiento libre", f_txt, G.COLOR_09, x, y, 14)

    y = G.sep(pantalla, x, y + int(4*ESCALA_GLOBAL), x_fin)

    # --- Controles ---
    y = G.texto(pantalla, "Controles:", f_tit, G.COLOR_11, x, y, 15)
    y = G.texto(pantalla, "  WASD  empujar pelota", f_txt, G.COLOR_09, x, y, 13)
    y = G.texto(pantalla, "  R     resetear", f_txt, G.COLOR_09, x, y, 13)
    y = G.texto(pantalla, "  ESC   salir", f_txt, G.COLOR_09, x, y, 13)

# ==================================================
# MAIN
# ==================================================
def main():
    win = G.Ventana("Tema 4 + 5: Proyección y Colisión", ANCHO, ALTO, PANEL_X, ESCALA, FPS)

    # Estado inicial: pelota cerca de la plataforma
    pos = Vector(0.0, 2.0)
    vel = Vector(0.0, 0.0)

    while True:
        dt, teclas, eventos = win.empezar_frame()

        # Reiniciar con R
        for e in eventos:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_r:
                pos = Vector(0.0, 2.0)
                vel = Vector(0.0, 0.0)

        # --- CONTROL CON WASD (aceleración suave) ---
        ax = (teclas[pygame.K_d] - teclas[pygame.K_a]) * ACELERACION
        ay = (teclas[pygame.K_w] - teclas[pygame.K_s]) * ACELERACION

        if ax != 0 or ay != 0:
            vel = vel + Vector(ax, ay) * dt
            if vel.magnitud() > VEL_MAX:
                vel = vel.normalizar() * VEL_MAX
        else:
            # Fricción cuando no se presiona nada
            vel = vel * FRICCION
            if vel.magnitud() < 0.05:
                vel = Vector(0.0, 0.0)

        # Mover
        pos = pos + vel * dt

        # Límites de pantalla (rebote suave)
        if pos.x < -5.5: pos.x = -5.5; vel.x *= -0.5
        if pos.x > 5.5: pos.x = 5.5; vel.x *= -0.5
        if pos.y < -5.0: pos.y = -5.0; vel.y *= -0.5
        if pos.y > 5.0: pos.y = 5.0; vel.y *= -0.5

        # --- Calcular descomposición (SIEMPRE para el panel) ---
        dot = vel.producto_punto(NORMAL)
        c_proy = NORMAL * dot
        c_orto = vel - c_proy

        # --- Detección de colisión con la pared ---
        proy_punto = PARED.punto_mas_cercano(pos)
        diff = pos - proy_punto
        dist = diff.magnitud()

        colisionando = dist <= 0.4

        if colisionando:
            # Empujar hacia afuera usando la dirección real desde la pared
            if dist < 1e-6:
                d = NORMAL
            else:
                d = diff.normalizar()
            pos = pos + d * (0.4 - dist)

            # Dibujar primero con la descomposición original
            win.limpiar()
            dibujar_area(win.pantalla, pos, vel, c_proy, c_orto, True)
            win.dibujar_panel_fondo()
            dibujar_panel(win.pantalla, win.fuentes, vel, c_proy, c_orto, True)
            win.terminar_frame()

            # Luego anular la componente perpendicular
            vel = c_orto
            continue

        # Sin colisión
        win.limpiar()
        dibujar_area(win.pantalla, pos, vel, c_proy, c_orto, False)
        win.dibujar_panel_fondo()
        dibujar_panel(win.pantalla, win.fuentes, vel, c_proy, c_orto, False)
        win.terminar_frame()

if __name__ == "__main__":
    main()