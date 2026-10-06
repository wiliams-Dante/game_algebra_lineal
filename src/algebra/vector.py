import math


class Vector:

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y})"

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector") -> "Vector":
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, escalar: float) -> "Vector":
        return Vector(self.x * escalar, self.y * escalar)

    def __rmul__(self, escalar: float) -> "Vector":
        return self.__mul__(escalar)

    def producto_punto(self, other: "Vector") -> float:
        return self.x * other.x + self.y * other.y

    def magnitud(self) -> float:
        return math.sqrt(self.x**2 + self.y**2)

    def normalizar(self) -> "Vector":
        mag = self.magnitud()
        if mag == 0:
            return Vector(0.0, 0.0)
        return Vector(self.x / mag, self.y / mag)