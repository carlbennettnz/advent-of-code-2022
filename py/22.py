import re
from util import Vector

map, moves = open("../in/22s.txt", "r").read().split("\n\n")

map = map.split("\n")

pos = Vector(min([map[0].index("."), map[0].index("#")]), 0)
d = 0
d_vectors = [
    Vector.E,
    Vector.S,
    Vector.W,
    Vector.N,
]

width = max(len(row) for row in map)


def pixel(p):
    row = map[p.y % len(map)]
    # print("pixel", p.x % width, f'"{row[p.x % width] if p.x % width < len(row) else " "}"')
    return row[p.x % width] if p.x % width < len(row) else " "


print("?", pixel(Vector(1, 5)))
while moves:
    dist = re.match(r"^\d+", moves).group()
    moves = moves[len(dist) :]

    for i in range(int(dist)):
        next_pos = pos + d_vectors[d]
        # print("next_pos", next_pos.x % width, next_pos.y % len(map))

        while pixel(next_pos) == " ":
            # print("skipping", next_pos)
            next_pos += d_vectors[d]

        if pixel(next_pos) == "#":
            break

        pos = next_pos

    # print(dist, pos.x % width, pos.y % len(map))

    if moves:
        dd = moves[0]
        moves = moves[1:]

        if dd == "L":
            d = (d - 1) % 4
        else:
            d = (d + 1) % 4

print((pos.y % len(map) + 1) * 1000 + (pos.x % width + 1) * 4 + d)
