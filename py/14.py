from util import Vector

input = open("../in/14.txt", "r").read()

rock = set()

# parse
for line in input.split("\n"):
    last = None

    for point in line.split(" -> "):
        p = Vector(*[int(n) for n in point.split(",")])
        last = last or p

        if last:
            if last.x < p.x:
                for x in range(last.x, p.x + 1):
                    rock.add(Vector(x, p.y))

            if last.x > p.x:
                for x in range(p.x, last.x + 1):
                    rock.add(Vector(x, p.y))

            if last.y < p.y:
                for y in range(last.y, p.y + 1):
                    rock.add(Vector(p.x, y))

            if last.y > p.y:
                for y in range(p.y, last.y + 1):
                    rock.add(Vector(p.x, y))

        last = p


max_y = max(p.y for p in rock)


def blocked(p):
    return p in rock or p in sand


def print_cave():
    min_x = min(p.x for p in rock.union(sand))
    max_x = max(p.x for p in rock.union(sand))

    for y in range(0, max_y + 3):
        line = ""

        for x in range(min_x - 1, max_x + 2):
            p = Vector(x, y)
            if p in rock or p.y == max_y + 2:
                line += "#"
            elif p in sand:
                line += "O"
            else:
                line += "."

        print(line + " " + str(len([p for p in sand if p.y == y])))


for part in range(1, 3):
    sand = set()

    def tick():
        p = Vector(500, 0)

        while True:
            if p.y == max_y + 1:
                if part == 1:
                    return False
                else:
                    break
            if not blocked(p + Vector.S):
                p += Vector.S
            elif not blocked(p + Vector.SW):
                p += Vector.SW
            elif not blocked(p + Vector.SE):
                p += Vector.SE
            else:
                break

        sand.add(p)
        return part != 2 or p.y != 0

    while tick():
        pass

    # print_cave()
    print(f"part {part}", len(sand))
