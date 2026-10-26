# main.py
import pygame
import random
from src.algebra.vector import Vector
from src.entidades.jugador import Jugador
from src.entidades.plataforma import Plataforma
from src.entidades.proyectil import Proyectil
from src.render import graficos as G
from src.render import fondo as F
from src.render.sprites import Animador

from src.render.graficos import ANCHO, ALTO, ESCALA, FPS

# ==================================================
# CONFIGURACIÓN E IMPORTS DE COLORES
# ==================================================
from variables import (
    DEBUG_HITBOX, LIMITE_IZQ, LIMITE_DER,
    ANCHO, ALTO, ESCALA, FPS,
    COLOR_01,  # Fondo noche, sombra plataforma
    COLOR_02,  # Panel lateral, relleno barra
    COLOR_03,  # Borde de barra de vida
    COLOR_08,  # Texto principal
    COLOR_11,  # Dorado (Ganador Empate)
    COLOR_19,  # Rojo frambuesa (Hitbox de proyectiles en debug)
    COLOR_25,  # Overlay negro
    COLOR_26,  # Cobre / Fuego (P1, Efectos P1)
    COLOR_27,  # Verde Esmeralda (P2, Efectos P2)
    COLOR_28,  # Rojo oscuro (Arriba)
    COLOR_29,  # Granate profundo (Medio)
    COLOR_30,  # Casi negro rojizo (Abajo)
    COLOR_31,  # Borde superior
)

# ==================================================
# MAPA
# ==================================================
PLATAFORMAS = [
    Plataforma(Vector(-15.0, 9.5), Vector(1, 0), 30.0, 0.1),
    Plataforma(Vector(-13.0, 7.5), Vector(1, 0), 3.75, 0.1),
    Plataforma(Vector(-6.0, 7.5), Vector(1, 0), 3.75, 0.1),
    Plataforma(Vector(1.0, 7.5), Vector(1, 0), 3.75, 0.1),
    Plataforma(Vector(9.0, 7.5), Vector(1, 0), 3.75, 0.1),
    Plataforma(Vector(-10.0, 5.5), Vector(1, 0), 3.75, 0.1),
    Plataforma(Vector(-2.0, 5.5), Vector(1, 0), 3.75, 0.1),
    Plataforma(Vector(5.0, 5.5), Vector(1, 0), 3.75, 0.1),
    Plataforma(Vector(12.0, 5.5), Vector(1, 0), 3.75, 0.1),
    Plataforma(Vector(-13.0, 3.5), Vector(1, 0), 3.75, 0.1),
    Plataforma(Vector(-5.0, 3.5), Vector(1, 0), 3.75, 0.1),
    Plataforma(Vector(3.0, 3.5), Vector(1, 0), 3.75, 0.1),
    Plataforma(Vector(10.0, 3.5), Vector(1, 0), 3.75, 0.1),
    Plataforma(Vector(-11.0, 1.5), Vector(1, 0), 3.75, 0.1),
    Plataforma(Vector(-3.0, 1.5), Vector(1, 0), 3.75, 0.1),
    Plataforma(Vector(5.0, 1.5), Vector(1, 0), 3.75, 0.1),
    Plataforma(Vector(12.0, 1.5), Vector(1, 0), 3.75, 0.1),
    Plataforma(Vector(-9.0, -0.5), Vector(1, 0), 3.75, 0.1),
    Plataforma(Vector(-1.0, -0.5), Vector(1, 0), 3.75, 0.1),
    Plataforma(Vector(7.0, -0.5), Vector(1, 0), 3.75, 0.1),
]

