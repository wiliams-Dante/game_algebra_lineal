import pygame

# Tu clase matemática con floats
class Vector2D:
    def __init__(self, x: float, y: float):
        self.x = float(x)
        self.y = float(y)

    def sumar(self, otro: "Vector2D") -> "Vector2D":
        return Vector2D(self.x + otro.x, self.y + otro.y)

# Inicializar Pygame
pygame.init()
pantalla = pygame.display.set_mode((600, 400))

# --- VARIABLES DEL JUEGO ---
posicion = Vector2D(50.0, 200.0)      # Posición inicial
velocidad = Vector2D(2.5, 0.0)       # Se moverá 2.5 píxeles a la derecha por frame

reloj = pygame.time.Clock()
ejecutando = True

while ejecutando:
    reloj.tick(60)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    # 1. ACTUALIZAR POSICIÓN (Lógica de Álgebra Lineal con Floats)
    posicion = posicion.sumar(velocidad)

    # 2. DIBUJAR EN PANTALLA (Conexión con Pygame)
    pantalla.fill((20, 20, 20))
    
    # Pasamos las coordenadas float de nuestro vector a Pygame
    pygame.draw.rect(pantalla, (0, 255, 150), (posicion.x, posicion.y, 50, 50))

    pygame.display.flip()

pygame.quit()