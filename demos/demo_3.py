# demos/demo_3.py
import pygame
from src.algebra.vector import Vector
from src.render import graficos as G
from src.entidades.plataforma import Plataforma

from src.render.graficos import ANCHO, ALTO, ESCALA, FPS, ESCALA_GLOBAL
from variables import DEMO_3_PANEL_BASE

PANEL_X = int(DEMO_3_PANEL_BASE * ESCALA_GLOBAL)

# Pared inclinada (como un terreno en el juego)
PARED = Plataforma(Vector(-4.0, -4.0), Vector(1.0, 1.5), longitud=6.0, grosor=0.2)
NORMAL = PARED.normal().normalizar()

# ==================================================
# DIBUJO DEL PLANO
# ==================================================
def dibujar_area(pantalla, pos, vel, c_proy, c_orto, colisionando):
    G.ejes(pantalla)

    # Dibujamos la pared
    p1 = G.a_pantalla(PARED.origen)
    p2 = G.a_pantalla(PARED.extremo_final())
    pygame.draw.line(pantalla, G.COLOR_09, p1, p2, int(PARED.grosor * ESCALA) + 2)

    # Dibujamos la Normal de la pared desde el centro de la pared
    centro_pared = PARED.origen + PARED.direccion * (PARED.longitud / 2)
    G.flecha(pantalla, centro_pared, NORMAL * 2, G.COLOR_12, 2, 4)

    # Dibujamos el objeto (círculo)
    px, py = G.a_pantalla(pos)
    pygame.draw.circle(pantalla, G.COLOR_08, (px, py), int(0.4 * ESCALA))
    pygame.draw.circle(pantalla, G.COLOR_15, (px, py), int(0.4 * ESCALA), 2)

    # Dibujamos el vector de velocidad (sale del objeto)
    G.flecha(pantalla, pos, vel, G.COLOR_15, 3, 5)

    # Si hay colisión, dibujamos la descomposición en ese punto exacto
    if colisionando:
        # Proyección sobre la normal
        G.flecha(pantalla, pos, c_proy, G.COLOR_11, 2, 4)
        # Componente ortogonal (deslizamiento)
        G.flecha(pantalla, pos, c_orto, G.COLOR_16, 2, 4)
        
        # Líneas punteadas formando el rectángulo
        G.linea_discontinua(pantalla, pos + c_proy, pos + vel, G.COLOR_10, 6, 4)
        G.linea_discontinua(pantalla, pos + c_orto, pos + vel, G.COLOR_10, 6, 4)

        f_et = G.fuente(14, bold=True)
        pantalla.blit(f_et.render("v", True, G.COLOR_15), (px + int(10*ESCALA_GLOBAL), py - int(15*ESCALA_GLOBAL)))
        pantalla.blit(f_et.render("Proy", True, G.COLOR_11), (px + int(5*ESCALA_GLOBAL), py + int(5*ESCALA_GLOBAL)))
        pantalla.blit(f_et.render("v_orto", True, G.COLOR_16), (px - int(30*ESCALA_GLOBAL), py + int(10*ESCALA_GLOBAL)))

