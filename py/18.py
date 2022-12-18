import dataclasses
import itertools
from rich import print

input = [[int(p) for p in line.split(",")] for line in open("../in/18.txt", "r").read().strip().split("\n")]


@dataclasses.dataclass(frozen=True)
class Vector:
    x: int
    y: int
    z: int

    def adj(self):
        return [
            Vector(self.x + 1, self.y, self.z),
            Vector(self.x - 1, self.y, self.z),
            Vector(self.x, self.y + 1, self.z),
            Vector(self.x, self.y - 1, self.z),
            Vector(self.x, self.y, self.z + 1),
            Vector(self.x, self.y, self.z - 1),
        ]


droplets = [Vector(x, y, z) for x, y, z in input]
sides = set()

count = 0

for droplet in droplets:
    for adj in droplet.adj():
        if adj not in droplets:
            sides.add((droplet, adj))

print("part 1:", len(sides))

bounds = (
    (min(p.x for p in droplets), max(p.x for p in droplets)),
    (min(p.y for p in droplets), max(p.y for p in droplets)),
    (min(p.z for p in droplets), max(p.z for p in droplets)),
)
outside = {Vector(bounds[0][0] - 1, bounds[1][0] - 1, bounds[2][0] - 2)}

while True:
    for x in range(bounds[0][0] - 1, bounds[0][1] + 2):
        for y in range(bounds[1][0] - 1, bounds[1][1] + 2):
            for z in range(bounds[2][0] - 1, bounds[2][1] + 2):
                p = Vector(x, y, z)

                if p in droplets:
                    continue

                if any(adj in outside for adj in p.adj()):
                    outside.add(p)

    count = 0

    for wall, space in sides:
        if space in outside:
            count += 1

    print("part 2:", count)
