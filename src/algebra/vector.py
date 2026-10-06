class Vector:
    def __init__(self, x : float, y : float):
        self.x = x
        self.y = y 


    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y})" 
    
    def __add__ (self, Vector2: Vector ) -> Vector:
        p = Vector(self.x + Vector2.x, self.y + Vector2.y)
        return p 



def main():
    # 1. Probar Espacio Vectorial R² (Tema 1)
    posicion = Vector(10.0, 5.0)
    velocidad = Vector(2.0, 0.0)
    
    nueva_posicion = posicion + velocidad
    print(f"Nueva Posición: {nueva_posicion}")  # Muestra: Vector(12.0, 5.0)

if __name__ == "__main__":
    main()