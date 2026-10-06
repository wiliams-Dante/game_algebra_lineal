import os
import sys

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")
)

from algebra.vector import Vector

u = Vector(4, 3)
v = Vector(-1, 2)

print(f"u = {u}")
print(f"v = {v}")

print(f"u + v = {u + v}")
print(f"u - v = {u - v}")
print(f"2 * u = {2 * u}") 
print(f"u · v = {u.producto_punto(v)}")
print(f"||u|| = {u.magnitud()}")
print(f" û = {u.normalizar()}")
