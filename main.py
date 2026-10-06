class Vector:
    # 1. Type Hints: le decimos a tus compañeros que x e y son flotantes o enteros
    def __init__(self, x: float, y: float):
        self.x = float(x)
        self.y = float(y)

    def __repr__(self) :
        return f"Vector({self.x}, {self.y})"

    def __add__(self, otro: "Vector") -> "Vector":
        return Vector(self.x + otro.x, self.y + otro.y)

    def __mul__(self, escalar: float) -> "Vector":
        return Vector(self.x * escalar, self.y * escalar)


def main():
    p1 = Vector(4, 5)
    p2 = Vector(2, 3)

    # Impresión directa gracias a __repr__
    print(f"Vector 1: {p1}")  # Muestra: Vector(4.0, 5.0)

    # Suma de vectores usando el operador + (__add__)
    v_suma = p1 + p2
    print(f"Suma: {v_suma}")  # Muestra: Vector(6.0, 8.0)

    # Producto por escalar usando el operador * (__mul__)
    v_escalado = p1 * 2
    print(f"Escalado por 2: {v_escalado}")  # Muestra: Vector(8.0, 10.0)


if __name__ == "__main__":
    main()