import pygame
import sys
import math

# ---------- Configuracion ----------
WIDTH, HEIGHT = 800, 600
FPS = 60
COLOR_FONDO = (15, 15, 25)
COLOR_ARISTA = (100, 220, 255)
COLOR_VERTICE = (255, 220, 100)

# ---------- Vector 3D minimo ----------
class Vector3:
    # Solo lo necesario para el ejemplo: suma, escala y rotacion.
    def __init__(self, x, y, z):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, escalar):
        return Vector3(self.x * escalar, self.y * escalar, self.z * escalar)

    def __repr__(self):
        return f"Vector3({self.x:.2f}, {self.y:.2f}, {self.z:.2f})"


# ---------- Matrices de rotacion (3x3) ----------
# Cada rotacion es una matriz que multiplica al vector.

def rotar_x(v, angulo):
    # Rota alrededor del eje X.
    # [1    0       0   ]
    # [0   cos    -sin  ]
    # [0   sin     cos  ]
    c, s = math.cos(angulo), math.sin(angulo)
    return Vector3(
        v.x,
        v.y * c - v.z * s,
        v.y * s + v.z * c,
    )

def rotar_y(v, angulo):
    # Rota alrededor del eje Y.
    # [ cos   0   sin ]
    # [  0    1    0  ]
    # [-sin   0   cos ]
    c, s = math.cos(angulo), math.sin(angulo)
    return Vector3(
        v.x * c + v.z * s,
        v.y,
        -v.x * s + v.z * c,
    )

def rotar_z(v, angulo):
    # Rota alrededor del eje Z.
    # [cos  -sin  0]
    # [sin   cos  0]
    # [ 0     0   1]
    c, s = math.cos(angulo), math.sin(angulo)
    return Vector3(
        v.x * c - v.y * s,
        v.x * s + v.y * c,
        v.z,
    )


# ---------- Proyeccion en perspectiva ----------
# Un punto 3D se proyecta sobre el plano 2D de la pantalla.
# La idea: cuanto mas lejos (mayor z), mas cerca del centro se dibuja.

def proyectar(v, distancia=4.0, escala=300.0):
    # z + distancia evita dividir entre cero si z esta cerca de 0.
    factor = escala / (v.z + distancia)
    x_pantalla = WIDTH / 2 + v.x * factor
    y_pantalla = HEIGHT / 2 - v.y * factor   # Y invertida: pantalla crece hacia abajo
    return (int(x_pantalla), int(y_pantalla))


# ---------- Cubo ----------
# 8 vertices centrados en el origen, lado 2.
VERTICES_BASE = [
    Vector3(-1, -1, -1),  # 0
    Vector3( 1, -1, -1),  # 1
    Vector3( 1,  1, -1),  # 2
    Vector3(-1,  1, -1),  # 3
    Vector3(-1, -1,  1),  # 4
    Vector3( 1, -1,  1),  # 5
    Vector3( 1,  1,  1),  # 6
    Vector3(-1,  1,  1),  # 7
]

# Aristas: pares de indices de vertices que se conectan.
ARISTAS = [
    (0, 1), (1, 2), (2, 3), (3, 0),   # cara trasera (z = -1)
    (4, 5), (5, 6), (6, 7), (7, 4),   # cara delantera (z = 1)
    (0, 4), (1, 5), (2, 6), (3, 7),   # aristas que unen las dos caras
]


# ---------- Loop principal ----------
def main():
    pygame.init()
    pantalla = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Cubo 3D girando - Pygame")
    reloj = pygame.time.Clock()
    fuente = pygame.font.SysFont("Arial", 16)

    ax, ay, az = 0.0, 0.0, 0.0   # angulos de rotacion acumulados

    while True:
        dt = reloj.tick(FPS) / 1000.0

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                pygame.quit(); sys.exit()

        # --- Actualizar angulos ---
        ax += 0.7 * dt
        ay += 1.1 * dt
        az += 0.3 * dt

        # --- Rotar cada vertice del cubo ---
        vertices_rotados = []
        for v in VERTICES_BASE:
            r = rotar_x(v, ax)
            r = rotar_y(r, ay)
            r = rotar_z(r, az)
            vertices_rotados.append(r)

        # --- Proyectar a 2D ---
        puntos_2d = [proyectar(v) for v in vertices_rotados]

        # --- Dibujar ---
        pantalla.fill(COLOR_FONDO)

        # Aristas
        for i, j in ARISTAS:
            pygame.draw.line(pantalla, COLOR_ARISTA,
                             puntos_2d[i], puntos_2d[j], 2)

        # Vertices
        for p in puntos_2d:
            pygame.draw.circle(pantalla, COLOR_VERTICE, p, 4)

        # Texto de ayuda
        texto = fuente.render(
            "Cubo 3D con proyeccion en perspectiva - ESC para salir",
            True, (180, 180, 180))
        pantalla.blit(texto, (20, 20))

        pygame.display.flip()


if __name__ == "__main__":
    main()