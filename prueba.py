# prueba.py
import pygame
import math
import random
from src.algebra.vector import Vector
from src.algebra.base import Base2D

# Configuración
ANCHO, ALTO = 1100, 700
FPS = 60
ESCALA = 70.0

# Colores
COLOR_FONDO = (15, 10, 20)
COLOR_SUELO = (45, 35, 55)
COLOR_P1 = (207, 117, 43)    # Cobre
COLOR_P2 = (58, 186, 112)    # Verde
COLOR_TEXTO = (240, 235, 225)
COLOR_CHISPA = (250, 200, 60)

def lerp(a, b, t):
    return a + (b - a) * t

def dibujar_texto(pantalla, texto, x, y, color=COLOR_TEXTO, tamaño=24):
    f = pygame.font.SysFont("Courier New", tamaño, bold=True)
    sup = f.render(texto, True, color)
    pantalla.blit(sup, (x - sup.get_width()//2, y))

def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Prueba de Cinemáticas - Hit Stop y Cámara")
    reloj = pygame.time.Clock()

    # Estado del juego y la cámara
    estado = "normal" # "intro", "normal", "hit_stop", "ko"
    timer = 0.0
    
    # Variables de la cámara
    cam_angulo = 0.0
    cam_zoom = 1.0
    target_angulo = 0.0
    target_zoom = 1.0
    
    # Posiciones de los personajes
    p1_pos = Vector(-3, 0)
    p2_pos = Vector(3, 0)
    
    # Partículas para el Hit-Stop
    particulas = []

    def crear_particulas(pos):
        for _ in range(15):
            particulas.append({
                "pos": Vector(pos.x, pos.y),
                "vel": Vector(random.uniform(-3, 3), random.uniform(-3, 3)),
                "vida": 0.5
            })

    def a_pantalla(p):
        # 1. Traslación al centro de la pantalla
        p_rel = Vector(p.x, p.y)
        
        # 2. Rotación (Cambio de base)
        c, s = math.cos(cam_angulo), math.sin(cam_angulo)
        base_cam = Base2D(Vector(c, s), Vector(-s, c))
        p_rot = base_cam.cambiar_de_base(p_rel)
        
        # 3. Zoom y ajuste a Pygame
        return (int(ANCHO//2 + p_rot.x * ESCALA * cam_zoom),
                int(ALTO//2 - p_rot.y * ESCALA * cam_zoom))

    while True:
        dt_real = reloj.tick(FPS) / 1000.0
        dt = dt_real # dt que usaremos para las físicas
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); return
            
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r:
                    estado = "normal"
                    cam_angulo = 0; cam_zoom = 1
                    target_angulo = 0; target_zoom = 1
                    particulas.clear()
                elif e.key == pygame.K_1:
                    estado = "intro"
                    timer = 2.5
                elif e.key == pygame.K_2 and estado == "normal":
                    estado = "hit_stop"
                    timer = 0.08 # 80 milisegundos de congelamiento
                    crear_particulas(Vector(0, 0))
                elif e.key == pygame.K_3 and estado == "normal":
                    estado = "ko"
                    timer = 3.0
                    crear_particulas(p2_pos)

        # ==========================================
        # LÓGICA DE ESTADOS (CINEMÁTICAS)
        # ==========================================
        if estado == "intro":
            timer -= dt_real
            target_zoom = 0.6 # Empieza alejado
            cam_zoom = lerp(cam_zoom, target_zoom, 2.0 * dt_real)
            
            if timer <= 0:
                estado = "normal"
                target_zoom = 1.0
                
        elif estado == "hit_stop":
            timer -= dt_real
            target_zoom = 1.08 # Micro zoom
            cam_zoom = target_zoom # Salto instantáneo
            dt = 0 # ¡CONGELAMOS EL TIEMPO DE LAS FÍSICAS!
            
            if timer <= 0:
                estado = "normal"
                target_zoom = 1.0
                
        elif estado == "ko":
            timer -= dt_real
            dt = dt_real * 0.2 # CÁMARA LENTA (20% de velocidad)
            target_zoom = 1.6
            target_angulo = math.radians(-15)
            
            if timer <= 0:
                estado = "normal"
                target_zoom = 1.0
                target_angulo = 0.0

        # Interpolación suave de la cámara (solo si no es hit_stop)
        if estado != "hit_stop":
            cam_zoom = lerp(cam_zoom, target_zoom, 4.0 * dt_real)
            cam_angulo = lerp(cam_angulo, target_angulo, 4.0 * dt_real)

        # Actualizar partículas
        for p in particulas[:]:
            p["pos"] = p["pos"] + p["vel"] * dt
            p["vida"] -= dt_real
            if p["vida"] <= 0:
                particulas.remove(p)

        # ==========================================
        # DIBUJADO
        # ==========================================
        pantalla.fill(COLOR_FONDO)
        
        # Suelo
        pygame.draw.line(pantalla, COLOR_SUELO, a_pantalla(Vector(-10, -1.5)), a_pantalla(Vector(10, -1.5)), int(4 * cam_zoom))

        # Personajes
        pygame.draw.circle(pantalla, COLOR_P1, a_pantalla(p1_pos), int(0.5 * ESCALA * cam_zoom))
        pygame.draw.circle(pantalla, COLOR_P2, a_pantalla(p2_pos), int(0.5 * ESCALA * cam_zoom))

        # Partículas
        for p in particulas:
            pygame.draw.circle(pantalla, COLOR_CHISPA, a_pantalla(p["pos"]), int(4 * cam_zoom))

        # Textos según el estado
        if estado == "intro":
            if timer > 1.0:
                dibujar_texto(pantalla, "READY?", ANCHO//2, ALTO//2 - 100, COLOR_TEXTO, 60)
            else:
                dibujar_texto(pantalla, "FIGHT!", ANCHO//2, ALTO//2 - 100, COLOR_CHISPA, 60)
                
        elif estado == "ko":
            # Flash blanco al inicio del KO
            if timer > 2.8:
                flash = pygame.Surface((ANCHO, ALTO))
                flash.fill((255, 255, 255))
                flash.set_alpha(int((timer - 2.8) * 255 / 0.2))
                pantalla.blit(flash, (0, 0))
            
            dibujar_texto(pantalla, "K.O.", ANCHO//2, ALTO//2 - 50, (255, 50, 50), 80)
            dibujar_texto(pantalla, "Slow Motion + Rotación de Cámara", ANCHO//2, ALTO//2 + 40, COLOR_TEXTO, 20)

        elif estado == "hit_stop":
            dibujar_texto(pantalla, "HIT STOP (dt = 0)", ANCHO//2, 50, COLOR_CHISPA, 30)

        # Instrucciones
        dibujar_texto(pantalla, "[1] Intro   [2] Hit-Stop   [3] K.O.   [R] Reset", ANCHO//2, ALTO - 40, (150, 150, 150), 20)

        pygame.display.flip()

if __name__ == "__main__":
    main()