# ==================================================
# PANEL (TEMA 4 + 5)
# ==================================================
def dibujar_panel(pantalla, fuentes, vel, c_proy, c_orto, colisionando):
    f_tit, f_txt = fuentes
    x = PANEL_X + int(15 * ESCALA_GLOBAL)
    y = int(10 * ESCALA_GLOBAL)
    x_fin = ANCHO - int(12 * ESCALA_GLOBAL)

    y = G.texto(pantalla, "TEMA 4 + 5: APLICACIÓN EN FÍSICA", f_tit, G.COLOR_13, x, y, 22)
    y = G.sep(pantalla, x, y + int(4*ESCALA_GLOBAL), x_fin)

    y = G.texto(pantalla, f"  v = ({vel.x:5.2f}, {vel.y:5.2f})", f_txt, G.COLOR_15, x, y, 15)
    y = G.texto(pantalla, f"  n = ({NORMAL.x:5.2f}, {NORMAL.y:5.2f})", f_txt, G.COLOR_12, x, y, 15)
    
    y = G.sep(pantalla, x, y + int(4*ESCALA_GLOBAL), x_fin)

    if colisionando:
        y = G.texto(pantalla, "¡COLISIÓN DETECTADA!", f_tit, G.COLOR_19, x, y, 18)
        y += int(4*ESCALA_GLOBAL)
        
        # Proyección
        y = G.texto(pantalla, "Proyección Normal (Empuje):", f_tit, G.COLOR_11, x, y, 15)
        y = G.texto(pantalla, f"  Proy_n(v) = {c_proy.producto_punto(NORMAL):5.2f} * n", f_txt, G.COLOR_10, x, y, 14)
        y = G.texto(pantalla, f"  Proy_n(v) = ({c_proy.x:5.2f}, {c_proy.y:5.2f})", f_txt, G.COLOR_11, x, y, 14)
        
        y = G.sep(pantalla, x, y + int(4*ESCALA_GLOBAL), x_fin)
        
        # Componente Ortogonal
        y = G.texto(pantalla, "Componente Ortogonal (Desliz):", f_tit, G.COLOR_16, x, y, 15)
        y = G.texto(pantalla, "  v_orto = v - Proy_n(v)", f_txt, G.COLOR_10, x, y, 14)
        y = G.texto(pantalla, f"  v_orto = ({c_orto.x:5.2f}, {c_orto.y:5.2f})", f_txt, G.COLOR_16, x, y, 14)

        y = G.sep(pantalla, x, y + int(4*ESCALA_GLOBAL), x_fin)
        
        # Prueba de ortogonalidad
        y = G.texto(pantalla, "Prueba de Ortogonalidad:", f_tit, G.COLOR_11, x, y, 15)
        y = G.texto(pantalla, "  <Proy_n(v), v_orto> = 0", f_txt, G.COLOR_10, x, y, 14)
        y = G.texto(pantalla, f"  Resultado = {c_proy.producto_punto(c_orto):6.4f}", f_txt, G.COLOR_08, x, y, 14)
    else:
        y = G.texto(pantalla, "Objeto en movimiento libre...", f_txt, G.COLOR_09, x, y, 16)
        y = G.texto(pantalla, "Mueve el objeto con WASD", f_txt, G.COLOR_09, x, y, 14)
        y = G.texto(pantalla, "hacia la pared para ver la magia.", f_txt, G.COLOR_09, x, y, 14)

# ==================================================
# MAIN
# ==================================================
def main():
    win = G.Ventana("Tema 4 + 5: Proyección y Colisión", ANCHO, ALTO, PANEL_X, ESCALA, FPS)
    
    # Estado del objeto
    pos = Vector(-3.0, 3.0)
    vel = Vector(2.0, -2.0)

    while True:
        dt, teclas, eventos = win.empezar_frame()
        
        # Input del usuario (mueve la velocidad)
        vx = (teclas[pygame.K_d] - teclas[pygame.K_a]) * 5.0
        vy = (teclas[pygame.K_w] - teclas[pygame.K_s]) * 5.0
        
        # Actualizamos posición
        pos = pos + vel * dt
        
        # Limites de pantalla
        if pos.x < -6: pos.x = -6; vel.x *= -1
        if pos.x > 6: pos.x = 6; vel.x *= -1
        if pos.y < -5: pos.y = -5; vel.y *= -1
        if pos.y > 5: pos.y = 5; vel.y *= -1

        # Reiniciar con R
        for e in eventos:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_r:
                pos = Vector(-3.0, 3.0)
                vel = Vector(2.0, -2.0)

        # --- LÓGICA DE COLISIÓN ---
        # Distancia al punto más cercano de la pared
        dist = PARED.distancia_al_segmento(pos)
        
        colisionando = False
        c_proy = Vector(0, 0)
        c_orto = Vector(0, 0)

        if dist <= 0.4: # Si el radio del objeto toca la pared
            colisionando = True
            
            # Producto interno para la proyección
            dot = vel.producto_punto(NORMAL)
            c_proy = NORMAL * dot          # Componente que empuja la pared
            c_orto = vel - c_proy          # Componente que resbala

            # Simulamos el deslizamiento aplicando la componente ortogonal
            pos = pos + c_orto * dt
            
            # Al tocar la pared, empujamos un poco hacia afuera para que no se atasque
            pos = pos + NORMAL * (0.4 - dist)

        win.limpiar()
        dibujar_area(win.pantalla, pos, vel, c_proy, c_orto, colisionando)
        win.dibujar_panel_fondo()
        dibujar_panel(win.pantalla, win.fuentes, vel, c_proy, c_orto, colisionando)
        win.terminar_frame()

if __name__ == "__main__":
    main()