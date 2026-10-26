# demos/demo_2.py
import pygame
import math
from src.algebra.vector import Vector
from src.algebra.base import Base2D
from src.render import graficos as G

from src.render.graficos import ANCHO, ALTO, ESCALA, FPS, ESCALA_GLOBAL
from variables import DEMO_2_PANEL_BASE

PANEL_X = int(DEMO_2_PANEL_BASE * ESCALA_GLOBAL)
VELOCIDAD = 2.0
VELOCIDAD_GIRO = 1.2

def rotar(vec, angulo):
    # Rotación de un vector usando matriz de rotación 2D
    c, s = math.cos(angulo), math.sin(angulo)
    return Vector(vec.x * c - vec.y * s, vec.x * s + vec.y * c)


def dibujar_area(pantalla, base, P, c1, c2):
    o = Vector(0, 0)
    v1, v2 = base.v1, base.v2

    G.ejes(pantalla)
    # Rectas generadas por los vectores de la base
    G.recta(pantalla, o, v1, G.COLOR_06, 1)     
    G.recta(pantalla, o, v2, G.COLOR_07, 1)     

    if base.es_valida and c1 is not None and c2 is not None:
        fin1 = v1 * c1
        fin2 = v2 * c2
        # Líneas punteadas: combinación lineal P = c1*v1 + c2*v2
        G.linea_discontinua(pantalla, o, fin1, G.COLOR_10, 8, 5)     
        G.linea_discontinua(pantalla, fin1, P, G.COLOR_10, 8, 5)
        G.linea_discontinua(pantalla, o, fin2, G.COLOR_16, 6, 6)     
        G.linea_discontinua(pantalla, fin2, P, G.COLOR_16, 6, 6)

    # Dibujo de los vectores base
    G.flecha(pantalla, o, v1, G.COLOR_15, 4, 6)  
    G.flecha(pantalla, o, v2, G.COLOR_17, 4, 6)  

    # Punto P en el plano
    px, py = G.a_pantalla(P)
    pygame.draw.circle(pantalla, G.COLOR_12, (px, py), int(9 * ESCALA_GLOBAL))   
    pygame.draw.circle(pantalla, G.COLOR_22, (px, py), int(9 * ESCALA_GLOBAL), max(1, int(2 * ESCALA_GLOBAL)))
    # Origen (vector cero)
    pygame.draw.circle(pantalla, G.COLOR_08, G.a_pantalla(o), int(6 * ESCALA_GLOBAL))   

    f_et = G.fuente(15, bold=True)

    def etiq(txt, vec, color, dx=10, dy=-14):
        px, py = G.a_pantalla(vec)
        pantalla.blit(f_et.render(txt, True, color), (px + int(dx*ESCALA_GLOBAL), py + int(dy*ESCALA_GLOBAL)))

    etiq("v1", v1, G.COLOR_15)
    etiq("v2", v2, G.COLOR_17)
    etiq("P", P, G.COLOR_12, 12, 10)


