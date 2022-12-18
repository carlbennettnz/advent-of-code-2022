import re
from typing import NamedTuple
from util import Vector
from intervaltree import IntervalTree

# input = open("../in/15s.txt", "r").read()
# line_of_interest = 10
input = open("../in/15.txt", "r").read()
line_of_interest = 2000000


class Sensor(NamedTuple):
    x: int
    y: int
    radius: int

    @property
    def fw(self):  # "forwards [slash]", where a line going up and right from this point intersects y=0
        return self.x + self.y - 1

    @property
    def bw(self):  # "backwards [slash]", where a line going up and left from this point intersects y=0
        return self.x - self.y + 1

    def in_range(self, p):
        return abs(self.x - p.x) + abs(self.y - p.y) <= self.radius


sensors = []
beacons = set()
covered = IntervalTree()
fw_lines = set()
bw_lines = set()
limit = 4_000_000

# parse
for line in input.strip().split("\n"):
    sx, sy, bx, by = [int(n) for n in re.findall(r"-?\d+", line)]
    radius = abs(sx - bx) + abs(sy - by)
    sensors.append(Sensor(sx, sy, radius))
    beacons.add(Vector(bx, by))

# scan the line of interest
for sensor in sensors:
    horizontal_coverage = sensor.radius - abs(sensor.y - line_of_interest)

    if horizontal_coverage >= 0:
        covered[sensor.x - horizontal_coverage : sensor.x + horizontal_coverage + 1] = True

covered.merge_overlaps()
points_covered = sum(interval.end - interval.begin for interval in covered.items())
beacon_covered = len([b for b in beacons if b.y == line_of_interest])
print("part 1:", points_covered - beacon_covered)

# find 1 pixel wide gaps between sensors
for a in sensors:
    for b in sensors:
        if abs(a.fw - b.fw) - a.radius - b.radius == 2:
            fw_lines.add(a.fw + a.radius + 1)

        if abs(a.bw - b.bw) - a.radius - b.radius == 2:
            bw_lines.add(a.bw + a.radius + 1)

# check the intersections of our diagonal lines to find the one in bounds and not seen by a sensor
for fw in fw_lines:
    for bw in bw_lines:
        x = (fw + bw) // 2
        y = (fw - bw) // 2 + 1
        p = Vector(x, y)

        if 0 <= p.x <= limit and 0 <= p.y <= limit:
            if not any(sensor.in_range(p) for sensor in sensors):
                print("part 2:", p.x * limit + p.y)
