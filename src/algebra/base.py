from src.algebra.vector import Vector

class Base2D:

    def __init__(self, v1: Vector, v2: Vector):
        # Base B = {v1, v2}
        self.v1 = v1
        self.v2 = v2
        self.es_valida = True

        if self.es_linealmente_dependiente():
            print("Los vectores ingresados son LD. No forman una base para R^2.")
            self.es_valida = False

    def determinante(self) -> float:
        # det(B) = v1_x * v2_y - v1_y * v2_x
        return self.v1.x * self.v2.y - self.v1.y * self.v2.x

    def es_linealmente_dependiente(self) -> bool:
        # det(B) = 0 => LD
        return abs(self.determinante()) == 0

    def es_conjunto_ortogonal(self) -> bool:
        # <v1, v2> = 0 => Ortogonales
        return abs(self.v1.producto_punto(self.v2)) == 0

    def cambiar_de_base(self, v: Vector) -> Vector:
        # Coordenadas [v]_B = (c1, c2) usando la Regla de Cramer
        # Resolvemos v = c1*v1 + c2*v2
        det_B = self.determinante()
        
        if abs(det_B) == 0 :
            raise ValueError("No se puede cambiar de base: la base es linealmente dependiente.")
            
        # c1 = det(v, v2) / det(v1, v2)
        c1 = (v.x * self.v2.y - v.y * self.v2.x) / det_B
        
        # c2 = det(v1, v) / det(v1, v2)
        c2 = (self.v1.x * v.y - self.v1.y * v.x) / det_B
        
        return Vector(c1, c2)

    def reconstruir_desde_base(self, c1: float, c2: float) -> Vector:
        # Combinacion lineal: v = c1*v1 + c2*v2
        return self.v1 * c1 + self.v2 * c2

    def __repr__(self) -> str:
        return f"Base2D(v1={self.v1}, v2={self.v2})"