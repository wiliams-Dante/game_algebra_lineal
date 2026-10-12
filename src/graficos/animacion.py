class Animacion:
    # Gestiona una secuencia de frames y su reproduccion en el tiempo.
    #
    # Solo tiene una lista de frames,
    # un temporizador y un indice.
    #
    # - bucle=True  -> se repite indefinidamente (idle, caminar).
    # - bucle=False -> se reproduce una vez y se queda en el ultimo frame.

    def __init__(self, frames, duracion_frame, bucle):
        self.frames = frames                 # lista de Surface
        self.duracion_frame = duracion_frame # segundos por frame
        self.bucle = bucle
        self.indice = 0
        self.tiempo = 0.0
        self.terminada = False

    def reiniciar(self):
        # Vuelve al primer frame y desactiva la bandera de terminada.
        self.indice = 0
        self.tiempo = 0.0
        self.terminada = False

    def actualizar(self, dt):
        # Avanza el temporizador y cambia de frame cuando toca.
        if self.terminada:
            return
        self.tiempo += dt
        if self.tiempo >= self.duracion_frame:
            self.tiempo -= self.duracion_frame
            self.indice += 1
            if self.indice >= len(self.frames):
                if self.bucle:
                    self.indice = 0
                else:
                    self.indice = len(self.frames) - 1
                    self.terminada = True

    def frame_actual(self):
        # Devuelve la Surface del frame que toca mostrar.
        if not self.frames:
            return None
        return self.frames[self.indice]

    def __repr__(self):
        return (f"Animacion(frames={len(self.frames)}, "
                f"indice={self.indice}, bucle={self.bucle}, "
                f"terminada={self.terminada})")