import re
from typing import NamedTuple

input = open("../in/15.txt", "r").read()


class Point(NamedTuple):
    x: int
    y: int


sensors = {}
limit = 4_000_000

for line in input.strip().split("\n"):
    sx, sy, bx, by = [int(n) for n in re.findall(r"-?\d+", line)]
    sensor = Point(sx, sy)
    distance_to_beacon = abs(sx - bx) + abs(sy - by)
    sensors[sensor] = distance_to_beacon

for y in range(0, limit + 1):
    ranges = []
    sorted_ranges = []

    for sensor, distance in sensors.items():
        horizontal_distance_allowed = distance - abs(sensor.y - y)
        if horizontal_distance_allowed >= 0:
            covered_from = max(0, sensor.x - horizontal_distance_allowed)
            covered_to = min(limit, sensor.x + horizontal_distance_allowed)
            if covered_from < covered_to:
                ranges.append((covered_from, covered_to))

    last_covered_x = 0
    for begin, end in sorted(ranges):
        if begin > last_covered_x:
            x = last_covered_x + 1
            print("got it", Point(x, y), x * limit + y)
            exit()
        else:
            last_covered_x = max(last_covered_x, end)

    if y % 10_000 == 0:
        print("nope", y)
