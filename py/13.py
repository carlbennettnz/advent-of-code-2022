import json
from functools import cmp_to_key, reduce

input = open("../in/13.txt", "r").read()

packet_pairs = [
    [json.loads(side) for side in pair] for pair in [pair.split("\n") for pair in input.split("\n\n")]
]


def check(l, r, d=0):
    # print('  '*d + f'- Compare {l} vs {r}')

    if isinstance(l, int) and isinstance(r, int):
        return l - r
    else:
        l = [l] if isinstance(l, int) else l
        r = [r] if isinstance(r, int) else r

        for l2, r2 in zip(l, r):
            if comp := check(l2, r2, d + 1):
                return comp

        return len(l) - len(r)


print("part 1:", sum(i + 1 for i, (l, r) in enumerate(packet_pairs) if check(l, r) < 0))

packets = reduce(list.__add__, packet_pairs) + [[[2]], [[6]]]
packets.sort(key=cmp_to_key(check))

print("part 2:", (packets.index([[2]]) + 1) * (packets.index([[6]]) + 1))
