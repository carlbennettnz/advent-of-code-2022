from collections import defaultdict
from typing import NamedTuple

jets = [-1 if jet == "<" else 1 for jet in open('17.txt', 'r').read()]
num_rocks = 1000000000000

rocks = [
    [[True] * 4],
    [[False, True, False], [True] * 3, [False, True, False]],
    [[False, False, True], [False, False, True], [True] * 3],
    [[True]] * 4,
    [[True] * 2] * 2
]

tower = defaultdict(list)
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
    if location.x < 0 or location.x + len(rock[0]) > 7 or location.y - len(rock) + 1 < 0:
        return True

    for point in points_in_rock(rock, location):
        if point.x in tower[point.y]:
            return True

    return False

def print_cave(rock_points = None):
    if not rock_points:
        rock_points = []

    top = max(p.y for p in rock_points) if rock_points else max(tower.keys())

    for y in range(top, max(top - 30, 0) - 1, -1):
        print(''.join('#' if x in tower[y] else ('@' if Point(x, y) in rock_points else '.') for x in range(0, 7)))

max_height = 0
last_max_height = 0
deltas = []
cycle_size = len(rocks)
stop_after = None
projection = None

for rock_num in range(0, num_rocks):
    rock = rocks[rock_num % len(rocks)]
    max_y_in_tower = max([y for y in tower if tower[y]]) if rock_num else -1
    location = Point(2, max_y_in_tower + 3 + len(rock))

    # Position the rock on the tower
    while True:
        new_location = Point(location.x + jets[tick % len(jets)], location.y)
        tick += 1

        if not collides(rock, new_location):
            location = new_location

        new_location = Point(location.x, location.y - 1)

        if collides(rock, new_location):
            break

        location = new_location

    # Add rock to the tower
    for point in points_in_rock(rock, location):
        tower[point.y].append(point.x)

    # Forget about parts of the stack more than 100 layers deep. An ultimately-unnecessary optimisation.
    for y in [y for y in tower if y < location.y - 100]:
        del tower[y]

    if rock_num + 1 == 2022:
        print('part 1:', max(y for y in tower if tower[y]) + 1)

    # If we've completed a cycle, check for repeating patterns in the delta of each cycle. If we find that the
    # last, say, 50 deltas were the same as the 50 before that, and those are the same as the 50 before, we
    # assume the pattern will repeat forever. We can extrapolate and print the answer.
    if rock_num and rock_num % cycle_size == 0:
        last_max_height, max_height = max_height, max(y for y in tower if tower[y])
        delta = max_height - last_max_height
        deltas.append(delta)

        for n in range(2, len(deltas) // 2):
            # Check if the last 3 sets of n cycles match
            if deltas[-n:] == deltas[-2*n:-n] == deltas[-3*n:-2*n]:
                # There are now 4 different numbers we need to get the answer:
                # - The height so far
                # - The size of all the repeating sets of n cycles we can fit between now and the final rock
                # - The size of a partial set of cycles at the end
                # - The size of a partial cycle after that
                # We'll need to drop a few more rocks to get the last number.
                repeat_size = sum(deltas[-n:])
                rocks_remaining = num_rocks - rock_num
                repeats_remaining = rocks_remaining // (cycle_size * n)
                rocks_after_last_repeat = rocks_remaining % (cycle_size * n)
                delta_of_partial_repeat = deltas[-n:-n + rocks_after_last_repeat // cycle_size]
                beyond_last_cycle = rocks_remaining % cycle_size
                projection = max_height + repeats_remaining * repeat_size + sum(delta_of_partial_repeat)
                # print(f'repeats start after {rock_num // cycle_size - 3 * n} cycles')
                # print(f'there are {beyond_last_cycle} rocks beyond the last cycle')
                stop_after = rock_num + beyond_last_cycle

    if rock_num == stop_after:
        delta = max(y for y in tower if tower[y]) - max_height
        projection += delta
        print('part 2:', projection)
        exit()
