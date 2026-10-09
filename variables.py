# ESCALA GLOBAL
ESCALA = 1.25
RUTA_SPRITE = "assets/images/personaje.png"  
#  Ventana 
WIDTH = int(1050 * ESCALA)
HEIGHT = int(600 * ESCALA)
PANEL_X = int(800 * ESCALA)
FPS = 60

#  Jugador 
VELOCIDAD_MOV = int(300 * ESCALA)
TAMANO_JUGADOR = int(50 * ESCALA)

#  Modos de la demo 
MODO_ROTADA = 1
MODO_NO_ORT = 2
MODO_LD = 3
MODO_INVERTIDA = 4
MODO_PERSONAJE = 5


#  Colores del área del juego 
COLOR_FONDO = (20, 20, 30)
COLOR_EJE_V1 = (255, 100, 100)
COLOR_EJE_V2 = (100, 255, 100)

#  Colores del cuadrado según el modo 
COLOR_CUADRO = {
    MODO_ROTADA:    (0, 200, 255),
    MODO_NO_ORT:    (255, 180, 0),
    MODO_LD:        (255, 60, 60),
    MODO_INVERTIDA: (180, 100, 255),
    MODO_PERSONAJE: (100, 255, 200)  
}

#  Colores del panel lateral 
COLOR_PANEL = (30, 30, 45)
COLOR_SEPARADOR = (80, 80, 120)
COLOR_TITULO = (255, 220, 100)
COLOR_MODO = (100, 200, 255)
COLOR_TEXTO = (220, 220, 220)
COLOR_TEXTO_DIM = (150, 150, 150)
COLOR_OK = (100, 255, 100)
COLOR_ERROR = (255, 100, 100)