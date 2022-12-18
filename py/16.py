import dataclasses
import itertools
import networkx
import re

graph = networkx.Graph()
input = open("../in/16.txt", "r").read()
flow_rates = {}

for line in input.split("\n"):
    node, flow_rate, *tunnels = re.findall(r"\b[A-Z0-9]+\b", line)
    graph.add_node(node)
    flow_rates[node] = int(flow_rate)
    graph.add_edges_from([(node, other) for other in tunnels])


def get_options(location, closed_valves, nodes_to_visit):
    options = []

    if not closed_valves:
        options.append(("noop",))
    else:
        if location in closed_valves:
            options.append(("open",))

        options.extend(
            [("move", neighbour) for neighbour in graph.neighbors(location) if neighbour in nodes_to_visit]
        )

    return options


@dataclasses.dataclass
class Branch:
    paths: list[list[str]]
    debug: list[str]
    closed_valves: set[str]
    score: int


paths = {}

for from_node in graph.nodes:
    for to_node in graph.nodes:
        paths[(from_node, to_node)] = networkx.shortest_path(graph, from_node, to_node)[1:]

for part in range(1, 3):
    branches = [
        Branch(
            paths=[["AA"]] * part,
            closed_valves={valve for valve in graph.nodes if flow_rates[valve] > 0},
            score=0,
            debug=[],
        )
    ]

    for time_remaining in range([30, 26][part - 1], 0, -1):
        new_branches = []
        for branch in branches:
            nodes_to_visit = []
            for path_index, path in enumerate(branch.paths):
                nodes_to_visit.append(set())
                # record all nodes worth visiting, and prevent pointless double-back
                for valve_to_open in branch.closed_valves:
                    for node in paths[(path[-1], valve_to_open)]:
                        if node not in path:
                            nodes_to_visit[path_index].add(node)

            for options in itertools.product(
                *[
                    get_options(path[-1], branch.closed_valves, nodes_to_visit)
                    for path, nodes_to_visit in zip(branch.paths, nodes_to_visit)
                ]
            ):
                new_branch = dataclasses.replace(
                    branch,
                    paths=[path.copy() for path in branch.paths],
                    closed_valves=branch.closed_valves.copy(),
                    debug=branch.debug + [options],
                )
                new_branches.append(new_branch)

                for path_index, option in enumerate(options):
                    path = new_branch.paths[path_index]

                    match option:
                        case "move", new_location:
                            new_branch.paths[path_index].append(new_location)

                        case "open",:
                            if path[-1] in new_branch.closed_valves:
                                new_branch.closed_valves -= {path[-1]}
                                new_branch.score += flow_rates[path[-1]] * (time_remaining - 1)

                            new_branch.paths[path_index] = path[-1:]

        branches = sorted(new_branches, key=lambda b: -b.score)[0:5000]

    for minute, options in enumerate(branches[0].debug):
        print(f"{minute+1} | ".rjust(5) + " | ".join([" to ".join(option).ljust(10) for option in options]))

    print()
    print(f"part {part}:", branches[0].score)
    print()
