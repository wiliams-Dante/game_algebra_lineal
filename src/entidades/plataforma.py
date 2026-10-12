from src.algebra.vector import Vector, EPSILON


class Plataforma:
    # Recta acotada: { origen + t*direccion : 0 <= t <= longitud }.
    # Si origen == (0,0), es subespacio vectorial.
    # Si origen != (0,0), es subespacio afín (trasladado).

    def __init__(self, origen: Vector, direccion: Vector, longitud: float,
                 grosor: float ):
        self.origen = origen
        self.direccion = direccion.normalizar()
        self.longitud = longitud
        self.grosor = grosor

    def extremo_final(self) -> Vector:
        # origen + longitud * direccion
        return self.origen + self.direccion * self.longitud

    def parametro(self, punto: Vector) -> float:
        # t = <punto - origen, direccion>
        # Coordenada escalar del punto a lo largo de la recta.
        return (punto - self.origen).producto_punto(self.direccion)

    def proyectar(self, punto: Vector) -> Vector:
        # Proyección ortogonal sobre la recta infinita.
        t = self.parametro(punto)
        return self.origen + self.direccion * t

    def punto_mas_cercano(self, punto: Vector) -> Vector:
        # Punto del segmento más cercano (t acotado a [0, longitud]).
        t = self.parametro(punto)
        t = max(0.0, min(self.longitud, t))
        return self.origen + self.direccion * t

    def distancia(self, punto: Vector) -> float:
        # Distancia perpendicular a la recta infinita.
        return (punto - self.proyectar(punto)).magnitud()

    def distancia_al_segmento(self, punto: Vector) -> float:
        # Distancia al segmento (no a la recta infinita).
        return (punto - self.punto_mas_cercano(punto)).magnitud()

    def colisiona(self, punto: Vector, radio: float) -> bool:
        # Colisión círculo-segmento.
        return self.distancia_al_segmento(punto) <= radio

    def normal(self) -> Vector:
        # Vector perpendicular a la direccion.
        return Vector(self.direccion.y, -self.direccion.x)


    def es_subespacio_vectorial(self) -> bool:
        # Lo es si pasa por el origen.
        return self.origen.magnitud() < EPSILON

    def es_subespacio_afin(self) -> bool:
        # Es afín si NO pasa por el origen.
        return not self.es_subespacio_vectorial()

    def contiene_al_cero(self) -> bool:
        # El (0,0) está en la recta si el origen lo está.
        return self.es_subespacio_vectorial()

    def tipo(self) -> str:
        # Etiqueta para mostrar en el panel.
        if self.es_subespacio_vectorial():
            return "Subespacio vectorial"
        return "Subespacio afin"

    def __repr__(self) -> str:
        return (f"Plataforma(origen={self.origen}, "
                f"direccion={self.direccion}, longitud={self.longitud})")