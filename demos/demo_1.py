import pygame
from src.algebra.vector import Vector
from src.render import graficos as G
from src.render.graficos import ANCHO, ALTO, ESCALA, FPS, ESCALA_GLOBAL
from variables import DEMO_1_PANEL_BASE
from src.algebra.base import determinante_2x2

PANEL_X = int(DEMO_1_PANEL_BASE * ESCALA_GLOBAL)
VELOCIDAD = 2.0
C_ESCALAR = 1.5
D_ESCALAR = 2.0


def dibujar_area(pantalla, u, v, z, en_w):
    o = Vector(0, 0)
    c, d = C_ESCALAR, D_ESCALAR

    G.ejes(pantalla)
    
    # Recta afín: y = x + 1 (no pasa por el origen)
    G.recta(pantalla, Vector(0, 1), Vector(1, 1), G.COLOR_05, 1)       
    G.recta(pantalla, o, v, G.COLOR_07, 2)                              

    # Axiomas 1 y 2: u + v (cerradura y conmutatividad)
    suma = u + v
    pygame.draw.line(pantalla, G.COLOR_04, G.a_pantalla(v), G.a_pantalla(suma), 1)   
    pygame.draw.line(pantalla, G.COLOR_04, G.a_pantalla(u), G.a_pantalla(suma), 1)

    # Axioma 6: c * u (cerradura bajo escalar)
    u_c = u * c
    v_c = v * c
    suma_c = u_c + v_c
    
    # Axioma 7: c*(u+v) = c*u + c*v
    pygame.draw.line(pantalla, G.COLOR_05, G.a_pantalla(v_c), G.a_pantalla(suma_c), 1)  
    pygame.draw.line(pantalla, G.COLOR_05, G.a_pantalla(u_c), G.a_pantalla(suma_c), 1)

    # Axioma 9: c*(d*u) = (c*d)*u
    u_cd = u * (c * d)
    pygame.draw.line(pantalla, G.COLOR_04, G.a_pantalla(u * (-0.5)), G.a_pantalla(u_cd + u * 0.5), 1)

    # Axioma 3: (u+v)+z = u+(v+z)
    suma_z = suma + z
    G.linea_discontinua(pantalla, suma, suma_z, G.COLOR_11)             
    G.linea_discontinua(pantalla, z, suma_z, G.COLOR_11)

    # Si z es paralelo a v, pertenece al subespacio W = gen{v}
    color_z = G.COLOR_16 if en_w else G.COLOR_13                        
    
    G.flecha(pantalla, o, u, G.COLOR_15, 4, 6)                          
    G.flecha(pantalla, o, v, G.COLOR_17, 4, 6)                          
    G.flecha(pantalla, o, z, color_z, 4, 6)
    G.flecha(pantalla, o, suma, G.COLOR_11, 2, 4)                       
    G.flecha(pantalla, o, u_c, G.COLOR_20, 2, 4)                        
    G.flecha(pantalla, o, u * (c + d), G.COLOR_21, 2, 4)                
    
    # Axioma 5: Inverso aditivo (u + -u = 0)
    G.flecha(pantalla, o, u * (-1), G.COLOR_14, 2, 4)                   
    G.flecha(pantalla, o, suma_c, G.COLOR_15, 2, 4)                     
    G.flecha(pantalla, o, u_cd, G.COLOR_11, 2, 4)                       
    G.flecha(pantalla, o, suma_z, G.COLOR_11, 2, 4)                     

    # Axioma 4: Vector neutro (origen)
    pygame.draw.circle(pantalla, G.COLOR_08, G.a_pantalla(o), 6)        

    f_et = G.fuente(14, bold=True)
    def etiq(txt, vec, color, dx=10, dy=-14):
        px, py = G.a_pantalla(vec)
        pantalla.blit(f_et.render(txt, True, color), (px + int(dx*ESCALA_GLOBAL), py + int(dy*ESCALA_GLOBAL)))

    etiq("u", u, G.COLOR_15)
    etiq("v", v, G.COLOR_17)
    etiq("z", z, color_z)
    etiq("1,2", suma, G.COLOR_11)
    etiq("3", suma_z, G.COLOR_11)
    etiq("6", u_c, G.COLOR_20)
    etiq("8", u * (c + d), G.COLOR_21)
    etiq("5", u * (-1), G.COLOR_14)
    etiq("7", suma_c, G.COLOR_15)
    etiq("9", u_cd, G.COLOR_11)

    px, py = G.a_pantalla(Vector(2.5, 3.5))
    sup = f_et.render("y = x + 1  (afín, NO subespacio)", True, G.COLOR_05)
    pantalla.blit(sup, (px, py))

    if en_w:
        f_big = G.fuente(22, bold=True)
        sup = f_big.render("z PERTENECE a W  (subespacio)", True, G.COLOR_16)
        pantalla.blit(sup, (int(30*ESCALA_GLOBAL), int(30*ESCALA_GLOBAL)))


