# VARIABLES DEL PROYECTO

#  Ventana 
WIDTH, HEIGHT = 1050, 600
PANEL_X = 800 # Posición horizontal donde empieza la interfaz 
FPS = 60 # Fluidez del juego


#  Jugador 
VELOCIDAD_MOV = 300 # Velo de mov. en píxeles por segundo 
TAMANO_JUGADOR = 50 # 50x50 píxeles


#  Modos de la demo 
MODO_ROTADA = 1     # Base ortonormal rotada
MODO_NO_ORT = 2     # Base no ortogonal
MODO_LD = 3         # Base linealmente dependiente 
MODO_INVERTIDA = 4  # Base con orientación negativa


#  Colores del área del juego 
COLOR_FONDO = (20, 20, 30) # Fondo oscuro 
COLOR_EJE_V1 = (255, 100, 100) # Vector rojo eje x
COLOR_EJE_V2 = (100, 255, 100) # Vector verde eje Y 



#  Colores del cuadrado según el modo 
COLOR_CUADRO = {
    MODO_ROTADA:    (0, 200, 255),   # azul
    MODO_NO_ORT:    (255, 180, 0),   # naranja
    MODO_LD:        (255, 60, 60),   # rojo
    MODO_INVERTIDA: (180, 100, 255), # morado
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