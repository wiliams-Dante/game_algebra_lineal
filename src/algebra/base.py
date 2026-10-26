from src.algebra.vector import Vector, EPSILON

def determinante_2x2(u: Vector, v: Vector) -> float:
    return u.x * v.y - u.y * v.x


class Base2D:

    def __init__(self, v1: Vector, v2: Vector):
        # Conjunto B = {v1, v2}
        self.v1 = v1
        self.v2 = v2
        self.es_valida = not self.es_linealmente_dependiente()

    def determinante(self) -> float:
        # Reutiliza la función global
        return determinante_2x2(self.v1, self.v2)

    
    def es_linealmente_dependiente(self) -> bool:
        # det(B) = 0  =>  LD (paralelos)
        return abs(self.determinante()) < EPSILON

    def es_conjunto_ortogonal(self) -> bool:
        # <v1, v2> = 0  =>  ortogonales
        return abs(self.v1.producto_punto(self.v2)) < EPSILON

    def es_base(self) -> bool:
        # Es base si es LI
        return not self.es_linealmente_dependiente()

    def es_base_ortogonal(self) -> bool:
        # Es base y sus vectores son ortogonales
        return self.es_base() and self.es_conjunto_ortogonal()

    def es_base_ortonormal(self) -> bool:
        # Es base ortogonal y ambos vectores son unitarios
        if not self.es_base_ortogonal():
            return False
        return (abs(self.v1.magnitud() - 1.0) < EPSILON and
                abs(self.v2.magnitud() - 1.0) < EPSILON)

    def orientacion(self) -> str:
        # Signo del det(B): indica si la base es dextrógira o levógira.
        # det > 0 -> misma orientación que la canónica.
        # det < 0 -> orientación invertida (como un reflejo).
        det = self.determinante()
        if abs(det) < EPSILON:
            return "LD, no es base"
        elif det > 0:
            return "Positiva (det > 0)"
        else:
            return "Negativa (det < 0)"

    def cambiar_de_base(self, v: Vector):
        # Devuelve [v]_B = coordenadas de v en la base {v1, v2}.
        # None si la base no es válida (LD).
        det_B = self.determinante()
        if abs(det_B) < EPSILON:
            return None

        # Matriz de vectores de la base
        a, b = self.v1.x, self.v2.x
        c, d = self.v1.y, self.v2.y

        # Matriz inversa
        inv_a =  d / det_B
        inv_b = -b / det_B
        inv_c = -c / det_B
        inv_d =  a / det_B

        # Multiplicación Matriz x Vector
        c1 = inv_a * v.x + inv_b * v.y
        c2 = inv_c * v.x + inv_d * v.y

        return Vector(c1, c2)

    def reconstruir_desde_base(self, c1: float, c2: float) -> Vector:
        # v = c1*v1 + c2*v2
        return self.v1 * c1 + self.v2 * c2

    def __repr__(self) -> str:
        return f"Base2D(v1={self.v1}, v2={self.v2})"