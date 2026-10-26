# launcher.py
import pygame
import sys
import subprocess

from src.render import fondo as F
from src.render import graficos as G
from src.render.graficos import ANCHO, ALTO, ESCALA, FPS, ESCALA_GLOBAL
from variables import (
    ANCHO, ALTO, ESCALA, FPS, ESCALA_GLOBAL,
    COLOR_08,   # texto principal
    COLOR_09,   # texto dim
    COLOR_10,   # texto teoría
    COLOR_13,   # violeta (P2 menú, opción seleccionada)
    COLOR_16,   # jade (P1 menú, carátula)
)

CENTRO = ANCHO // 2

def dibujar_caratula(pantalla, tiempo, particulas, capas_fondo):
    F.dibujar_fondo(pantalla, tiempo * 2.0, particulas, capas_fondo, ESCALA, ANCHO, ALTO, 1/60.0)

    f_uni = G.fuente(26, bold=True)
    f_fac = G.fuente(18)
    f_tit = G.fuente(22, bold=True)
    f_sub = G.fuente(20)
    f_txt = G.fuente(16)
    f_alum = G.fuente(15)

    color_titulo = G.pulso(COLOR_16, tiempo, 0.08, 1.5)
    color_subtitulo = G.pulso(COLOR_13, tiempo, 0.08, 1.5)

    textos = [
        ("UNIVERSIDAD NACIONAL DE SAN AGUSTÍN", f_uni, COLOR_08, int(40 * ESCALA_GLOBAL)),
        ("Facultad de Ingeniería de Producción y Servicios", f_fac, COLOR_09, int(75 * ESCALA_GLOBAL)),
        ("Escuela Profesional de Ingeniería Electrónica", f_fac, COLOR_09, int(100 * ESCALA_GLOBAL)),
        ("TRABAJO DE INVESTIGACIÓN FORMATIVA", f_tit, color_titulo, int(150 * ESCALA_GLOBAL)),
        ("Álgebra Lineal Computacional Aplicada al Desarrollo de Videojuegos 2D", f_sub, color_subtitulo, int(180 * ESCALA_GLOBAL)),
        ("Docente: Dr. Eddy Gutiérrez Rodríguez", f_txt, COLOR_10, int(230 * ESCALA_GLOBAL)),
        ("Curso: Álgebra Lineal", f_txt, COLOR_10, int(255 * ESCALA_GLOBAL)),
        ("Grupo asignado: Grupo I", f_txt, COLOR_10, int(280 * ESCALA_GLOBAL)),
    ]

    for texto, fuente, color, y in textos:
        txt = fuente.render(texto, True, color)
        sombra = fuente.render(texto, True, (0, 0, 0))
        pantalla.blit(sombra, (CENTRO - txt.get_width()//2 + 2, y + 2))
        pantalla.blit(txt, (CENTRO - txt.get_width()//2, y))

    txt_integrantes = f_txt.render("Integrantes:", True, color_titulo)
    pantalla.blit(txt_integrantes, (CENTRO - txt_integrantes.get_width()//2, int(320 * ESCALA_GLOBAL)))

    alumnos = [
        "Ajahuana Coaguila Renato Arley", "Castilla Ccahuna Luis Alberto",
        "Ccorimaya Mamani Dayana V", "Condori Sonco Faustino Horacio",
        "Puelles Albarracin David", "Ramos Calderon Jose Rodrigo",
        "Stephanie Susan Vásquez Gorbeña", "Sullcapuma Ccallo Kevin Leonardo",
        "Surco Almiron Arturo Enmanuel", "Taipe Huanca Wiliams Yeferson",
        "Yerson Dorregaray Chaco"
    ]

    x_izq = CENTRO - int(390 * ESCALA_GLOBAL)
    x_der = CENTRO + int(40 * ESCALA_GLOBAL)

    col_izq, col_der = alumnos[:6], alumnos[6:]
    y_alum = int(350 * ESCALA_GLOBAL)
    salto_alum = int(25 * ESCALA_GLOBAL)

    for i in range(6):
        pantalla.blit(f_alum.render(f"• {col_izq[i]}", True, COLOR_08), (x_izq, y_alum))
        if i < len(col_der):
            pantalla.blit(f_alum.render(f"• {col_der[i]}", True, COLOR_08), (x_der, y_alum))
        y_alum += salto_alum

    txt_pie = f_fac.render("Arequipa - 2026", True, COLOR_09)
    pantalla.blit(txt_pie, (CENTRO - txt_pie.get_width()//2, int(550 * ESCALA_GLOBAL)))

def dibujar_menu(pantalla, tiempo, seleccion, opciones, particulas, capas_fondo):
    F.dibujar_fondo(pantalla, tiempo * 2.0, particulas, capas_fondo, ESCALA, ANCHO, ALTO, 1/60.0)
    f_opc = G.fuente(26, bold=True)

    y_inicio = int(280 * ESCALA_GLOBAL)
    salto_menu = int(60 * ESCALA_GLOBAL)

    for i, texto in enumerate(opciones):
        y = y_inicio + i * salto_menu
        color = COLOR_13 if i == seleccion else COLOR_09

        txt = f_opc.render(texto, True, color)
        pantalla.blit(txt, (CENTRO - txt.get_width()//2, y))

def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Presentación - Álgebra Lineal")
    reloj = pygame.time.Clock()

    capas_fondo = F.cargar_capas_fondo(ANCHO, ALTO)
    particulas = F.crear_particulas(ANCHO, ALTO, cantidad=60)

    estado = "caratula"
    seleccion = 0
    opciones = [
        "Jugar Videojuego",
        "Demo 1: Espacios y Subespacios Vectoriales",
        "Demo 2: Bases y Cambio de Base",
        "Demo 3: Producto Interno y Ortogonalidad",
        "Salir"
    ]

    tiempo = 0
    while True:
        dt = reloj.tick(FPS) / 1000.0
        tiempo += dt

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()

                if estado == "caratula" and e.key == pygame.K_RETURN:
                    estado = "menu"
                    tiempo = 0

                elif estado == "menu":
                    if e.key == pygame.K_DOWN:
                        seleccion = (seleccion + 1) % len(opciones)
                    elif e.key == pygame.K_UP:
                        seleccion = (seleccion - 1) % len(opciones)
                    elif e.key == pygame.K_RETURN:

                        if seleccion == 4:
                            pygame.quit(); sys.exit()

                        pygame.display.quit()
                        pygame.quit()

                        cmd = []
                        if seleccion == 0: cmd = [sys.executable, "main.py"]
                        elif seleccion == 1: cmd = [sys.executable, "-m", "demos.demo_1"]
                        elif seleccion == 2: cmd = [sys.executable, "-m", "demos.demo_2"]
                        elif seleccion == 3: cmd = [sys.executable, "-m", "demos.demo_3"]

                        if cmd:
                            subprocess.run(cmd)

                        pygame.init()
                        pantalla = pygame.display.set_mode((ANCHO, ALTO))
                        pygame.display.set_caption("Presentación - Álgebra Lineal")
                        pygame.event.clear()
                        capas_fondo = F.cargar_capas_fondo(ANCHO, ALTO)
                        particulas = F.crear_particulas(ANCHO, ALTO, cantidad=40)
                        estado = "menu"
                        tiempo = 0

        if estado == "caratula":
            dibujar_caratula(pantalla, tiempo, particulas, capas_fondo)
        elif estado == "menu":
            dibujar_menu(pantalla, tiempo, seleccion, opciones, particulas, capas_fondo)

        pygame.display.flip()

if __name__ == "__main__":
    main()