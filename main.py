import pygame
import sys
from src.algebra.vector import Vector
from src.algebra.base import Base2D

# ============================
# CONFIGURACIÓN
# ============================
WIDTH, HEIGHT = 1050, 600
PANEL_X = 800                      # aquí empieza el panel lateral
FPS = 60
VELOCIDAD_MOV = 300
TAMANO_JUGADOR = 50

pygame.init()
pantalla = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Grupo I - Ejemplos y Contraejemplos")
reloj = pygame.time.Clock()
fuente = pygame.font.SysFont("Arial", 18)
fuente_peq = pygame.font.SysFont("Arial", 14)
fuente_tit = pygame.font.SysFont("Arial", 16, bold=True)

# ============================
# ESTADO
# ============================
posicion = Vector(PANEL_X / 2, HEIGHT / 2)
velocidad = Vector(0, 0)

MODO_ROTADA = 1
MODO_NO_ORT = 2
MODO_LD = 3
MODO_INVERTIDA = 4

modo_actual = MODO_ROTADA
modo_anterior = None
base_actual = Base2D(Vector(1, 0), Vector(0, 1))


def nombre_modo(m):
    return {
        MODO_ROTADA:    "1. Base ortonormal rotada",
        MODO_NO_ORT:    "2. Base NO ortogonal",
        MODO_LD:        "3. Base LD (NO es base)",
        MODO_INVERTIDA: "4. Base ortonormal invertida",
    }[m]


def descripcion_modo(m):
    return {
        MODO_ROTADA: [
            "La base gira con el movimiento.",
            "El cuadrado NO se deforma.",
            "Base VALIDA y ORTOGONAL.",
        ],
        MODO_NO_ORT: [
            "v1 y v2 NO son perpendiculares.",
            "<v1,v2> != 0.",
            "El cuadrado se deforma en",
            "un paralelogramo. Sigue siendo",
            "base porque det != 0.",
        ],
        MODO_LD: [
            "v1 y v2 son PARALELOS.",
            "det(B) = 0  =>  NO es base.",
            "El cuadrado COLAPSA a una",
            "linea. Se pierde un grado",
            "de libertad en R^2.",
        ],
        MODO_INVERTIDA: [
            "Base ortonormal pero v2",
            "invertido respecto al eje Y.",
            "det(B) = -1  (reflexion).",
            "El cuadrado se espeja.",
        ],
    }[m]