# ==================================================
# SISTEMA DE CHISPAS
# ==================================================
class Chispa:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vel_x = random.uniform(-2.0, 2.0) * G.ESCALA_GLOBAL
        self.vel_y = random.uniform(-3.0, 1.0) * G.ESCALA_GLOBAL
        self.vida_max = random.uniform(1.0, 2.0)
        self.vida = self.vida_max
        self.color = color
        self.tamaño = random.randint(2, 3)

    def actualizar(self, dt):
        self.x += self.vel_x * dt * 60
        self.y += self.vel_y * dt * 60
        self.vida -= dt

    def dibujar(self, pantalla):
        if self.vida > 0:
            alpha = int(max(0, self.vida / self.vida_max) * 255)
            glow_alpha = int(alpha * 0.25)
            glow_size = self.tamaño * 3
            surf_glow = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
            pygame.draw.circle(surf_glow, (*self.color, glow_alpha), (glow_size, glow_size), glow_size)
            pantalla.blit(surf_glow, (self.x - glow_size, self.y - glow_size))

            surf = pygame.Surface((self.tamaño * 2, self.tamaño * 2), pygame.SRCALPHA)
            pygame.draw.circle(surf, (*self.color, alpha), (self.tamaño, self.tamaño), self.tamaño)
            pantalla.blit(surf, (self.x - self.tamaño, self.y - self.tamaño))

chispas = []

def crear_explosion(pos_px, color):
    for _ in range(12): 
        chispas.append(Chispa(pos_px[0], pos_px[1], color))

# ==================================================
# FUNCIONES AUXILIARES
# ==================================================
def crear_jugador(x, y):
    return Jugador(posicion=Vector(x, y), radio=0.40, velocidad_h=6.0,
                   gravedad=25.0, salto=10.0, vida_max=100.0,
                   ataque=10.0, cooldown_golpe=0.4, cooldown_disparo=0.8)

def leer_input(teclas, izq, der, salto, disparo):
    return {"izq": teclas[izq], "der": teclas[der], "salto": teclas[salto], "disparo": teclas[disparo]}