def dibujar_panel(pantalla, fuentes, u, v, z, en_w):
    f_tit, f_txt = fuentes
    x = PANEL_X + int(15 * ESCALA_GLOBAL)
    y = int(10 * ESCALA_GLOBAL)
    x_fin = ANCHO - int(12 * ESCALA_GLOBAL)

    c, d = C_ESCALAR, D_ESCALAR
    cero = Vector(0, 0)
    
    # Cálculos para demostrar los 10 axiomas
    suma = u + v
    suma_inv = v + u                 # Axioma 2
    neutro_a = u + cero              # Axioma 4
    inverso_a = u + (u * (-1))       # Axioma 5
    doble_u = u * c                  # Axioma 6
    dist1_izq = (u + v) * c          # Axioma 7
    dist1_der = u * c + v * c        # Axioma 7
    dist2_izq = u * (c + d)          # Axioma 8
    dist2_der = u * c + u * d        # Axioma 8
    asoc_izq = u * (c * d)           # Axioma 9
    asoc_der = (u * c) * d           # Axioma 9
    neutro_e = u * 1                 # Axioma 10
    asoc_suma_izq = (u + v) + z      # Axioma 3
    asoc_suma_der = u + (v + z)      # Axioma 3

    y = G.texto(pantalla, f"u=({u.x:5.2f},{u.y:5.2f})   v=({v.x:5.2f},{v.y:5.2f})", f_txt, G.COLOR_08, x, y, 16)
    y = G.texto(pantalla, f"z=({z.x:5.2f},{z.y:5.2f})   c={c}   d={d}", f_txt, G.COLOR_11, x, y, 16)
    y = G.sep(pantalla, x, y + int(4*ESCALA_GLOBAL), x_fin)

    y = G.texto(pantalla, "TEMA 1: Espacio vectorial", f_tit, G.COLOR_13, x, y, 20)

    # Demostración numérica de los 10 axiomas
    axiomas = [
        ("1", "Cerradura +", "u + v  pertenece a  V", f"({suma.x:.2f},{suma.y:.2f})  OK", G.COLOR_11),
        ("2", "Conmutativa", "u + v = v + u", f"({suma.x:.2f},{suma.y:.2f}) = ({suma_inv.x:.2f},{suma_inv.y:.2f})", G.COLOR_11),
        ("3", "Asociativa +", "(u+v)+z = u+(v+z)", f"({asoc_suma_izq.x:.2f},{asoc_suma_izq.y:.2f}) = ({asoc_suma_der.x:.2f},{asoc_suma_der.y:.2f})", G.COLOR_11),
        ("4", "Neutro +", "u + 0 = u", f"({neutro_a.x:.2f},{neutro_a.y:.2f}) = ({u.x:.2f},{u.y:.2f})", G.COLOR_15),
        ("5", "Inverso +", "u + (-u) = 0", f"({inverso_a.x:.2f},{inverso_a.y:.2f}) = (0.00,0.00)", G.COLOR_14),
        ("6", "Cerradura *", "c * u  pertenece a  V", f"({doble_u.x:.2f},{doble_u.y:.2f})  OK", G.COLOR_20),
        ("7", "Distributiva 1", "c*(u+v) = c*u + c*v", f"({dist1_izq.x:.2f},{dist1_izq.y:.2f}) = ({dist1_der.x:.2f},{dist1_der.y:.2f})", G.COLOR_15),
        ("8", "Distributiva 2", "(c+d)*u = c*u + d*u", f"({dist2_izq.x:.2f},{dist2_izq.y:.2f}) = ({dist2_der.x:.2f},{dist2_der.y:.2f})", G.COLOR_21),
        ("9", "Asociativa *", "c*(d*u) = (c*d)*u", f"({asoc_izq.x:.2f},{asoc_izq.y:.2f}) = ({asoc_der.x:.2f},{asoc_der.y:.2f})", G.COLOR_11),
        ("10", "Neutro *", "1 * u = u", f"({neutro_e.x:.2f},{neutro_e.y:.2f}) = ({u.x:.2f},{u.y:.2f})", G.COLOR_15),
    ]

    for num, nombre, formula, valor, color in axiomas:
        pantalla.blit(f_txt.render(f"{num:>2}.", True, color), (x, y))
        pantalla.blit(f_txt.render(nombre, True, color), (x + int(25 * ESCALA_GLOBAL), y))
        y += int(15 * ESCALA_GLOBAL)
        pantalla.blit(f_txt.render(f"     {formula}", True, G.COLOR_10), (x, y))
        y += int(14 * ESCALA_GLOBAL)
        pantalla.blit(f_txt.render(f"     {valor}", True, G.COLOR_16), (x, y))
        y += int(21 * ESCALA_GLOBAL)

    y = G.sep(pantalla, x, y + int(4*ESCALA_GLOBAL), x_fin)

    # Subespacio: W = gen{v} (todas las combinaciones de v)
    y = G.texto(pantalla, "TEMA 2: Subespacio vectorial", f_tit, G.COLOR_13, x, y, 20)
    y = G.texto(pantalla, "W = gen{v} = { t*v : t en R }", f_txt, G.COLOR_07, x, y, 16)
    
    # Test de dependencia lineal: si det(z,v)=0, son paralelos (z pertenece a W)
    y = G.texto(pantalla, "Test:  z en W <=> det(z,v)=0", f_txt, G.COLOR_10, x, y, 14)
    y = G.texto(pantalla, f"  det(z,v) = {determinante_2x2(z, v):6.3f}", f_txt, G.COLOR_08, x, y, 14)

    if en_w:
        y = G.texto(pantalla, "  z PERTENECE a W", f_txt, G.COLOR_16, x, y, 18)
    else:
        y = G.texto(pantalla, "  z NO pertenece a W", f_txt, G.COLOR_19, x, y, 18)


