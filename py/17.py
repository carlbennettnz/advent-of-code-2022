from dataclasses import dataclass
from collections import defaultdict

from util import Vector

jets = [-1 if jet == "<" else 1 for jet in open("../in/17.txt", "r").read()]
num_rocks = 1000000000000

rock_templates = [
    [[True] * 4],
    [[False, True, False], [True] * 3, [False, True, False]],
    [[False, False, True], [False, False, True], [True] * 3],
    [[True]] * 4,
    [[True] * 2] * 2,
]

tower = defaultdict(list)
tick = 0


@dataclass
class Rock:
    points: list[Vector]

    @classmethod
    def from_template(cls, template, location):
        points: list[Vector] = []

        for y, row in enumerate(template):
            for x, point in enumerate(row):
                if point:
                    points.append(Vector(x, -y) + location)

        return cls(points)

    def move(self, vector):
        new_points = [point + vector for point in self.points]

        if any(p.x < 0 or p.x >= 7 or p.y < 0 or p.x in tower[p.y] for p in new_points):
            return False

        self.points = new_points

        return True


def print_tower(rock=None):
    if not rock:
        rock = Rock([])

    top = max(p.y for p in rock.points) if rock.points else max(tower.keys())

    for y in range(top, max(top - 30, 0) - 1, -1):
        line = ""

        for x in range(0, 7):
            if x in tower[y]:
                line += "#"
            elif Vector(x, y) in rock.points:
                line += "@"
            else:
                line += "."

        print(line)

    print()


max_height = 0
last_max_height = 0
deltas = []
cycle_size = len(rock_templates)
stop_after = None
projection = 0

for rock_num in range(0, num_rocks):
    rock_template = rock_templates[rock_num % len(rock_templates)]
    max_y_in_tower = max([y for y in tower if tower[y]]) if rock_num else -1
    location = Vector(2, max_y_in_tower + 3 + len(rock_template))
    rock = Rock.from_template(rock_template, location)

    # Position the rock on the tower
    while True:
        rock.move(Vector(jets[tick % len(jets)], 0))
        tick += 1

        if not rock.move(Vector(0, -1)):
            break

    # Add rock to the tower
    for point in rock.points:
        tower[point.y].append(point.x)

    # Forget about parts of the stack more than 100 layers deep. An ultimately-unnecessary optimisation.
    for y in [y for y in tower if y < location.y - 100]:
        del tower[y]

    if rock_num + 1 == 2022:
        print("part 1:", max(y for y in tower if tower[y]) + 1)

    # If we've completed a cycle, check for repeating patterns in the deltas of each cycle. If we find that the
    # last, say, 50 deltas were the same as the 50 before that, and those are the same as the 50 before, we
    # assume the pattern will repeat forever. We can extrapolate and print the answer.
    if rock_num and rock_num % cycle_size == 0:
        last_max_height, max_height = max_height, max(y for y in tower if tower[y])
        rocks_remaining = num_rocks - rock_num
        delta = max_height - last_max_height
        deltas.append(delta)

        for n in range(2, len(deltas) // 2):
            # Check if the last 3 sets of n cycles match
            if deltas[-n:] == deltas[-2 * n : -n] == deltas[-3 * n : -2 * n]:
                repeat_size = sum(deltas[-n:])
                repeats_remaining = rocks_remaining // (cycle_size * n)
                rocks_after_last_repeat = rocks_remaining % (cycle_size * n)
                size_of_partial_repeat = sum(deltas[-n : -n + rocks_after_last_repeat // cycle_size])
                print("part 2:", max_height + repeat_size * repeats_remaining + size_of_partial_repeat)
                exit()