def dibujar_plataformas(win):
    for plat in PLATAFORMAS:
        p1_px = G.a_pantalla(Vector(plat.origen.x, -plat.origen.y))
        p2_px = G.a_pantalla(Vector(plat.extremo_final().x, -plat.extremo_final().y))
        grosor_px = int(plat.grosor * ESCALA)
        x_rect = min(p1_px[0], p2_px[0])
        y_rect = p1_px[1]
        ancho_rect = abs(p2_px[0] - p1_px[0])
        radio = max(1, int(4 * G.ESCALA_GLOBAL))

        # 1. Sombra (Casi negro)
        color_sombra = G.oscurecer(COLOR_30, 0.5)
        pygame.draw.rect(win.pantalla, color_sombra,
                         (x_rect, y_rect + grosor_px, ancho_rect, max(2, int(3 * G.ESCALA_GLOBAL))),
                         border_radius=radio)
        
        # 2. Degradado de 3 colores (Línea por línea)
        if ancho_rect > 0 and grosor_px > 0:
            grad_surf = pygame.Surface((ancho_rect, grosor_px), pygame.SRCALPHA)
            
            for y in range(grosor_px):
                t = y / grosor_px 
                
                if t < 0.5:
                    t_local = t * 2.0
                    r = int(COLOR_28[0] * (1 - t_local) + COLOR_29[0] * t_local)
                    g = int(COLOR_28[1] * (1 - t_local) + COLOR_29[1] * t_local)
                    b = int(COLOR_28[2] * (1 - t_local) + COLOR_29[2] * t_local)
                else:
                    t_local = (t - 0.5) * 2.0
                    r = int(COLOR_29[0] * (1 - t_local) + COLOR_30[0] * t_local)
                    g = int(COLOR_29[1] * (1 - t_local) + COLOR_30[1] * t_local)
                    b = int(COLOR_29[2] * (1 - t_local) + COLOR_30[2] * t_local)
                    
                pygame.draw.line(grad_surf, (r, g, b), (0, y), (ancho_rect, y))

            mask_surf = pygame.Surface((ancho_rect, grosor_px), pygame.SRCALPHA)
            pygame.draw.rect(mask_surf, (255, 255, 255, 255), (0, 0, ancho_rect, grosor_px), border_radius=radio)
            grad_surf.blit(mask_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

            win.pantalla.blit(grad_surf, (x_rect, y_rect))
        
        # 3. Borde superior mágico
        if ancho_rect > radio * 2:
            pygame.draw.line(win.pantalla, COLOR_31,
                             (x_rect + radio, y_rect), (x_rect + ancho_rect - radio, y_rect),
                             max(2, int(2 * G.ESCALA_GLOBAL)))

def dibujar_proyectiles(win, proyectiles):
    for proj in proyectiles:
        pos_px = G.a_pantalla(Vector(proj.posicion.x, -proj.posicion.y))
        img = proj.sprite
        if proj.mirando_izq: img = pygame.transform.flip(img, True, False)

        glow = pygame.transform.scale(img, (int(img.get_width() * 1.25), int(img.get_height() * 1.25)))
        glow.set_alpha(50)
        win.pantalla.blit(glow, glow.get_rect(center=pos_px))
        win.pantalla.blit(img, img.get_rect(center=pos_px))

# ==================================================
# DIBUJO DEL JUEGO
# ==================================================
def dibujar_juego(win, camara_x, camara_y, particulas, capas_fondo, p1, p2, animador_p1, animador_p2, proyectiles, dt, shake_mag):
    if shake_mag > 0:
        offset_x = random.uniform(-shake_mag, shake_mag) * G.ESCALA_GLOBAL
        offset_y = random.uniform(-shake_mag, shake_mag) * G.ESCALA_GLOBAL
    else:
        offset_x, offset_y = 0, 0

    G.configurar_camara(Vector(camara_x + offset_x, -camara_y + offset_y))

    F.dibujar_fondo(win.pantalla, camara_x, particulas, capas_fondo, ESCALA, ANCHO, ALTO, dt)
    dibujar_plataformas(win)
    dibujar_proyectiles(win, proyectiles)

    animador_p1.dibujar(win.pantalla, G.a_pantalla(Vector(p1.posicion.x, -p1.posicion.y)), p1.direccion_mirada)
    animador_p2.dibujar(win.pantalla, G.a_pantalla(Vector(p2.posicion.x, -p2.posicion.y)), p2.direccion_mirada)

    if DEBUG_HITBOX:
        # Hitbox P1 (Cobre)
        pygame.draw.circle(win.pantalla, COLOR_26, G.a_pantalla(Vector(p1.posicion.x, -p1.posicion.y)), int(p1.radio * ESCALA), 2)
        # Hitbox P2 (Verde)
        pygame.draw.circle(win.pantalla, COLOR_27, G.a_pantalla(Vector(p2.posicion.x, -p2.posicion.y)), int(p2.radio * ESCALA), 2)
        # Hitbox Proyectiles (Rojo)
        for proj in proyectiles:
            pygame.draw.circle(win.pantalla, COLOR_19, G.a_pantalla(Vector(proj.posicion.x, -proj.posicion.y)), int(proj.radio * ESCALA), 2)

# ==================================================
# BARRA DE VIDA (SOLO CAPA 1)
# ==================================================
def dibujar_barra_glass(win, x, y, ancho, alto, porc, color_mid, es_p2=False):
    radio = max(3, alto // 2)
    pygame.draw.rect(win.pantalla, COLOR_02, (x, y, ancho, alto), border_radius=radio)

    if porc <= 0:
        pygame.draw.rect(win.pantalla, COLOR_03, (x, y, ancho, alto), 2, border_radius=radio)
        return

    ancho_actual = max(radio * 2, int(ancho * porc))
    x_rect = (x + ancho - ancho_actual) if es_p2 else x

    glow_color = tuple(min(255, int(c * 1.3)) for c in color_mid)
    glow_surf = pygame.Surface((ancho_actual + 8, alto + 8), pygame.SRCALPHA)
    pygame.draw.rect(glow_surf, (*glow_color, 45), (0, 0, ancho_actual + 8, alto + 8), border_radius=radio + 4)
    win.pantalla.blit(glow_surf, (x_rect - 4, y - 4))

    pygame.draw.rect(win.pantalla, color_mid, (x_rect, y, ancho_actual, alto), border_radius=radio)
    pygame.draw.rect(win.pantalla, COLOR_03, (x_rect, y, ancho_actual, alto), 2, border_radius=radio)

# ==================================================
# DIBUJO DEL HUD
# ==================================================
def dibujar_hud(win, p1, p2, vidas_p1, vidas_p2, ganador, vida_vis_p1, vida_vis_p2):
    ancho_barra = int(350 * G.ESCALA_GLOBAL)
    alto_barra = int(20 * G.ESCALA_GLOBAL)
    y_barra = int(20 * G.ESCALA_GLOBAL)

    f_ui = G.fuente(18, bold=True)
    t = pygame.time.get_ticks() / 1000.0

    # P1 (Cobre / Fuego) - izquierda
    p1_x = int(20 * G.ESCALA_GLOBAL)
    porc_p1 = max(0.0, vida_vis_p1 / p1.vida_max)
    dibujar_barra_glass(win, p1_x, y_barra, ancho_barra, alto_barra, porc_p1, COLOR_26, es_p2=False)

    txt_vidas_p1 = f_ui.render(f" Vidas: {vidas_p1}", True, G.brillo(COLOR_26, 1.15))
    win.pantalla.blit(txt_vidas_p1, (p1_x + 5, y_barra + alto_barra + 8))

    # P2 (Verde Esmeralda) - derecha
    p2_x = ANCHO - ancho_barra - int(20 * G.ESCALA_GLOBAL)
    porc_p2 = max(0.0, vida_vis_p2 / p2.vida_max)
    dibujar_barra_glass(win, p2_x, y_barra, ancho_barra, alto_barra, porc_p2, COLOR_27, es_p2=True)

    txt_vidas_p2 = f_ui.render(f" Vidas: {vidas_p2}", True, G.brillo(COLOR_27, 1.15))
    win.pantalla.blit(txt_vidas_p2, (p2_x + ancho_barra - txt_vidas_p2.get_width() - 5, y_barra + alto_barra + 8))

    # Pantalla de victoria
    if ganador is not None:
        s_vic = pygame.Surface((ANCHO, ALTO))
        s_vic.set_alpha(180); s_vic.fill(COLOR_25)
        win.pantalla.blit(s_vic, (0, 0))

        # Elegimos el color según quién haya ganado
        if ganador == "JUGADOR 1":
            color_base = COLOR_26  # Cobre / Fuego
        elif ganador == "JUGADOR 2":
            color_base = COLOR_27  # Verde Esmeralda
        else:
            color_base = COLOR_11  # Dorado (para empates)

        color_ganador = G.pulso(color_base, t, 0.10, 1.8) 
        
        f_big = G.fuente(70, bold=True)
        txt_ganador = f_big.render(f"¡{ganador} GANA!", True, color_ganador)
        win.pantalla.blit(txt_ganador, txt_ganador.get_rect(center=(ANCHO // 2, ALTO // 2 - 30)))

        f_sub = G.fuente(28)
        txt_sub = f_sub.render("Presiona R para jugar de nuevo | ESC para salir", True, COLOR_08)
        win.pantalla.blit(txt_sub, txt_sub.get_rect(center=(ANCHO // 2, ALTO // 2 + 50)))

# ==================================================
# JUEGO PRINCIPAL
# ==================================================
def main():
    global DEBUG_HITBOX
    win = G.Ventana("Álgebra Lineal en Videojuegos", ANCHO, ALTO, ANCHO, ESCALA, FPS)

    try:
        pygame.mixer.init()
        pygame.mixer.music.load("assets/audio/fondo_audio.mp3")
        pygame.mixer.music.set_volume(0.7)
        pygame.mixer.music.play(-1)
    except: pass

    capas_fondo = F.cargar_capas_fondo(ANCHO, ALTO)

    tamano_laser = (int(100 * G.ESCALA_GLOBAL), int(60 * G.ESCALA_GLOBAL))
    tamano_sprite = (int(120 * G.ESCALA_GLOBAL), int(120 * G.ESCALA_GLOBAL))

    try:
        laser_p1_img = pygame.transform.scale(pygame.image.load("assets/images/sprites_jugador_1/ataque_distancia/laser.png").convert_alpha(), tamano_laser)
    except: laser_p1_img = pygame.Surface(tamano_laser)
    try:
        laser_p2_img = pygame.transform.scale(pygame.image.load("assets/images/sprites_jugador_2/ataque_distancia/laser.png").convert_alpha(), tamano_laser)
    except: laser_p2_img = pygame.Surface(tamano_laser)

    p1, p2 = crear_jugador(-4.0, 4.0), crear_jugador(4.0, 4.0)

    animador_p1 = Animador("assets/images/sprites_jugador_1", fps_animacion=12, tamaño=tamano_sprite)
    animador_p2 = Animador("assets/images/sprites_jugador_2", fps_animacion=12, tamaño=tamano_sprite)

    proyectiles = []
    chispas.clear()
    particulas = F.crear_particulas(ANCHO, ALTO, cantidad=35)

    camara_x, camara_y = 0.0, 0.0
    vidas_p1, vidas_p2 = 3, 3
    ganador = None
    timer_respawn_p1, timer_respawn_p2 = 0.0, 0.0

    shake_mag = 0.0
    vida_vis_p1, vida_vis_p2 = p1.vida, p2.vida

    while True:
        dt, teclas, eventos = win.empezar_frame()

        if shake_mag > 0:
            shake_mag = max(0, shake_mag - 2.0 * dt)

        for e in eventos:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_h: DEBUG_HITBOX = not DEBUG_HITBOX
                if e.key == pygame.K_r:
                    p1.reiniciar(Vector(-4.0, 4.0)); p2.reiniciar(Vector(4.0, 4.0))
                    proyectiles.clear(); vidas_p1, vidas_p2 = 3, 3
                    ganador = None; timer_respawn_p1, timer_respawn_p2 = 0.0, 0.0
                    shake_mag = 0.0
                    vida_vis_p1, vida_vis_p2 = p1.vida, p2.vida
                    chispas.clear()

                if ganador is None:
                    # P1 Ataca (P2 recibe daño -> Explosión Verde de P2)
                    if e.key == pygame.K_f and p1.puede_golpear() and p1.estado not in Jugador.ESTADOS_BLOQUEANTES:
                        animador_p1.reiniciar()
                        if p1.golpear(p2):
                            animador_p2.reiniciar()
                            shake_mag = 0.5
                            crear_explosion(G.a_pantalla(Vector(p2.posicion.x, -p2.posicion.y)), COLOR_27)

                    # P2 Ataca (P1 recibe daño -> Explosión Cobre de P1)
                    if e.key == pygame.K_MINUS and p2.puede_golpear() and p2.estado not in Jugador.ESTADOS_BLOQUEANTES:
                        animador_p2.reiniciar()
                        if p2.golpear(p1):
                            animador_p1.reiniciar()
                            shake_mag = 0.5
                            crear_explosion(G.a_pantalla(Vector(p1.posicion.x, -p1.posicion.y)), COLOR_26)

        if ganador is None:
            p1.actualizar(dt, leer_input(teclas, pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_g), PLATAFORMAS)
            p2.actualizar(dt, leer_input(teclas, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_PERIOD), PLATAFORMAS)

            p1.posicion.x = G.clamp(p1.posicion.x, LIMITE_IZQ, LIMITE_DER)
            p2.posicion.x = G.clamp(p2.posicion.x, LIMITE_IZQ, LIMITE_DER)
            if p1.colisiona_con(p2): p1.resolver_choque(p2)

            if teclas[pygame.K_g] and p1.puede_disparar() and p1.estado not in Jugador.ESTADOS_BLOQUEANTES:
                p1.disparar(); animador_p1.reiniciar()
            if teclas[pygame.K_PERIOD] and p2.puede_disparar() and p2.estado not in Jugador.ESTADOS_BLOQUEANTES:
                p2.disparar(); animador_p2.reiniciar()

            for p, anim, laser_img in [
                (p1, animador_p1, laser_p1_img), 
                (p2, animador_p2, laser_p2_img)
            ]:
                if p.estado == Jugador.ESTADO_ATAQUE_DISTANCIA and not p.proyectil_disparado:
                    if anim.indice_frame >= 5:
                        origen, direccion = p.crear_proyectil()
                        nuevo_proyectil = Proyectil(origen, direccion, dano=20.0, velocidad=12.0, radio=0.37, tiempo_vida=4.0)
                        nuevo_proyectil.sprite = laser_img
                        nuevo_proyectil.mirando_izq = (p.direccion_mirada < 0)
                        proyectiles.append(nuevo_proyectil)
                        p.proyectil_disparado = True

            for proj in proyectiles[:]:
                proj.actualizar(dt)
                if not proj.vivo: proyectiles.remove(proj); continue
                
                # Si el proyectil golpea a P1, explota en Cobre (color de P1)
                if proj.colisiona_con(p1):
                    p1.recibir_dano(proj.dano); animador_p1.reiniciar(); proyectiles.remove(proj)
                    shake_mag = 0.3
                    crear_explosion(G.a_pantalla(Vector(p1.posicion.x, -p1.posicion.y)), COLOR_26)
                
                # Si el proyectil golpea a P2, explota en Verde (color de P2)
                elif proj.colisiona_con(p2):
                    p2.recibir_dano(proj.dano); animador_p2.reiniciar(); proyectiles.remove(proj)
                    shake_mag = 0.3
                    crear_explosion(G.a_pantalla(Vector(p2.posicion.x, -p2.posicion.y)), COLOR_27)

            animador_p1.actualizar(dt, p1.estado); animador_p2.actualizar(dt, p2.estado)

            if animador_p1.ha_terminado() and p1.estado in Jugador.ESTADOS_BLOQUEANTES: p1.estado = Jugador.ESTADO_QUIETO
            if animador_p2.ha_terminado() and p2.estado in Jugador.ESTADOS_BLOQUEANTES: p2.estado = Jugador.ESTADO_QUIETO

            if not p1.esta_vivo() and timer_respawn_p1 <= 0: vidas_p1 -= 1; timer_respawn_p1 = 1.5
            if timer_respawn_p1 > 0:
                timer_respawn_p1 -= dt
                if timer_respawn_p1 <= 0:
                    if vidas_p1 > 0: p1.reiniciar(Vector(-4.0, 4.0))
                    else: ganador = "JUGADOR 2"

            if not p2.esta_vivo() and timer_respawn_p2 <= 0: vidas_p2 -= 1; timer_respawn_p2 = 1.5
            if timer_respawn_p2 > 0:
                timer_respawn_p2 -= dt
                if timer_respawn_p2 <= 0:
                    if vidas_p2 > 0: p2.reiniciar(Vector(4.0, 4.0))
                    else: ganador = "JUGADOR 1"

            if vidas_p1 <= 0 and vidas_p2 <= 0: ganador = "EMPATE"

        vida_vis_p1 += (p1.vida - vida_vis_p1) * 5.0 * dt
        vida_vis_p2 += (p2.vida - vida_vis_p2) * 5.0 * dt

        objetivo_x = (p1.posicion.x + p2.posicion.x) * 0.5
        objetivo_y = (p1.posicion.y + p2.posicion.y) * 0.5
        camara_x += (objetivo_x - camara_x) * 3.0 * dt
        camara_y += (objetivo_y - camara_y) * 3.0 * dt
        camara_x = G.clamp(camara_x, -10.0, 10.0)
        camara_y = G.clamp(camara_y, -8.0, 5.0)

        dibujar_juego(win, camara_x, camara_y, particulas, capas_fondo, p1, p2, animador_p1, animador_p2, proyectiles, dt, shake_mag)

        for chispa in chispas[:]:
            chispa.actualizar(dt)
            chispa.dibujar(win.pantalla)
            if chispa.vida <= 0:
                chispas.remove(chispa)

        dibujar_hud(win, p1, p2, vidas_p1, vidas_p2, ganador, vida_vis_p1, vida_vis_p2)
        win.terminar_frame()

if __name__ == "__main__":
    main()