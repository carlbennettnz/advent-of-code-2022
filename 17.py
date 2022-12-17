from typing import NamedTuple
import rich

jets = list(open('17.txt', 'r').read())
num_rocks = 1000000000000

rocks = [
    [[True] * 4],
    [[False, True, False], [True, False, True], [False, True, False]],
    [[False, False, True], [False, False, True], [True] * 3],
    [[True]] * 4,
    [[True] * 2] * 2
]

cave = set()
tick = 0

class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

def points_in_rock(rock, location):
    points = []

    for y, line in enumerate(rock):
        for x, point in enumerate(line):
            if point:
                points.append(Point(location.x + x, location.y - y))

    return points

def collides(rock, location):
    for point in points_in_rock(rock, location):
        if point in cave or point.x < 0 or point.x >= 7 or point.y < 0:
            return True

    return False

def print_cave(rock_points = None):
    if not rock_points:
        rock_points = cave
    top = max(p.y for p in rock_points)
    for y in range(top, max(top - 30, 0), -1):
        print(''.join('#' if Point(x, y) in cave else ('@' if Point(x, y) in rock_points else '.') for x in range(0, 7)))

max_height = 0
last_max_height = 0
deltas = []
cycle_size = len(jets) * len(rocks)
print(num_rocks / cycle_size)

# for rock_num in range(0, len(jets) * len(rocks) * 100):
for rock_num in range(0, num_rocks):
    rock = rocks[rock_num % len(rocks)]
    location = Point(2, max(p.y for p in cave | {Point(0, -1)}) + 3 + len(rock))
    starting_tick = tick

    while True:
        dx = -1 if jets[tick % len(jets)] == "<" else 1
        new_location = Point(location.x + dx, location.y)
        if not collides(rock, new_location):
            location = new_location

        new_location = Point(location.x, location.y - 1)
        tick += 1

        if tick - starting_tick > 3 and collides(rock, new_location):
            break

        location = new_location

    cave -= {p for p in cave if p.y < location.y - 100}
    cave |= {*points_in_rock(rock, location)}

    if rock_num and rock_num % cycle_size == 0:
        last_max_height = max_height
        max_height = max(p.y for p in cave)
        delta = max_height - last_max_height
        deltas.append(delta)
        rich.print(delta, max_height, num_rocks // rock_num * max_height)

        for n in range(2, len(deltas) // 2):
            if deltas[-n:] == deltas[-2*n:-n] == deltas[-3*n:-2*n]:
                repeat_size = sum(deltas[-n:])
                rocks_remaining = num_rocks - rock_num
                repeats_remaining = int(rocks_remaining / cycle_size / n)
                extra_cycles = rocks_remaining % (cycle_size * n)
                additional_cycles = deltas[-n:-n + extra_cycles // cycle_size]
                missed = rocks_remaining % cycle_size
                print(additional_cycles)
                projection = max_height + repeats_remaining * repeat_size + sum(additional_cycles)
                print('expected ', 1514285714288)
                print('projected', projection)
                print('repeats start after', rock_num // cycle_size - 3 * n, 'cycles')
                print('missed', missed)
                exit()
        # print_cave({location})

print_cave()
print(max(p.y for p in cave) + 1)