def dibujar_panel(pantalla, fuentes, base, P, c1, c2):
    f_tit, f_txt = fuentes
    x = PANEL_X + int(15 * ESCALA_GLOBAL)
    y = int(10 * ESCALA_GLOBAL)
    x_fin = ANCHO - int(12 * ESCALA_GLOBAL)

    v1 = base.v1
    v2 = base.v2
    base_valida = base.es_valida
    # Determinante de la matriz [v1, v2]
    det_B = base.determinante()

    y = G.texto(pantalla, "TEMA 3: Bases y cambio de base", f_tit, G.COLOR_13, x, y, 22)
    y = G.sep(pantalla, x, y + int(4*ESCALA_GLOBAL), x_fin)

    # Si det(B) = 0 -> Vectores Linealmente Dependientes
    if not base_valida:
        y = G.texto(pantalla, "!! NO ES BASE !!", f_tit, G.COLOR_19, x, y, 20)
        y = G.texto(pantalla, "v1 y v2 paralelos (det = 0)", f_txt, G.COLOR_19, x, y, 14)
        y = G.sep(pantalla, x, y + int(4*ESCALA_GLOBAL), x_fin)

    y = G.texto(pantalla, "Base actual:", f_tit, G.COLOR_11, x, y, 18)
    y = G.texto(pantalla, f"v1 = ({v1.x:5.2f}, {v1.y:5.2f})", f_txt, G.COLOR_15, x, y, 16)
    y = G.texto(pantalla, f"v2 = ({v2.x:5.2f}, {v2.y:5.2f})", f_txt, G.COLOR_17, x, y, 16)

    if base_valida:
        y = G.texto(pantalla, f"det(B) = {det_B:6.3f}   base valida", f_txt, G.COLOR_16, x, y, 14)
        # Orientación de la base según el signo del determinante
        y = G.texto(pantalla, f"  Orientacion: {base.orientacion()}", f_txt, G.COLOR_08, x, y, 14)
    else:
        y = G.texto(pantalla, f"det(B) = {det_B:6.3f}   NO es base", f_txt, G.COLOR_19, x, y, 14)
        y = G.texto(pantalla, f"  Orientacion: {base.orientacion()}", f_txt, G.COLOR_09, x, y, 14)

    # Validación de ortogonalidad: <v1, v2> = 0
    if base.es_conjunto_ortogonal(): y = G.texto(pantalla, "  Ortogonal: SI", f_txt, G.COLOR_16, x, y, 14)
    else: y = G.texto(pantalla, "  Ortogonal: NO", f_txt, G.COLOR_09, x, y, 14)

    # Validación de ortonormalidad: Ortogonal + ||v|| = 1
    if base.es_base_ortonormal(): y = G.texto(pantalla, "  Ortonormal: SI", f_txt, G.COLOR_16, x, y, 14)
    else: y = G.texto(pantalla, "  Ortonormal: NO", f_txt, G.COLOR_09, x, y, 14)

    y = G.sep(pantalla, x, y + int(6*ESCALA_GLOBAL), x_fin)

    y = G.texto(pantalla, "El mismo punto P:", f_tit, G.COLOR_11, x, y, 18)
    # Coordenadas de P en la base canónica
    y = G.texto(pantalla, f"  P (canonica) = ({P.x:5.2f}, {P.y:5.2f})", f_txt, G.COLOR_12, x, y, 16)
    y = G.texto(pantalla, "    coef. de e1=(1,0) y e2=(0,1)", f_txt, G.COLOR_09, x, y, 13)

    if base_valida and c1 is not None and c2 is not None:
        # Coordenadas de P en la nueva base B
        y = G.texto(pantalla, f"  P (base B)   = ({c1:5.2f}, {c2:5.2f})", f_txt, G.COLOR_16, x, y, 16)
        y = G.texto(pantalla, "    coef. de v1 y v2", f_txt, G.COLOR_09, x, y, 13)
    else:
        y = G.texto(pantalla, "  P (base B)   = no definido (LD)", f_txt, G.COLOR_19, x, y, 16)

    y = G.sep(pantalla, x, y + int(6*ESCALA_GLOBAL), x_fin)

    y = G.texto(pantalla, "Reconstruccion:", f_tit, G.COLOR_11, x, y, 18)
    # Combinación lineal para volver a la base canónica
    y = G.texto(pantalla, "P = c1*v1 + c2*v2", f_txt, G.COLOR_10, x, y, 15)

    if base_valida and c1 is not None and c2 is not None:
        y = G.texto(pantalla, f"  c1 = {c1:5.2f}   c2 = {c2:5.2f}", f_txt, G.COLOR_10, x, y, 14)
        rec = base.reconstruir_desde_base(c1, c2)
        y = G.texto(pantalla, f"  = ({rec.x:5.2f}, {rec.y:5.2f}) = P", f_txt, G.COLOR_16, x, y, 14)

    y = G.sep(pantalla, x, y + int(6*ESCALA_GLOBAL), x_fin)

    y = G.texto(pantalla, "Las 4 bases a demostrar:", f_tit, G.COLOR_11, x, y, 18)
    for linea in ["1. Canonica", "2. Rotada 45", "3. No ortogonal", "4. Invertida"]:
        y = G.texto(pantalla, "  " + linea, f_txt, G.COLOR_08, x, y, 15)

    y = G.sep(pantalla, x, y + int(6*ESCALA_GLOBAL), x_fin)

    y = G.texto(pantalla, "Controles:", f_tit, G.COLOR_11, x, y, 18)
    for linea in ["WASD    mover P", "Flechas mover v1", "IJKL    mover v2", "Q / E   rotar base", "R       resetear", "ESC     salir"]:
        y = G.texto(pantalla, linea, f_txt, G.COLOR_09, x, y, 14)


def main():
    win = G.Ventana("Tema 3: controlas base y vectores", ANCHO, ALTO, PANEL_X, ESCALA, FPS)
    
    # Base canónica inicial y punto P
    v1 = Vector(1.0, 0.0)
    v2 = Vector(0.0, 1.0)
    P = Vector(4.0, 2.0)

    while True:
        dt, teclas, eventos = win.empezar_frame()
        for e in eventos:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_r:
                v1 = Vector(1.0, 0.0); v2 = Vector(0.0, 1.0); P = Vector(4.0, 2.0)

        # Rotación de la base
        if teclas[pygame.K_q]:
            delta = VELOCIDAD_GIRO * dt; v1 = rotar(v1, delta); v2 = rotar(v2, delta)
        if teclas[pygame.K_e]:
            delta = -VELOCIDAD_GIRO * dt; v1 = rotar(v1, delta); v2 = rotar(v2, delta)

        # Traslación de los vectores (suma)
        P = P + Vector((teclas[pygame.K_d] - teclas[pygame.K_a]), (teclas[pygame.K_w] - teclas[pygame.K_s])) * (VELOCIDAD * dt)
        v1 = v1 + Vector((teclas[pygame.K_RIGHT] - teclas[pygame.K_LEFT]), (teclas[pygame.K_UP] - teclas[pygame.K_DOWN])) * (VELOCIDAD * dt)
        v2 = v2 + Vector((teclas[pygame.K_l] - teclas[pygame.K_j]), (teclas[pygame.K_i] - teclas[pygame.K_k])) * (VELOCIDAD * dt)

        # Instanciamos la base con los vectores actuales
        base = Base2D(v1, v2)
        if base.es_valida:
            # Cambio de base: [P]_B = [B]^-1 * P
            c = base.cambiar_de_base(P); c1, c2 = c.x, c.y
        else:
            c1, c2 = None, None

        win.limpiar()
        dibujar_area(win.pantalla, base, P, c1, c2)
        win.dibujar_panel_fondo()
        dibujar_panel(win.pantalla, win.fuentes, base, P, c1, c2)
        win.terminar_frame()

if __name__ == "__main__":
    main()