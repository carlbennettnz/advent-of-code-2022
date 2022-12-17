from typing import NamedTuple

import rich

jets = list(open('17s.txt', 'r').read())
num_rocks = 1000000000000

rocks = [
    [[True] * 4],
    [[False, True, False], [True] * 3, [False, True, False]],
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

formations = set()
max_height = 0
last_max_height = 0
deltas = []

# for rock_num in range(0, len(jets) * len(rocks) * 100):
for rock_num in range(0, 2022):
    rock = rocks[rock_num % len(rocks)]
    location = Point(2, max(p.y for p in cave | {Point(0, -1)}) + 3 + len(rock))

    while True:
        dx = -1 if jets[tick % len(jets)] == "<" else 1
        new_location = Point(location.x + dx, location.y)
        if not collides(rock, new_location):
            location = new_location

        new_location = Point(location.x, location.y - 1)
        tick += 1

        if collides(rock, new_location):
            break

        location = new_location

    cave -= {p for p in cave if p.y < location.y - 100}
    cave |= {*points_in_rock(rock, location)}

    # if rock_num and rock_num % (len(jets) * len(rocks)) == 0:
    #     # formations.add(tuple(sorted([Point(p.x, p.y - location.y) for p in cave], key=lambda p: p.y * 2^8 + p.x)))
    #     last_max_height = max_height
    #     max_height = max(p.y for p in cave)
    #     deltas.append(max_height - last_max_height)
    #     rich.print((max_height - last_max_height) % 79900)
    #
    #     for n in range(2, len(deltas) // 2):
    #         if deltas[-n:] == deltas[-2*n:-n] == deltas[-3*n:-2*n]:
    #             repeat_size = sum(deltas[-n:])
    #             initial_size = sum(deltas[0:-3*n])
    #             num_repeats = (num_rocks - (len(deltas) - 3 * n)) / (len(jets) * len(rocks))
    #             print(num_repeats)
    #             rich.print('found a repeat', dict(n=n, repeat_size=repeat_size, initial_size=initial_size, num_repeats=num_repeats, total=initial_size + repeat_size * num_repeats))
    #             # exit()
    #     # print_cave({location})

print_cave()
print(max(p.y for p in cave) + 1)