def main():
    win = G.Ventana("Tema 1 y 2: espacio + subespacio", ANCHO, ALTO, PANEL_X, ESCALA, FPS)
    # Vectores iniciales en R2
    u = Vector(2.0, 1.0)
    v = Vector(1.0, 0.5)
    z = Vector(-1.0, 1.5)

    while True:
        dt, teclas, eventos = win.empezar_frame()
        for e in eventos:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_r:
                u = Vector(2.0, 1.0); v = Vector(1.0, 0.5); z = Vector(-1.0, 1.5)

        # Actualización de posición con suma de vectores
        u = u + Vector((teclas[pygame.K_d] - teclas[pygame.K_a]), (teclas[pygame.K_w] - teclas[pygame.K_s])) * (VELOCIDAD * dt)
        v = v + Vector((teclas[pygame.K_RIGHT] - teclas[pygame.K_LEFT]), (teclas[pygame.K_UP] - teclas[pygame.K_DOWN])) * (VELOCIDAD * dt)
        z = z + Vector((teclas[pygame.K_l] - teclas[pygame.K_j]), (teclas[pygame.K_i] - teclas[pygame.K_k])) * (VELOCIDAD * dt)
        
        # Condición de subespacio: si det(z,v) ~ 0, z está en W
        en_w = abs(determinante_2x2(z, v)) < 0.05

        win.limpiar()
        dibujar_area(win.pantalla, u, v, z, en_w)
        win.dibujar_panel_fondo()
        dibujar_panel(win.pantalla, win.fuentes, u, v, z, en_w)
        win.terminar_frame()

if __name__ == "__main__":
    main()