# ============================
# BUCLE PRINCIPAL
# ============================
while True:
    dt = reloj.tick(FPS) / 1000.0

    # --- 1. EVENTOS ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_1:
                modo_actual = MODO_ROTADA
            elif evento.key == pygame.K_2:
                modo_actual = MODO_NO_ORT
            elif evento.key == pygame.K_3:
                modo_actual = MODO_LD
            elif evento.key == pygame.K_4:
                modo_actual = MODO_INVERTIDA
            elif evento.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    # --- 2. TECLADO (suma de vectores) ---
    teclas = pygame.key.get_pressed()
    velocidad = Vector(0, 0)

    if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
        velocidad = velocidad + Vector(-VELOCIDAD_MOV, 0)
    if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
        velocidad = velocidad + Vector(VELOCIDAD_MOV, 0)
    if teclas[pygame.K_UP] or teclas[pygame.K_w]:
        velocidad = velocidad + Vector(0, -VELOCIDAD_MOV)
    if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
        velocidad = velocidad + Vector(0, VELOCIDAD_MOV)

    # --- 3. ACTUALIZAR POSICIÓN ---
    posicion = posicion + velocidad * dt

    # --- 4. RECONSTRUIR BASE SEGÚN MODO ---
    # Solo se reconstruye cuando cambia el modo (para no spamear la consola
    # con el warning de LD en cada frame).
    if modo_actual != modo_anterior:
        if modo_actual == MODO_ROTADA:
            base_actual = Base2D(Vector(1, 0), Vector(0, 1))
        elif modo_actual == MODO_NO_ORT:
            base_actual = Base2D(Vector(1, 0), Vector(1, 1))
        elif modo_actual == MODO_LD:
            base_actual = Base2D(Vector(1, 1), Vector(2, 2))
        elif modo_actual == MODO_INVERTIDA:
            base_actual = Base2D(Vector(1, 0), Vector(0, -1))
        modo_anterior = modo_actual

    # En modo rotada, la base sigue la dirección de movimiento
    if modo_actual == MODO_ROTADA and velocidad.magnitud() > 0:
        v1 = velocidad.normalizar()
        v2 = Vector(-v1.y, v1.x)
        base_actual = Base2D(v1, v2)

    # --- 5. DIBUJAR ÁREA DEL JUEGO ---
    pygame.draw.rect(pantalla, (20, 20, 30), (0, 0, PANEL_X, HEIGHT))

    # Grid
    for x in range(0, PANEL_X, 50):
        pygame.draw.line(pantalla, (40, 40, 55), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, 50):
        pygame.draw.line(pantalla, (40, 40, 55), (0, y), (PANEL_X, y))

    # Ejes de la base (siempre dibujados, excepto si son degenerados)
    if base_actual.es_valida or modo_actual == MODO_LD:
        # v1 (rojo)
        fin_v1 = posicion + base_actual.v1 * 80
        pygame.draw.line(pantalla, (255, 100, 100),
                         (posicion.x, posicion.y),
                         (fin_v1.x, fin_v1.y), 3)
        # v2 (verde)
        fin_v2 = posicion + base_actual.v2 * 80
        pygame.draw.line(pantalla, (100, 255, 100),
                         (posicion.x, posicion.y),
                         (fin_v2.x, fin_v2.y), 3)

    # Cuadrado/paralelogramo/linea segun la base
    mitad = TAMANO_JUGADOR / 2
    esquinas_locales = [
        (-mitad, -mitad),
        ( mitad, -mitad),
        ( mitad,  mitad),
        (-mitad,  mitad),
    ]

    esquinas_mundo = []
    for cx, cy in esquinas_locales:
        # ¡Aquí está el cambio de base inverso!
        esquina = posicion + base_actual.reconstruir_desde_base(cx, cy)
        esquinas_mundo.append((esquina.x, esquina.y))

    # Color segun el modo
    color_cuadro = {
        MODO_ROTADA:    (0, 200, 255),   # azul
        MODO_NO_ORT:    (255, 180, 0),   # naranja
        MODO_LD:        (255, 60, 60),   # rojo (peligro)
        MODO_INVERTIDA: (180, 100, 255), # morado
    }[modo_actual]

    # El polígono se dibuja igual, aunque en LD será una línea
    pygame.draw.polygon(pantalla, color_cuadro, esquinas_mundo)
    pygame.draw.polygon(pantalla, (255, 255, 255), esquinas_mundo, 1)

    # Texto de control
    fuente_ctrl = pygame.font.SysFont("Arial", 16)
    t = fuente_ctrl.render("Mover con WASD | Cambiar modo con 1,2,3,4 | ESC para salir",
                           True, (150, 150, 150))
    pantalla.blit(t, (15, HEIGHT - 25))

    # --- 6. PANEL LATERAL ---
    pygame.draw.rect(pantalla, (30, 30, 45),
                     (PANEL_X, 0, WIDTH - PANEL_X, HEIGHT))
    pygame.draw.line(pantalla, (80, 80, 120),
                     (PANEL_X, 0), (PANEL_X, HEIGHT), 2)

    y = 15
    t = fuente_tit.render("GRUPO I - DEMO", True, (255, 220, 100))
    pantalla.blit(t, (PANEL_X + 15, y)); y += 28

    t = fuente_peq.render("Cambia de modo con 1, 2, 3, 4",
                          True, (150, 150, 150))
    pantalla.blit(t, (PANEL_X + 15, y)); y += 25

    # Nombre del modo
    t = fuente.render(nombre_modo(modo_actual), True, (100, 200, 255))
    pantalla.blit(t, (PANEL_X + 15, y)); y += 30

    # Datos de la base
    pygame.draw.line(pantalla, (80, 80, 120),
                     (PANEL_X + 15, y), (WIDTH - 15, y), 1)
    y += 10

    datos = [
        (f"v1 = ({base_actual.v1.x:.2f}, {base_actual.v1.y:.2f})", (220, 220, 220)),
        (f"v2 = ({base_actual.v2.x:.2f}, {base_actual.v2.y:.2f})", (220, 220, 220)),
        (f"<v1,v2> = {base_actual.v1.producto_punto(base_actual.v2):.2f}", (220, 220, 220)),
        (f"det(B)  = {base_actual.determinante():.2f}", (220, 220, 220)),
    ]
    for txt, col in datos:
        t = fuente_peq.render(txt, True, col)
        pantalla.blit(t, (PANEL_X + 15, y)); y += 22

    y += 8
    # Estado ortogonal
    es_ort = base_actual.es_conjunto_ortogonal()
    col_ort = (100, 255, 100) if es_ort else (255, 100, 100)
    t = fuente_peq.render(f"Ortogonal: {'SI' if es_ort else 'NO'}", True, col_ort)
    pantalla.blit(t, (PANEL_X + 15, y)); y += 22

    # Estado es base
    es_base = base_actual.es_valida
    col_base = (100, 255, 100) if es_base else (255, 100, 100)
    t = fuente_peq.render(f"Es base:   {'SI' if es_base else 'NO'}", True, col_base)
    pantalla.blit(t, (PANEL_X + 15, y)); y += 30

    # Descripción pedagógica
    pygame.draw.line(pantalla, (80, 80, 120),
                     (PANEL_X + 15, y), (WIDTH - 15, y), 1)
    y += 15

    t = fuente_tit.render("Explicacion:", True, (200, 200, 200))
    pantalla.blit(t, (PANEL_X + 15, y)); y += 25

    for linea in descripcion_modo(modo_actual):
        t = fuente_peq.render(linea, True, (180, 180, 180))
        pantalla.blit(t, (PANEL_X + 15, y)); y += 20

    pygame.display.flip()