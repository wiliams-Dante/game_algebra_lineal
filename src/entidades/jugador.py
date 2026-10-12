from src.algebra.vector import Vector


class Jugador:
    # El estado se guarda como TEXTO en `self.estado`.
    # El renderizador lo lee para saber que animacion mostrar.
    #
    # Los nombres de los estados se definen AQUI como constantes
    # de clase. main.py puede importarlos para construir el
    # diccionario de animaciones.
    #
    # El hitbox es un circulo de radio `radio`, centrado SIEMPRE
    # en `posicion`. No hay offset.

    # --- Nombres de estados (fuente de verdad) ---
    ESTADO_QUIETO           = "quieto"
    ESTADO_MOVIMIENTO       = "movimiento"
    ESTADO_ASCIENDE         = "asciende"
    ESTADO_DESCIENDE        = "desciende"
    ESTADO_ATAQUE_NORMAL    = "ataque_normal"
    ESTADO_ATAQUE_DISTANCIA = "ataque_distancia"
    ESTADO_RECIBE_DANO      = "recibe_dano"
    ESTADO_MUERE            = "muere"

    # Estados que bloquean el movimiento mientras se reproducen.
    ESTADOS_BLOQUEANTES = (
        ESTADO_ATAQUE_NORMAL,
        ESTADO_ATAQUE_DISTANCIA,
        ESTADO_RECIBE_DANO,
    )

    def __init__(self, posicion: Vector, radio: float,
                 velocidad_h: float,
                 gravedad: float,
                 salto: float,
                 vida_max: float,
                 ataque: float,
                 cooldown_golpe: float,
                 cooldown_disparo: float):
        # --- Fisica ---
        self.posicion = posicion
        self.velocidad = Vector(0, 0)
        self.radio = radio
        self.apoyado = False
        self.direccion_mirada = 1        # 1 derecha, -1 izquierda

        # --- Parametros de fisica ---
        self.velocidad_h = velocidad_h
        self.gravedad = gravedad
        self.salto = salto

        # --- Estado (texto, lo lee el renderizador) ---
        self.estado = Jugador.ESTADO_QUIETO

        # --- Combate ---
        self.vida_max = vida_max
        self.vida = vida_max
        self.ataque = ataque
        self.cooldown_golpe = cooldown_golpe
        self.tiempo_golpe = 0.0
        self.cooldown_disparo = cooldown_disparo
        self.tiempo_disparo = 0.0

        # Bandera: si ya salio el proyectil durante la animacion.
        self.proyectil_disparado = False

    # ---------- Ciclo de vida ----------

    def reiniciar(self, posicion: Vector):
        # Vuelve al estado inicial.
        self.posicion = posicion
        self.velocidad = Vector(0, 0)
        self.apoyado = False
        self.direccion_mirada = 1
        self.estado = Jugador.ESTADO_QUIETO
        self.vida = self.vida_max
        self.tiempo_golpe = 0.0
        self.tiempo_disparo = 0.0
        self.proyectil_disparado = False

    def actualizar(self, dt, input_jugador, plataformas):
        # Un frame completo de fisica + estado.
        # input_jugador: {"izq": bool, "der": bool,
        #                 "salto": bool, "disparo": bool}

        # --- Cooldowns ---
        self.tiempo_golpe = max(0.0, self.tiempo_golpe - dt)
        self.tiempo_disparo = max(0.0, self.tiempo_disparo - dt)

        # --- Si esta muerto, solo reproduce "muere" ---
        if not self.esta_vivo():
            self.estado = Jugador.ESTADO_MUERE
            return

        # --- Si esta en animacion de ataque, no se mueve ---
        if self.estado in Jugador.ESTADOS_BLOQUEANTES:
            return

        # --- Input horizontal ---
        vx = 0.0
        if input_jugador.get("izq", False):
            vx -= 1
        if input_jugador.get("der", False):
            vx += 1

        self.velocidad.x = vx * self.velocidad_h
        if vx > 0:
            self.direccion_mirada = 1
        elif vx < 0:
            self.direccion_mirada = -1

        # --- Gravedad ---
        self.velocidad.y += self.gravedad * dt

        # --- Salto ---
        if self.apoyado and input_jugador.get("salto", False):
            self.velocidad.y = -self.salto
            self.apoyado = False

        # --- Integrar posicion ---
        self.posicion = self.posicion + self.velocidad * dt

        # --- Colisiones con plataformas ---
        self._resolver_colisiones(plataformas)

        # --- Actualizar estado ---
        self._actualizar_estado()

    def _resolver_colisiones(self, plataformas):
        # Resuelve colisiones usando la POSICION (el hitbox esta
        # centrado en ella).
        self.apoyado = False
        for plat in plataformas:
            if not plat.colisiona(self.posicion, self.radio):
                continue
            proy = plat.punto_mas_cercano(self.posicion)
            diff = self.posicion - proy
            if diff.magnitud() < 1e-6:
                d = plat.normal()
            else:
                d = diff.normalizar()
            # Sacar al jugador fuera de la plataforma.
            self.posicion = self.posicion + d * (self.radio - diff.magnitud())
            # Anular componente de velocidad que entra en la plataforma.
            vn = self.velocidad.producto_punto(d)
            if vn < 0:
                self.velocidad = self.velocidad - d * vn
            if d.y < -0.5:
                self.apoyado = True

    def _actualizar_estado(self):
        # Elige el estado segun lo que esta pasando.
        if not self.esta_vivo():
            self.estado = Jugador.ESTADO_MUERE
        elif not self.apoyado:
            if self.velocidad.y < 0:
                self.estado = Jugador.ESTADO_ASCIENDE
            else:
                self.estado = Jugador.ESTADO_DESCIENDE
        elif abs(self.velocidad.x) > 1:
            self.estado = Jugador.ESTADO_MOVIMIENTO
        else:
            self.estado = Jugador.ESTADO_QUIETO

    # ---------- Animaciones ----------

    def terminar_animacion(self):
        # Vuelve a "quieto" si estaba en una animacion bloqueante
        # que ya termino. Lo llama main.py cuando el renderizador
        # dice que la animacion acabo.
        if self.estado in Jugador.ESTADOS_BLOQUEANTES:
            if self.esta_vivo():
                self.estado = Jugador.ESTADO_QUIETO
            else:
                self.estado = Jugador.ESTADO_MUERE

    # ---------- Combate ----------

    def esta_vivo(self) -> bool:
        return self.vida > 0

    def recibir_dano(self, cantidad: float):
        if not self.esta_vivo():
            return
        self.vida = max(0.0, self.vida - cantidad)
        if self.vida > 0:
            self.estado = Jugador.ESTADO_RECIBE_DANO
        else:
            self.estado = Jugador.ESTADO_MUERE

    def puede_golpear(self) -> bool:
        return self.tiempo_golpe <= 0.0 and self.esta_vivo()

    def golpear(self, otro):
        if not self.puede_golpear():
            return
        otro.recibir_dano(self.ataque)
        self.tiempo_golpe = self.cooldown_golpe
        self.estado = Jugador.ESTADO_ATAQUE_NORMAL

    def puede_disparar(self) -> bool:
        return self.tiempo_disparo <= 0.0 and self.esta_vivo()

    def disparar(self):
        # Cambia al estado de ataque a distancia.
        # El proyectil lo crea main.py cuando el renderizador
        # llega al frame correcto.
        if not self.puede_disparar():
            return
        self.estado = Jugador.ESTADO_ATAQUE_DISTANCIA
        self.tiempo_disparo = self.cooldown_disparo
        self.proyectil_disparado = False

    def crear_proyectil(self):
        # Devuelve los datos para que main.py cree el Proyectil.
        # Asi Jugador NO importa Proyectil (menos acoplamiento).
        offset = 40 * self.direccion_mirada
        origen = Vector(self.posicion.x + offset, self.posicion.y )
        direccion = Vector(self.direccion_mirada, 0)
        return origen, direccion

    # ---------- Colision con otro jugador ----------

    def colisiona_con(self, otro) -> bool:
        # Distancia entre posiciones <= suma de radios.
        d = (self.posicion - otro.posicion).magnitud()
        return d <= self.radio + otro.radio

    def resolver_choque(self, otro):
        # Separa a los dos usando las posiciones.
        diff = self.posicion - otro.posicion
        d = diff.magnitud()
        if d < 1e-6:
            return
        overlap = (self.radio + otro.radio) - d
        direccion = diff.normalizar()
        self.posicion = self.posicion + direccion * (overlap / 2)
        otro.posicion = otro.posicion - direccion * (overlap / 2)

    # ---------- Debug ----------

    def __repr__(self) -> str:
        return (f"Jugador(pos={self.posicion}, vel={self.velocidad}, "
                f"estado={self.estado}, vida={self.vida:.0f}/"
                f"{self.vida_max:.0f}, apoyado={self.apoyado})")