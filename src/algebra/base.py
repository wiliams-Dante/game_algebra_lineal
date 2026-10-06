from vector import Vector


class Base2D:

    def __init__(self, v1: Vector, v2: Vector):
        self.v1 = v1
        self.v2 = v2
        self.es_valida = True

        if self.es_linealmente_dependiente():
            print(
                "Los vectores ingresados son LD. No forman una base para R^2."
            )
            self.es_valida = False

    def determinante(self) -> float:
        return self.v1.x * self.v2.y - self.v1.y * self.v2.x

    def es_linealmente_dependiente(self) -> bool:
        return self.determinante() == 0.0

    def es_conjunto_ortogonal(self) -> bool:
        return self.v1.producto_punto(self.v2) == 0.0

    def cambiar_de_base(self, v: Vector) -> Vector:
        c1 = v.producto_punto(self.v1) / self.v1.producto_punto(self.v1)
        c2 = v.producto_punto(self.v2) / self.v2.producto_punto(self.v2)
        return Vector(c1, c2)

    def reconstruir_desde_base(self, c1: float, c2: float) -> Vector:
        vector_resultante = self.v1 * c1 + self.v2 * c2
        return vector_resultante

    def __repr__(self) -> str:
        return f"Base2D(v1={self.v1}, v2={self.v2})"
