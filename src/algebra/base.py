from src.algebra.vector import Vector, EPSILON


class Base2D:

    def __init__(self, v1: Vector, v2: Vector):
        # Conjunto B = {v1, v2}
        self.v1 = v1
        self.v2 = v2
        self.es_valida = True

        if self.es_linealmente_dependiente():
            print("Los vectores son LD. No forman una base para R^2.")
            self.es_valida = False

    def determinante(self) -> float:
        # det(B) = v1_x * v2_y - v1_y * v2_x
        return self.v1.x * self.v2.y - self.v1.y * self.v2.x

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
        # Signo del det(B)
        det = self.determinante()
        if abs(det) < EPSILON:
            return "LD, no es base"
        elif det > 0:
            return "Positiva (det > 0)"
        else:
            return "Negativa (det < 0)"

    def cambiar_de_base(self, v: Vector) -> Vector:
        #Multiplica la Matriz Inversa de la Base por el Vector v.
        det_B = self.determinante()

        if abs(det_B) < EPSILON:
            print("No se puede cambiar de base, los vectores son L.D.")
            return Vector(0.0, 0.0)
        #Matriz de vectores de la base
        a, b = self.v1.x, self.v2.x
        c, d = self.v1.y, self.v2.y

        # 3. Matriz Inversa 
        inv_a =  d / det_B
        inv_b = -b / det_B
        inv_c = -c / det_B
        inv_d =  a / det_B

        # Multiplicación Matriz x Vector:
 
        c1 = inv_a * v.x + inv_b * v.y
        c2 = inv_c * v.x + inv_d * v.y

        return Vector(c1, c2)

    def reconstruir_desde_base(self, c1: float, c2: float) -> Vector:
        # v = c1*v1 + c2*v2
        return self.v1 * c1 + self.v2 * c2

    def proyectar(self, v: Vector) -> Vector:
        # proj(v) = c1*v1 + c2*v2, con [v]_B = (c1, c2)
        # Es el vector del plano (o recta) generado por v1 y v2 más cercano a v.
        if not self.es_valida:
            return Vector(0.0, 0.0)
        c = self.cambiar_de_base(v)
        return self.reconstruir_desde_base(c.x, c.y)

    def componente_ortogonal(self, v: Vector) -> Vector:
        # v_perp = v - proj(v)
        # Parte de v que queda fuera del plano (o recta) generado por v1 y v2.
        # Cumple v = proj(v) + v_perp.
        return v - self.proyectar(v)

    def __repr__(self) -> str:
        return f"Base2D(v1={self.v1}, v2={self.v2})"