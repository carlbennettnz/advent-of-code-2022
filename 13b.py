import json
from functools import cmp_to_key

input = open('13.txt', 'r').read()

input = [pair.split('\n') for pair in input.split('\n\n')]
packets = []

for pair in input:
    for side in pair:
        packets.append(json.loads(side))

a = [[2]]
b = [[6]]
packets.append(a)
packets.append(b)

def check(l, r, d=0):
    print('  '*d + f'- Compare {l} vs {r}')

    if isinstance(l, int) and isinstance(r, int):
        return l - r
    else:
        if isinstance(l, int):
            l = [l]

        if isinstance(r, int):
            r = [r]

        for l2, r2 in zip(l, r):
            comp = check(l2, r2, d+1)

            if comp:
                return comp

        return len(l) - len(r)

packets.sort(key=cmp_to_key(check))
print((packets.index(a)+1) * (packets.index(b) + 1))