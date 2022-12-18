input = [[int(p) for p in line.split(",")] for line in open("../in/18.txt", "r").read().strip().split("\n")]
droplets = {(x, y, z) for x, y, z in input}


def adj(p):
    x, y, z = p
    return [
        (x + 1, y, z),
        (x - 1, y, z),
        (x, y + 1, z),
        (x, y - 1, z),
        (x, y, z + 1),
        (x, y, z - 1),
    ]


print("part 1:", sum(1 for d in droplets for a in adj(d) if a not in droplets))

limit = max(max(x, y, z) for x, y, z in droplets)
outside = set()
outside_count = 0

while True:
    for x in range(-1, limit + 2):
        for y in range(-1, limit + 2):
            for z in range(-1, limit + 2):
                p = (x, y, z)

                if p in droplets:
                    continue

                if outside_count == 0 and any(a == -1 or a == limit + 1 for a in p):
                    outside.add(p)

                if any(a in outside for a in adj(p)):
                    outside.add(p)

    if outside_count == len(outside):
        break

    outside_count = len(outside)

print("part 2:", sum(1 for d in droplets for a in adj(d) if a not in droplets and a in outside))
