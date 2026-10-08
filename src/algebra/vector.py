import math

# Dos números con diferencia < EPSILON se consideran "iguales"
EPSILON = 1e-9

class Vector:

    def __init__(self, x: float, y: float):
        # v = (x, y)
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        # Imprime (x, y)
        return f"Vector({self.x}, {self.y})"

    def __add__(self, other: "Vector") -> "Vector":
        # w = u + v
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector") -> "Vector":
        # w = u - v
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, escalar: float) -> "Vector":
        # w = c * v
        return Vector(self.x * escalar, self.y * escalar)

    def __rmul__(self, escalar: float) -> "Vector":
        # w = c * v
        return self.__mul__(escalar)

    def producto_punto(self, other: "Vector") -> float:
        # k = <u, v>
        return self.x * other.x + self.y * other.y

    def magnitud(self) -> float:
        # m = ||v||
        return math.sqrt(self.x**2 + self.y**2)

    def normalizar(self) -> "Vector":
        # u = v / ||v|| (vector unitario, ||u|| = 1)
        mag = self.magnitud()
        # Si la magnitud es ~0, el vector es (casi) nulo: no se puede normalizar.
        if mag < EPSILON:
            return Vector(0.0, 0.0)
        return Vector(self.x / mag, self.y / mag)