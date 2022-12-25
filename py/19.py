import itertools
import re
from enum import Enum
from typing import NamedTuple
from rich import print
import numpy as np


class Resource(Enum):
    ore = 0
    clay = 1
    obsidian = 2
    geode = 3


class Blueprint(NamedTuple):
    id: int
    costs: dict[Resource, dict[Resource, int]]


input = open("../in/19.txt", "r").read().strip().split("\n")
blueprints = []
for id, *costs in [map(int, re.findall(r"\d+", line)) for line in input]:
    blueprints.append(
        Blueprint(
            id=id,
            costs={
                Resource.ore: {Resource.ore: costs[0]},
                Resource.clay: {Resource.ore: costs[1]},
                Resource.obsidian: {Resource.ore: costs[2], Resource.clay: costs[3]},
                Resource.geode: {Resource.ore: costs[4], Resource.obsidian: costs[5]},
            },
        )
    )


class Option(NamedTuple):
    blueprint: Blueprint
    resources: dict[Resource, int]
    robots: dict[Resource, int]
    skipped: set[Resource]
    log: dict[int, Resource]

    def save(self):
        return Option(
            blueprint=self.blueprint,
            resources={r: self.resources[r] + self.robots[r] for r in Resource},
            robots=self.robots,
            skipped=self.skipped | {robot for robot in Resource if self.can_afford(robot)},
            log=self.log,
        )

    def buy(self, robot: Resource, tick: int):
        if robot not in self.skipped and self.can_afford(robot):
            robots = {**self.robots, robot: self.robots[robot] + 1}
            return Option(
                blueprint=self.blueprint,
                resources={
                    r: self.resources[r] - self.blueprint.costs[robot].get(r, 0) + self.robots[r]
                    for r in Resource
                },
                robots=robots,
                # Immediately skip any we'll never be able to save for because we don't have the robots
                skipped={
                    r
                    for r in Resource
                    if any(robots[r2] == 0 for r2 in self.blueprint.costs[r])
                    or r != Resource.geode
                    and robots[r] >= max(self.blueprint.costs[r2].get(r, 0) for r2 in Resource)
                },
                log={**self.log, tick: robot},
            )

    def can_afford(self, robot):
        return all(self.resources[r] >= self.blueprint.costs[robot].get(r, 0) for r in Resource)


score = 1
for blueprint in blueprints[:3]:
    print("#" * 50)
    print("BLUEPRINT", blueprint.id)
    print("#" * 50)
    options = [
        Option(
            blueprint,
            {r: 0 for r in Resource},
            {r: 1 if r is Resource.ore else 0 for r in Resource},
            skipped={Resource.obsidian, Resource.geode},
            log={},
        )
    ]

    for tick in range(1, 33):
        next_options = []

        for option in options:
            buys = [o for o in (option.buy(robot, tick) for robot in Resource) if o]
            next_options.extend(buys)

            # don't allow save if you can buy or have already skipped everything
            if len(buys) < 4 - len(option.skipped):
                next_options.append(option.save())

        options = sorted(
            next_options,
            key=lambda opt: sum((r.value + 1) ** 2 * q for r, q in opt.robots.items()),
            reverse=True,
        )[:200000]
        print(tick, len(options), max(o.resources[Resource.geode] for o in options))

    best = None
    for opt in options:
        if not best or opt.resources[Resource.geode] > best.resources[Resource.geode]:
            best = opt

    count = 0
    for opt in options:
        if all(opt.resources[r] <= best.resources[r] and opt.robots[r] <= best.robots[r] for r in Resource):
            count += 1

    score *= best.resources[Resource.geode]

    print(dict(resources=tuple(best.resources.values()), robots=tuple(best.robots.values()), excludable=count))


print(score)
