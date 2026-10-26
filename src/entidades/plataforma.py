# src/entidades/plataforma.py
from src.algebra.vector import Vector, EPSILON

class Plataforma:
    # Recta acotada: { origen + t*direccion : 0 <= t <= longitud }.
    #
    # Nota matematica:
    #   - TODO subespacio vectorial es tambien un subespacio afin.
    #   - Si pasa por el origen (origen == (0,0)): es un subespacio vectorial.
    #   - Si NO pasa por el origen: es un subespacio afin propio (trasladado).

    def __init__(self, origen: Vector, direccion: Vector, longitud: float, grosor: float):
        self.origen = origen
        self.direccion = direccion.normalizar()
        self.longitud = longitud
        self.grosor = grosor

    def extremo_final(self) -> Vector:
        # origen + longitud * direccion
        return self.origen + self.direccion * self.longitud

    def parametro(self, punto: Vector) -> float:
        # t = <punto - origen, direccion>
        return (punto - self.origen).producto_punto(self.direccion)

    def proyectar(self, punto: Vector) -> Vector:
        # Proyeccion ortogonal sobre la recta infinita.
        t = self.parametro(punto)
        return self.origen + self.direccion * t

    def punto_mas_cercano(self, punto: Vector) -> Vector:
        # Punto del segmento mas cercano (t acotado a [0, longitud]).
        t = self.parametro(punto)
        t = max(0.0, min(self.longitud, t))
        return self.origen + self.direccion * t

    def distancia_al_segmento(self, punto: Vector) -> float:
        # Distancia al segmento (no a la recta infinita).
        return (punto - self.punto_mas_cercano(punto)).magnitud()

    def colisiona(self, punto: Vector, radio: float) -> bool:
        # Colision circulo-segmento.
        return self.distancia_al_segmento(punto) <= radio

    def normal(self) -> Vector:
        # Vector perpendicular a la direccion.
        return Vector(self.direccion.y, -self.direccion.x)

    # ---------- Clasificacion algebraica ----------

    def pasa_por_origen(self) -> bool:
        # La recta contiene al (0,0) si su origen es (0,0).
        return self.origen.magnitud() < EPSILON

    def es_subespacio_vectorial(self) -> bool:
        # Pasa por el origen  =>  subespacio vectorial.
        return self.pasa_por_origen()

    def es_subespacio_afin_propio(self) -> bool:
        # Subespacio afin que NO es vectorial: esta trasladado.
        return not self.pasa_por_origen()

    def __repr__(self) -> str:
        return (f"Plataforma(origen={self.origen}, "
                f"direccion={self.direccion}, longitud={self.longitud})")