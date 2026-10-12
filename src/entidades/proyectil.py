from src.algebra.vector import Vector


class Proyectil:
    # Vector en movimiento: p(t) = p0 + v * t.
    # Es una recta en forma parametrica.
    #
    # El hitbox es un circulo de radio `radio`, centrado SIEMPRE
    # en `posicion`. No hay offset: el hitbox coincide con el centro.
    #
    # Sin dueno: el proyectil puede danar a cualquiera, incluido
    # quien lo disparo.
    #
    # Sin pygame: solo algebra y estado del juego.

    def __init__(self, posicion: Vector, direccion: Vector,
                 dano: float,
                 velocidad: float,
                 radio: float,
                 tiempo_vida: float):
        # --- Algebra ---
        self.posicion = posicion
        self.direccion = direccion.normalizar()
        self.velocidad = self.direccion * velocidad

        # --- Hitbox ---
        self.radio = radio

        # --- Gameplay ---
        self.dano = dano
        self.tiempo_vida = tiempo_vida
        self.vivo = True

    # ---------- Ciclo de vida ----------

    def actualizar(self, dt):
        # Movimiento: p(t) = p0 + v * t
        self.posicion = self.posicion + self.velocidad * dt

        # Cuenta atras del tiempo de vida.
        self.tiempo_vida -= dt
        if self.tiempo_vida <= 0:
            self.vivo = False

    # ---------- Colisiones ----------

    def colisiona_con(self, jugador) -> bool:
        # Colision circulo-circulo:
        # ||posicion - jugador.posicion|| <= radio + jugador.radio
        d = (self.posicion - jugador.posicion).magnitud()
        return d <= self.radio + jugador.radio

    # ---------- Debug ----------

    def __repr__(self) -> str:
        return (f"Proyectil(pos={self.posicion}, "
                f"radio={self.radio}, vivo={self.vivo})")