import string
import networkx

input = open("../in/12.txt", "r").read()

DG = networkx.DiGraph()
grid = []
starts = []

# parse
for y, row in enumerate(input.split("\n")):
    grid.append([])
    for x, p in enumerate(row):
        if p in ("S", "a"):
            starts.append((x, y))

        if p == "S":
            start = (x, y)
            grid[y].append(0)
        elif p == "E":
            end = (x, y)
            grid[y].append(26)
        else:
            grid[y].append(string.ascii_lowercase.index(p))

# add nodes
for y, row in enumerate(grid):
    for x, p in enumerate(row):
        DG.add_node((x, y))

# add edges
for y, row in enumerate(grid):
    for x, p in enumerate(row):
        if 0 < x and row[x - 1] - p <= 1:
            DG.add_edge((x, y), (x - 1, y))

        if x < len(row) - 1 and row[x + 1] - p <= 1:
            DG.add_edge((x, y), (x + 1, y))

        if 0 < y and grid[y - 1][x] - p <= 1:
            DG.add_edge((x, y), (x, y - 1))

        if y < len(grid) - 1 and grid[y + 1][x] - p <= 1:
            DG.add_edge((x, y), (x, y + 1))


def dist(start, end):
    try:
        return len(networkx.shortest_path(DG, source=start, target=end)) - 1
    except:
        return float("inf")


print("part 1:", len(networkx.shortest_path(DG, source=start, target=end)) - 1)
print("part 2:", min(dist(s, end) for s in starts))
