# ==================================================
# ESCALA GLOBAL
# ==================================================
# Todo lo que sea tamano de pantalla, sprite o velocidad
# se multiplica por ESCALA. Cambiar este valor escala el juego.
ESCALA = 1

# ==================================================
# RUTAS DE ASSETS
# ==================================================
# Fondo del area de juego.
RUTA_FONDO = "assets/images/sprites_fondo/fondo.jpg"

# Carpetas de sprites de los jugadores.
CARPETA_SPRITES_P1 = "assets/images/sprites_jugador_1"
CARPETA_SPRITES_P2 = "assets/images/sprites_jugador_2"

# Subcarpetas de animaciones (mismas para ambos jugadores).
ANIM_QUIETO           = "quieto"
ANIM_MOVIMIENTO       = "movimiento"
ANIM_ATAQUE_NORMAL    = "ataque_normal"
ANIM_ATAQUE_DISTANCIA = "ataque_distancia"
ANIM_ASCIENDE         = "asciende"
ANIM_DESCIENDE        = "desciende"
ANIM_MUERE            = "muere"
ANIM_RECIBE_DANO      = "recibe_daño"

# Nombre del archivo del laser dentro de ataque_distancia/.
ARCHIVO_LASER = "laser.png"

# Sprite de respaldo (por si falta algun PNG).
RUTA_SPRITE_FALLBACK = "assets/images/personaje.png"

# ==================================================
# VENTANA
# ==================================================
WIDTH   = int(1050 * ESCALA)
HEIGHT  = int(600  * ESCALA)
PANEL_X = int(800  * ESCALA)
FPS     = 60

# ==================================================
# FISICA DEL JUGADOR
# ==================================================
VELOCIDAD_H = int(260 * ESCALA)     # velocidad horizontal
GRAVEDAD    = int(900 * ESCALA)     # aceleracion hacia abajo
SALTO       = int(480 * ESCALA)     # impulso del salto

# Tamano base del sprite del jugador (antes de escalar).
TAMANO_SPRITE_JUGADOR = 60

# Radio del hitbox del jugador.
RADIO_JUGADOR = int(50 * ESCALA)

# Offset del hitbox respecto a la posicion (por defecto centrado).
OFFSET_HITBOX_JUGADOR_X = 0
OFFSET_HITBOX_JUGADOR_Y = 0

# ==================================================
# COMBATE
# ==================================================
VIDA_MAX         = 100.0
ATAQUE           = 8.0
COOLDOWN_GOLPE   = 0.6      # segundos entre golpes cuerpo a cuerpo
COOLDOWN_DISPARO = 0.8      # segundos entre disparos

# ==================================================
# PROYECTIL
# ==================================================
DANO_PROYECTIL         = 6.0
VELOCIDAD_PROYECTIL    = int(700 * ESCALA)
RADIO_PROYECTIL        = int(8 * ESCALA)
TIEMPO_VIDA_PROYECTIL  = 2.5    # segundos

# Frame de la animacion de ataque_distancia en el que
# sale el laser (0-indexado).
FRAME_DISPARO = 9

# ==================================================
# ANIMACIONES: duracion de cada frame (segundos)
# ==================================================
DURACION_QUIETO           = 0.15
DURACION_MOVIMIENTO       = 0.10
DURACION_ATAQUE_NORMAL    = 0.08
DURACION_ATAQUE_DISTANCIA = 0.06
DURACION_ASCIENDE         = 0.12
DURACION_DESCIENDE        = 0.12
DURACION_MUERE            = 0.10
DURACION_RECIBE_DANO      = 0.10

# ==================================================
# MODOS DE LA DEMO (algebra)
# ==================================================
MODO_ROTADA     = 1
MODO_NO_ORT     = 2
MODO_LD         = 3
MODO_INVERTIDA  = 4
MODO_PERSONAJE  = 5
MODO_PLATAFORMA = 6
MODO_1V1        = 7

# ==================================================
# COLORES DEL AREA DE JUEGO
# ==================================================
COLOR_FONDO = (20, 20, 30)

# Colores de los ejes de la base.
COLOR_EJE_V1 = (255, 100, 100)
COLOR_EJE_V2 = (100, 255, 100)

# Colores del cuadrado segun el modo.
COLOR_CUADRO = {
    MODO_ROTADA:    (0, 200, 255),
    MODO_NO_ORT:    (255, 180, 0),
    MODO_LD:        (255, 60, 60),
    MODO_INVERTIDA: (180, 100, 255),
    MODO_PERSONAJE: (100, 255, 200),
}

# Colores de plataformas.
COLOR_PLATAFORMA_VECTORIAL = (100, 255, 200)
COLOR_PLATAFORMA_AFIN      = (255, 180, 0)
COLOR_SUELO                = (80, 80, 120)

# ==================================================
# COLORES DEL PANEL LATERAL
# ==================================================
COLOR_PANEL      = (30, 30, 45)
COLOR_SEPARADOR  = (80, 80, 120)
COLOR_TITULO     = (255, 220, 100)
COLOR_MODO       = (100, 200, 255)
COLOR_TEXTO      = (220, 220, 220)
COLOR_TEXTO_DIM  = (150, 150, 150)
COLOR_OK         = (100, 255, 100)
COLOR_ERROR      = (255, 100, 100)

# ==================================================
# COLORES DE LOS JUGADORES
# ==================================================
COLOR_J1 = (100, 200, 255)
COLOR_J2 = (255, 150, 100)

# ==================================================
# DEBUG
# ==================================================
COLOR_HITBOX_DEBUG = (255, 60, 60)