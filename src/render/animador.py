# src/render/sprites.py
import pygame
import os
from variables import SPRITE_FALLBACK

class Animador:
    def __init__(self, ruta_base, fps_animacion=12, tamaño=(120, 120)):
        self.fps_animacion = fps_animacion
        self.duracion_frame = 1.0 / fps_animacion
        self.tiempo_actual = 0.0
        self.indice_frame = 0
        self.tamaño = tamaño
        self.animaciones = {}
        self._estado_actual = None
        self.terminado = False

        estados = [
            "quieto", "movimiento", "asciende", "desciende",
            "ataque_normal", "ataque_distancia", "muere"
        ]

        for estado in estados:
            self.animaciones[estado] = self._cargar_carpeta(ruta_base, estado)

        self.animaciones["recibe_dano"] = self._cargar_carpeta(ruta_base, "recibe_dano")

    def _cargar_carpeta(self, ruta_base, nombre_carpeta):
        ruta = os.path.join(ruta_base, nombre_carpeta)
        frames = []
        if not os.path.exists(ruta):
            return [self._crear_sprite_vacio()]

        archivos = sorted([f for f in os.listdir(ruta) if f.startswith("sprite_") and f.endswith(".png")])
        for archivo in archivos:
            img = pygame.image.load(os.path.join(ruta, archivo)).convert_alpha()
            img = pygame.transform.scale(img, self.tamaño)
            frames.append(img)

        if not frames:
            return [self._crear_sprite_vacio()]
        return frames

    def _crear_sprite_vacio(self):
        surf = pygame.Surface(self.tamaño, pygame.SRCALPHA)
        surf.fill(SPRITE_FALLBACK)
        return surf

    def reiniciar(self):
        self.tiempo_actual = 0.0
        self.indice_frame = 0
        self.terminado = False

    def actualizar(self, dt, estado):
        frames = self.animaciones.get(estado, self.animaciones["quieto"])

        if self._estado_actual != estado:
            self._estado_actual = estado
            self.reiniciar()

        fps_actual = 12
        if estado == "ataque_distancia":
            fps_actual = 20

        duracion_frame_actual = 1.0 / fps_actual

        self.tiempo_actual += dt
        if self.tiempo_actual >= duracion_frame_actual:
            self.tiempo_actual -= duracion_frame_actual
            self.indice_frame += 1

            if self.indice_frame >= len(frames):
                if estado == "muere":
                    self.indice_frame = len(frames) - 1
                else:
                    self.indice_frame = 0
                self.terminado = True

    def dibujar(self, pantalla, posicion_pantalla, direccion_mirada):
        frames = self.animaciones.get(self._estado_actual, self.animaciones["quieto"])
        imagen = frames[self.indice_frame]

        if direccion_mirada < 0:
            imagen = pygame.transform.flip(imagen, True, False)

        rect = imagen.get_rect(center=posicion_pantalla)
        pantalla.blit(imagen, rect)

    def ha_terminado(self):
        return self.terminado