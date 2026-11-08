# src/entidades/jugador.py
from src.algebra.vector import Vector, EPSILON
from src.algebra.base import Base2D
class Jugador:
    ESTADO_QUIETO           = "quieto"
    ESTADO_MOVIMIENTO       = "movimiento"
    ESTADO_ASCIENDE         = "asciende"
    ESTADO_DESCIENDE        = "desciende"
    ESTADO_ATAQUE_NORMAL    = "ataque_normal"
    ESTADO_ATAQUE_DISTANCIA = "ataque_distancia"
    ESTADO_RECIBE_DANO      = "recibe_dano"
    ESTADO_MUERE            = "muere"

    ESTADOS_BLOQUEANTES = (ESTADO_ATAQUE_NORMAL, ESTADO_ATAQUE_DISTANCIA)
    DURACION_HITSTUN = 0.35

    def __init__(self, posicion: Vector, radio: float, velocidad_h: float,
                 gravedad: float, salto: float, vida_max: float,
                 ataque: float, cooldown_golpe: float, cooldown_disparo: float):
        self.posicion = posicion
        self.velocidad = Vector(0, 0)
        self.radio = radio
        self.apoyado = False
        self.direccion_mirada = 1
        self.velocidad_h = velocidad_h
        self.gravedad = gravedad
        self.salto = salto
        self.estado = Jugador.ESTADO_QUIETO
        self.vida_max = vida_max
        self.vida = vida_max
        self.ataque = ataque
        self.cooldown_golpe = cooldown_golpe
        self.tiempo_golpe = 0.0
        self.cooldown_disparo = cooldown_disparo
        self.tiempo_disparo = 0.0
        self.tiempo_hitstun = 0.0
        self.proyectil_disparado = False

    def reiniciar(self, posicion: Vector):
        self.posicion = posicion
        self.velocidad = Vector(0, 0)
        self.apoyado = False
        self.direccion_mirada = 1
        self.estado = Jugador.ESTADO_QUIETO
        self.vida = self.vida_max
        self.tiempo_golpe = 0.0
        self.tiempo_disparo = 0.0
        self.tiempo_hitstun = 0.0
        self.proyectil_disparado = False

    def actualizar(self, dt, input_jugador, plataformas):
        self.tiempo_golpe = max(0.0, self.tiempo_golpe - dt)
        self.tiempo_disparo = max(0.0, self.tiempo_disparo - dt)
        self.tiempo_hitstun = max(0.0, self.tiempo_hitstun - dt)

        if not self.esta_vivo():
            self.estado = Jugador.ESTADO_MUERE
            return

        if self.tiempo_hitstun > 0:
            self.velocidad.x = 0
            self.velocidad.y += self.gravedad * dt
            self.posicion = self.posicion + self.velocidad * dt
            self._resolver_colisiones(plataformas)
            self.estado = Jugador.ESTADO_RECIBE_DANO
            return

        if self.estado == Jugador.ESTADO_RECIBE_DANO:
            self.estado = Jugador.ESTADO_QUIETO

        if self.estado in Jugador.ESTADOS_BLOQUEANTES:
            self.velocidad.y += self.gravedad * dt
            self.posicion = self.posicion + self.velocidad * dt
            self._resolver_colisiones(plataformas)
            if self.apoyado:
                self.velocidad.x = 0
            return
        
        vx = 0.0
        if input_jugador.get("izq", False): vx -= 1
        if input_jugador.get("der", False): vx += 1

        self.velocidad.x = vx * self.velocidad_h
        if vx > 0: self.direccion_mirada = 1
        elif vx < 0: self.direccion_mirada = -1

        self.velocidad.y += self.gravedad * dt

        if self.apoyado and input_jugador.get("salto", False):
            self.velocidad.y = -self.salto
            self.apoyado = False

        self.posicion = self.posicion + self.velocidad * dt
        self._resolver_colisiones(plataformas)
        self._actualizar_estado()

    def _resolver_colisiones(self, plataformas):
        self.apoyado = False
        for plat in plataformas:
            if not plat.colisiona(self.posicion, self.radio): continue
            proy = plat.punto_mas_cercano(self.posicion)
            diff = self.posicion - proy
            dist = diff.magnitud()

            if dist < 1e-6:
                d = plat.normal()
                if self.velocidad.producto_punto(d) > 0: d = d * (-1.0)
                penetracion = self.radio
            else:
                d = diff.normalizar()

                # ─── FIX DEL BUG ───────────────────────────────
                # Si el jugador está cayendo (velocidad apunta hacia
                # la plataforma), lo empujamos en la dirección de la
                # normal (hacia arriba) en lugar de seguir el diff
                # (que apuntaría hacia abajo y lo mandaría al vacío).
                n = plat.normal()
                if self.velocidad.producto_punto(n) < 0:
                    d = d + n
                    if d.magnitud() > 1e-6:
                        d = d.normalizar()
                    else:
                        d = n
                # ─── FIN DEL FIX ──────────────────────────────

                penetracion = self.radio - dist

            self.posicion = self.posicion + d * penetracion

            # (el resto queda igual)
            base_colision = Base2D(plat.direccion, d)
            if base_colision.es_valida:
                vel_local = base_colision.cambiar_de_base(self.velocidad)
                if vel_local.y < 0:
                    vel_local.y = 0
                self.velocidad = base_colision.reconstruir_desde_base(vel_local.x, vel_local.y)
            else:
                vn = self.velocidad.producto_punto(d)
                if vn < 0:
                    self.velocidad = self.velocidad - d * vn

            if d.y < -0.5:
                self.apoyado = True  
                   
    def _actualizar_estado(self):
        if not self.esta_vivo(): self.estado = Jugador.ESTADO_MUERE
        elif not self.apoyado:
            self.estado = Jugador.ESTADO_ASCIENDE if self.velocidad.y < 0 else Jugador.ESTADO_DESCIENDE
        elif abs(self.velocidad.x) > EPSILON: self.estado = Jugador.ESTADO_MOVIMIENTO
        else: self.estado = Jugador.ESTADO_QUIETO

    def terminar_animacion(self):
        if self.tiempo_hitstun > 0: return
        if self.estado in Jugador.ESTADOS_BLOQUEANTES:
            if self.esta_vivo(): self.estado = Jugador.ESTADO_QUIETO
            else: self.estado = Jugador.ESTADO_MUERE

    def esta_vivo(self) -> bool:
        return self.vida > 0

    def recibir_dano(self, cantidad: float):
        if not self.esta_vivo(): return
        self.vida = max(0.0, self.vida - cantidad)
        if self.vida > 0:
            self.estado = Jugador.ESTADO_RECIBE_DANO
            self.tiempo_hitstun = Jugador.DURACION_HITSTUN
        else:
            self.estado = Jugador.ESTADO_MUERE
            self.tiempo_hitstun = 0.0

    def puede_golpear(self) -> bool:
        return self.tiempo_golpe <= 0.0 and self.esta_vivo()

    def golpear(self, otro) -> bool:
        """Intenta golpear a otro jugador. Retorna True si conectó."""
        if not self.puede_golpear(): return False
        
        self.tiempo_golpe = self.cooldown_golpe
        self.estado = Jugador.ESTADO_ATAQUE_NORMAL
        
        d = otro.posicion - self.posicion
        mirada = Vector(self.direccion_mirada, 0)
        alcance = self.radio + otro.radio + 0.5
        
        if d.magnitud() <= alcance and d.producto_punto(mirada) > 0:
            otro.recibir_dano(self.ataque)
            return True
        return False

    def puede_disparar(self) -> bool:
        return self.tiempo_disparo <= 0.0 and self.esta_vivo()

    def disparar(self):
        if not self.puede_disparar(): return
        self.estado = Jugador.ESTADO_ATAQUE_DISTANCIA
        self.tiempo_disparo = self.cooldown_disparo
        self.proyectil_disparado = False

    def crear_proyectil(self):
        offset = 0.70 * self.direccion_mirada
        origen = Vector(self.posicion.x + offset, self.posicion.y)
        direccion = Vector(self.direccion_mirada, 0)
        return origen, direccion

    def colisiona_con(self, otro) -> bool:
        return (self.posicion - otro.posicion).magnitud() <= self.radio + otro.radio

    def resolver_choque(self, otro):
        diff = self.posicion - otro.posicion
        d = diff.magnitud()
        if d < 1e-6: return
        overlap = (self.radio + otro.radio) - d
        direccion = diff.normalizar()
        self.posicion = self.posicion + direccion * (overlap / 2)
        otro.posicion = otro.posicion - direccion * (overlap / 2)

    def __repr__(self) -> str:
        return (f"Jugador(pos={self.posicion}, vel={self.velocidad}, "
                f"estado={self.estado}, vida={self.vida:.0f}/"
                f"{self.vida_max:.0f}, apoyado={self.apoyado}, "
                f"hitstun={self.tiempo_hitstun:.2f})")