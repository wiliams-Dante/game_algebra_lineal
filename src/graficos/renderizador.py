import pygame
import math


class RenderizadorJugador:
    # Dibuja un Jugador usando sus animaciones.
    #
    # Lee del jugador: `estado`, `posicion`, `direccion_mirada`.
    # No modifica al jugador: solo lee.
    #
    # El sprite se dibuja en:
    #     posicion + offset_sprite
    # Asi se puede alinear con el hitbox (que vive en el jugador
    # como `offset_hitbox`).

    def __init__(self, jugador, animaciones, offset_sprite):
        # jugador: instancia de Jugador (src/entidades/jugador.py)
        # animaciones: dict {"quieto": Animacion, "movimiento": Animacion, ...}
        # offset_sprite: Vector, desplazamiento del sprite respecto a posicion
        self.jugador = jugador
        self.animaciones = animaciones
        self.offset_sprite = offset_sprite

        # Animacion actualmente en reproduccion.
        self.anim_actual = "quieto"
        self.animaciones["quieto"].reiniciar()

    # ---------- Actualizacion ----------

    def actualizar(self, dt):
        # Mira el estado del jugador y reproduce la animacion adecuada.
        estado = self.jugador.estado

        # Si el estado cambio, cambia de animacion.
        if estado != self.anim_actual:
            if estado in self.animaciones:
                self.anim_actual = estado
                self.animaciones[estado].reiniciar()

        # Actualiza la animacion en curso.
        if self.anim_actual in self.animaciones:
            self.animaciones[self.anim_actual].actualizar(dt)

    # ---------- Consultas ----------

    def frame_actual(self) -> int:
        # Devuelve el indice del frame actual (para sincronizar disparos).
        if self.anim_actual in self.animaciones:
            return self.animaciones[self.anim_actual].indice
        return 0

    def animacion_terminada(self) -> bool:
        # True si la animacion actual termino (util para volver a "quieto").
        if self.anim_actual in self.animaciones:
            return self.animaciones[self.anim_actual].terminada
        return True

    # ---------- Dibujo ----------

    def dibujar(self, pantalla, a_pantalla):
        # Dibuja el frame actual centrado en posicion + offset_sprite.
        if self.anim_actual not in self.animaciones:
            return
        frame = self.animaciones[self.anim_actual].frame_actual()
        if frame is None:
            return

        # Voltear horizontalmente si mira a la izquierda.
        if self.jugador.direccion_mirada < 0:
            frame = pygame.transform.flip(frame, True, False)

        # Centro donde se dibuja el sprite.
        centro_mundo = self.jugador.posicion + self.offset_sprite

        rect = frame.get_rect(center=a_pantalla(centro_mundo))
        pantalla.blit(frame, rect)

    # ---------- Debug (opcional) ----------

    def dibujar_hitbox_debug(self, pantalla, a_pantalla):
        # Dibuja el circulo del hitbox del jugador (para depurar).
        centro = self.jugador.centro_hitbox()
        pygame.draw.circle(pantalla, (255, 60, 60),
                           a_pantalla(centro),
                           int(self.jugador.radio), 1)


class RenderizadorProyectil:
    # Dibuja un Proyectil usando su sprite.
    #
    # Lee del proyectil: `posicion`, `velocidad`.
    # El sprite se dibuja en:
    #     posicion + offset_sprite
    #
    # El sprite se rota segun la direccion del proyectil y
    # se voltea si va hacia la izquierda.

    def __init__(self, proyectil, sprite, offset_sprite):
        # proyectil: instancia de Proyectil
        # sprite: Surface ya escalada al tamano deseado
        # offset_sprite: Vector, desplazamiento del sprite
        self.proyectil = proyectil
        self.sprite = sprite
        self.offset_sprite = offset_sprite

    def actualizar(self, dt):
        # El proyectil no tiene animacion: no hace nada.
        pass

    def dibujar(self, pantalla, a_pantalla):
        if self.sprite is None:
            return

        img = self.sprite
        vx = self.proyectil.velocidad.x
        vy = self.proyectil.velocidad.y

        # Horizontal puro: solo flip (mas nitido).
        if abs(vy) < 1:
            if vx < 0:
                img = pygame.transform.flip(img, True, False)
        else:
            # Diagonal o vertical: rotar.
            angulo = math.degrees(math.atan2(-vy, vx))
            img = pygame.transform.rotate(img, angulo)
            # Corregir "boca abajo" al apuntar hacia la izquierda.
            if vx < 0:
                img = pygame.transform.flip(img, False, True)

        # Centro donde se dibuja el sprite.
        centro_mundo = self.proyectil.posicion + self.offset_sprite

        rect = img.get_rect(center=a_pantalla(centro_mundo))
        pantalla.blit(img, rect)

    # ---------- Debug (opcional) ----------

    def dibujar_hitbox_debug(self, pantalla, a_pantalla):
        # Dibuja el circulo del hitbox del proyectil.
        centro = self.proyectil.centro_hitbox()
        pygame.draw.circle(pantalla, (255, 60, 60),
                           a_pantalla(centro),
                           int(self.proyectil.radio), 1)