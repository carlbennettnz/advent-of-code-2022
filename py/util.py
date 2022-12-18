from dataclasses import dataclass


@dataclass(frozen=True)
class Vector:
    x: int
    y: int

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)


Vector.N = Vector(0, -1)
Vector.S = Vector(0, 1)
Vector.E = Vector(1, 0)
Vector.W = Vector(-1, 0)
Vector.NE = Vector(1, -1)
Vector.NW = Vector(-1, -1)
Vector.SE = Vector(1, 1)
Vector.SW = Vector(-1, 1)
