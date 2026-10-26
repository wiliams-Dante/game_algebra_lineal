# variables.py
# ======================================================
# CONFIGURACIÓN GLOBAL DEL PROYECTO
# ======================================================
# Único lugar para editar colores, tamaños y constantes.
# ======================================================

# --- Pantalla ---
ANCHO_BASE = 1280
ALTO_BASE  = 720
ESCALA_GLOBAL = 1.2
FPS = 60

ANCHO = int(ANCHO_BASE * ESCALA_GLOBAL)
ALTO  = int(ALTO_BASE * ESCALA_GLOBAL)
ESCALA = 70.0 * ESCALA_GLOBAL

# --- Límites del mapa ---
LIMITE_IZQ = -14.0
LIMITE_DER = 14.0

# --- Debug ---
DEBUG_HITBOX = False

# ======================================================
# PALETA DE COLORES (Temática: Bosque Carmesí y Fuego)
# ======================================================
# Eliminamos los tonos violetas/lavandas para quitar el "filtro".
# Ahora todo es cálido, rojizo y oscuro, combinando con tus sprites.
# ======================================================

# --- Fondos y Paneles ---
# ======================================================
# PALETA DE COLORES NEUTRA (Sin filtros superpuestos)
# ======================================================

# --- Fondos y Paneles (Neutros para que no tiñan la pantalla) ---
COLOR_01 = (0, 0, 0)        # Fondo de demos: Negro puro (adiós filtro)
COLOR_02 = (20, 20, 20)     # Panel lateral: Gris ultra oscuro
COLOR_03 = (60, 60, 60)     # Separadores, bordes de panel: Gris medio

# --- Textos (Blancos y grises para máxima legibilidad) ---
COLOR_08 = (255, 255, 255)  # Texto principal: Blanco puro
COLOR_09 = (150, 150, 150)  # Texto dim (secundario): Gris claro
COLOR_10 = (200, 200, 200)  # Texto teoría: Gris muy claro

# --- Ejes y Líneas Base ---
COLOR_04 = (40, 40, 40)     # Ejes X/Y: Gris oscuro (antes era violáceo)
COLOR_05 = (100, 100, 100)  # Líneas paralelas, rectas auxiliares: Gris
COLOR_06 = (130, 60, 80)    # Recta de v1 (Mantenemos su color)
COLOR_07 = (80, 150, 180)   # Recta de v2 (Mantenemos su azul)

# --- Colores de Elementos Matemáticos (Se mantienen vivos) ---
COLOR_11 = (255, 200, 60)   # Dorado/Amarillo (Títulos, sumas, etc.)
COLOR_12 = (255, 230, 180)  # Amarillo pálido (Normales)
COLOR_13 = (220, 90, 110)   # Carmesí (Modo, Z)
COLOR_14 = (200, 100, 150)  # Magenta (Inverso)
COLOR_15 = (240, 120, 130)  # Coral/Rojo (U, V1, P_A)
COLOR_16 = (58, 186, 112)   # Verde Esmeralda (OK, Éxito)
COLOR_17 = (85, 200, 155)   # Verde Menta (V, P_B)
COLOR_18 = (100, 220, 175)  # Verde medio
COLOR_19 = (215, 85, 100)   # Rojo Frambuesa (Error, Paredes, Plataformas)

# --- Extras ---
COLOR_20 = (160, 185, 230)
COLOR_21 = (200, 210, 240)
COLOR_22 = (30, 30, 30)
COLOR_23 = (255, 255, 255)
COLOR_24 = (60, 50, 10)
COLOR_25 = (0, 0, 0)

# --- Barras de vida del juego ---
COLOR_26 = (207, 117, 43)   # Barra P2 (Fuego/Cobre #cf752b)
COLOR_27 = (58, 186, 112)   # Barra P1 (Verde esmeralda)
# --- Colores exclusivos para el Bosque Encantado (Plataformas) ---
# --- Colores exclusivos para el Bosque Encantado (Plataformas de Madera) ---
# --- Colores exclusivos para el Bosque Encantado (Plataformas Rojas) ---
# --- Colores exclusivos para el Bosque Encantado (Plataformas Rojas) ---
# --- Colores exclusivos para el Bosque Encantado (Plataformas Rojas Suaves) ---
# --- Colores exclusivos para el Bosque Encantado (Plataformas Rojas Oscuras) ---
COLOR_28 = (90, 40, 50)      # Rojo oscuro arriba (Inicio del degradado)
COLOR_29 = (55, 20, 30)      # Granate profundo (Medio del degradado)
COLOR_30 = (25, 8, 15)       # Casi negro rojizo (Final del degradado)
COLOR_31 = (130, 60, 70)     # Rojo apagado para la línea del borde superior# ======================================================
SPRITE_FALLBACK = (200, 140, 200, 100)
PARTICULAS_COLORES = [COLOR_16, COLOR_15, COLOR_13, COLOR_11, COLOR_17]

# ======================================================
# DEMOS: LAYOUT
# ======================================================
DEMO_1_PANEL_BASE = 1000
DEMO_2_PANEL_BASE = 900
DEMO_3_PANEL_BASE = 800