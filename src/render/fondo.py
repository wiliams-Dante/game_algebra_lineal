# src/render/fondo.py
import pygame
import random
import math
from variables import PARTICULAS_COLORES, COLOR_01, COLOR_25

class _Particula:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.reiniciar(primera_vez=True)

    def reiniciar(self, primera_vez=False):
        self.x = random.uniform(0, self.ancho)
        self.y = random.uniform(0, self.alto)

        angulo = random.uniform(0, 2 * math.pi)
        rapidez = random.uniform(30.0, 100.0)
        self.vel_x = math.cos(angulo) * rapidez
        self.vel_y = math.sin(angulo) * rapidez

        self.tamaño = random.randint(1, 2)

        # Paleta Atardecer: jade, coral, violeta, dorado
        self.color = random.choice(PARTICULAS_COLORES)

        self.vida_max = random.uniform(4.0, 10.0)
        self.vida = self.vida_max

    def actualizar(self, dt):
        self.x += self.vel_x * dt
        self.y += self.vel_y * dt
        self.vida -= dt
        if (self.x < -50 or self.x > self.ancho + 50 or
            self.y < -50 or self.y > self.alto + 50 or
            self.vida <= 0):
            self.reiniciar(primera_vez=False)

def cargar_capas_fondo(ANCHO, ALTO):
    def cargar_capa(nombre_archivo):
        try:
            ruta = f"assets/images/sprites_fondo/{nombre_archivo}"
            img = pygame.image.load(ruta).convert_alpha()
            w, h = img.get_size()
            nuevo_w = int(w * (ALTO / h))
            return pygame.transform.scale(img, (nuevo_w, ALTO))
        except FileNotFoundError:
            return None

    return [
        (cargar_capa("fondo.png"), 0.1),
        (cargar_capa("lejos.png"), 0.3),
        (cargar_capa("medio.png"), 0.6),
        (cargar_capa("cerca.png"), 0.9)
    ]

def crear_particulas(ANCHO, ALTO, cantidad=80):
    return [_Particula(ANCHO, ALTO) for _ in range(cantidad)]

def dibujar_fondo(pantalla, camara_x, particulas, capas_fondo, ESCALA, ANCHO, ALTO, dt):
    # Noche profunda violeta
    pantalla.fill(COLOR_01)
    for imagen, factor in capas_fondo:
        if imagen:
            parallax_x = int(-camara_x * ESCALA * factor)
            ancho_img = imagen.get_width()
            x = parallax_x % ancho_img - ancho_img
            while x < ANCHO:
                pantalla.blit(imagen, (x, 0))
                x += ancho_img

    for p in particulas:
        p.actualizar(dt)
        if -50 < p.x < ANCHO + 50 and -50 < p.y < ALTO + 50:
            alpha = 255
            if p.vida < 1.0:
                alpha = int((p.vida / 1.0) * 255)
            elif p.vida > p.vida_max - 1.0:
                alpha = int(((p.vida_max - p.vida) / 1.0) * 255)

            glow_alpha = int(alpha * 0.20)
            glow_size = p.tamaño * 3
            surf_glow = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
            pygame.draw.circle(surf_glow, (*p.color, glow_alpha), (glow_size, glow_size), glow_size)
            pantalla.blit(surf_glow, (p.x - glow_size, p.y - glow_size))

            surf = pygame.Surface((p.tamaño * 2, p.tamaño * 2), pygame.SRCALPHA)
            pygame.draw.circle(surf, (*p.color, alpha), (p.tamaño, p.tamaño), p.tamaño)
            pantalla.blit(surf, (p.x - p.tamaño, p.y - p.tamaño))

    capa_oscura = pygame.Surface((ANCHO, ALTO))
    capa_oscura.set_alpha(100)
    capa_oscura.fill(COLOR_25)
    pantalla.blit(capa_oscura, (0, 0))