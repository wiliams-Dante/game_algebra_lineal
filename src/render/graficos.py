# src/render/graficos.py
import pygame
import sys
import os
import math
from src.algebra.vector import Vector

# Importamos configuración y paleta desde variables.py
from variables import (
    ESCALA_GLOBAL, ANCHO, ALTO, FPS, ESCALA,
    COLOR_01, COLOR_02, COLOR_03, COLOR_04, COLOR_05,
    COLOR_06, COLOR_07, COLOR_08, COLOR_09, COLOR_10,
    COLOR_11, COLOR_12, COLOR_13, COLOR_14, COLOR_15,
    COLOR_16, COLOR_17, COLOR_18, COLOR_19, COLOR_20,
    COLOR_21, COLOR_22, COLOR_23, COLOR_24, COLOR_25,
)

def fuente(tamaño, bold=False):
    tam_final = max(8, int(tamaño * ESCALA_GLOBAL))
    return pygame.font.SysFont("Courier New", tam_final, bold=bold)

def brillo(color, factor=1.3):
    return tuple(min(255, int(c * factor)) for c in color[:3])

def oscurecer(color, factor=0.6):
    return tuple(max(0, int(c * factor)) for c in color[:3])

def pulso(color, t, intensidad=0.1, velocidad=2.0):
    factor = 1.0 + math.sin(t * velocidad) * intensidad
    return tuple(min(255, int(c * factor)) for c in color[:3])

# ==================================================
# 1) MUNDO y CÁMARA
# ==================================================
_origen = Vector(0, 0)
_escala = 70.0
_camara = Vector(0, 0)

def configurar(origen_pantalla, escala):
    global _origen, _escala
    _origen = origen_pantalla
    _escala = escala

def configurar_camara(pos_camara):
    global _camara
    _camara = pos_camara

def a_pantalla(p):
    p_relativo = p - _camara
    return (int(_origen.x + p_relativo.x * _escala),
            int(_origen.y - p_relativo.y * _escala))

def clamp(v, minimo, maximo):
    return max(minimo, min(maximo, v))

# ==================================================
# 2) DIBUJO
# ==================================================
def flecha(pantalla, origen, vector, color, grosor=3, radio_punta=5):
    fin = origen + vector
    pygame.draw.line(pantalla, color, a_pantalla(origen), a_pantalla(fin),
                     max(1, int(grosor * ESCALA_GLOBAL)))
    pygame.draw.circle(pantalla, color, a_pantalla(fin),
                       max(1, int(radio_punta * ESCALA_GLOBAL)))

def ejes(pantalla, largo=5.0, color=None):
    c = color if color is not None else COLOR_04
    pygame.draw.line(pantalla, c, a_pantalla(Vector(-largo, 0)), a_pantalla(Vector(largo, 0)), 1)
    pygame.draw.line(pantalla, c, a_pantalla(Vector(0, -largo)), a_pantalla(Vector(0, largo)), 1)

def recta(pantalla, punto, direccion, color, grosor=1, L=18.0):
    if direccion.magnitud() < 1e-6: return
    d = direccion.normalizar()
    pygame.draw.line(pantalla, color, a_pantalla(punto + d * (-L)), a_pantalla(punto + d * L),
                     max(1, int(grosor * ESCALA_GLOBAL)))

def linea_discontinua(pantalla, a, b, color, dash=8, gap=5):
    pa, pb = a_pantalla(a), a_pantalla(b)
    dx, dy = pb[0] - pa[0], pb[1] - pa[1]
    largo = (dx * dx + dy * dy) ** 0.5
    if largo == 0: return
    ux, uy = dx / largo, dy / largo
    pos = 0
    while pos < largo:
        fin = min(pos + dash, largo)
        pygame.draw.line(pantalla, color,
                         (int(pa[0] + ux * pos), int(pa[1] + uy * pos)),
                         (int(pa[0] + ux * fin), int(pa[1] + uy * fin)), 1)
        pos += dash + gap

def texto(pantalla, txt, fuente_txt, color, x, y, salto=22):
    pantalla.blit(fuente_txt.render(txt, True, color), (x, y))
    return y + int(salto * ESCALA_GLOBAL)

def sep(pantalla, x, y, x_fin, color=None):
    c = color if color is not None else COLOR_03
    pygame.draw.line(pantalla, c, (x, y), (x_fin, y), max(1, int(1 * ESCALA_GLOBAL)))
    return y + int(8 * ESCALA_GLOBAL)

# ==================================================
# 3) VENTANA
# ==================================================
class Ventana:
    def __init__(self, titulo, ancho=None, alto=None, panel_x=None, escala=None, fps=None, fullscreen=None, vsync=1):
        ancho = ancho if ancho is not None else ANCHO
        alto = alto if alto is not None else ALTO
        panel_x = panel_x if panel_x is not None else ancho
        escala = escala if escala is not None else ESCALA
        fps = fps if fps is not None else FPS

        if fullscreen is None:
            fullscreen = os.environ.get("FULLSCREEN") == "1"

        pygame.init()
        flags = pygame.SCALED
        if fullscreen: flags |= pygame.FULLSCREEN

        try:
            self.pantalla = pygame.display.set_mode((ancho, alto), flags, vsync=vsync)
        except pygame.error:
            self.pantalla = pygame.display.set_mode((ancho, alto), flags)

        pygame.display.set_caption(titulo)
        self.reloj = pygame.time.Clock()
        self.fps, self.ancho, self.alto, self.panel_x = fps, ancho, alto, panel_x

        self.f_tit = fuente(16, bold=True)
        self.f_txt = fuente(13)
        self.fuentes = (self.f_tit, self.f_txt)

        configurar(Vector(panel_x / 2, alto / 2), escala)
        configurar_camara(Vector(0, 0))

    def salir(self):
        pygame.quit()
        sys.exit()

    def empezar_frame(self):
        dt = self.reloj.tick(self.fps) / 1000.0
        teclas = pygame.key.get_pressed()
        eventos = list(pygame.event.get())
        for e in eventos:
            if e.type == pygame.QUIT:
                self.salir()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                self.salir()
        return dt, teclas, eventos

    def limpiar(self):
        self.pantalla.fill(COLOR_01)

    def dibujar_panel_fondo(self):
        pygame.draw.rect(self.pantalla, COLOR_02, (self.panel_x, 0, self.ancho - self.panel_x, self.alto))
        pygame.draw.line(self.pantalla, COLOR_03, (self.panel_x, 0), (self.panel_x, self.alto),
                         max(1, int(2 * ESCALA_GLOBAL)))

    def terminar_frame(self):
        pygame.display.flip()