from collections import namedtuple

input = open('14.txt', 'r').read()

rock = set()
sand = set()

Point = namedtuple('Point', ['x', 'y'])

for line in input.split('\n'):
    last = None

    for point in line.split(' -> '):
        p = Point(*[int(n) for n in point.split(',')])
        last = last or p

        if last:
            if last.x < p.x:
                for x in range(last.x, p.x + 1):
                    rock.add(Point(x, p.y))

            if last.x > p.x:
                for x in range(p.x, last.x + 1):
                    rock.add(Point(x, p.y))

            if last.y < p.y:
                for y in range(last.y, p.y + 1):
                    rock.add(Point(p.x, y))

            if last.y > p.y:
                for y in range(p.y, last.y + 1):
                    rock.add(Point(p.x, y))

        last = p

def blocked(p):
    return p in rock or p in sand

max_y = max(p.y for p in rock)

def print_cave():
    min_x = min(p.x for p in rock.union(sand))
    max_x = max(p.x for p in rock.union(sand))

    for y in range(0, max_y+3):
        line = ''

        for x in range(min_x - 1, max_x+2):
            p = Point(x, y)
            if p in rock or p.y == max_y + 2:
                line += '#'
            elif p in sand:
                line += 'O'
            else:
                line += '.'

        print(line + ' ' + str(len([p for p in sand if p.y == y])))

def down(point):
    return Point(point.x, point.y + 1)

def down_left(point):
    return Point(point.x - 1, point.y + 1)

def down_right(point):
    return Point(point.x + 1, point.y + 1)

def tick():
    p = Point(500, 0)

    while True:
        if p.y == max_y + 1:
            break
        if not blocked(down(p)):
            l = p
            p = down(p)
        elif not blocked(down_left(p)):
            l = p
            p = down_left(p)
        elif not blocked(down_right(p)):
            l = p
            p = down_right(p)
        else:
            break

    sand.add(p)
    return p != Point(500, 0)

while tick():
    pass

print_cave()
print(len(sand))

o = Point(500, -1)