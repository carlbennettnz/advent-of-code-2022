import json

input = open('13.txt', 'r').read()

input = [pair.split('\n') for pair in input.split('\n\n')]
packet_pairs = []

for pair in input:
    packet_pair = []
    for side in pair:
        packet_pair.append(json.loads(side))
    packet_pairs.append(packet_pair)

def check(l, r, d=0):
    print('  '*d + f'- Compare {l} vs {r}')
    if d > 10:
        raise RuntimeError('max depth')

    if isinstance(l, int) and isinstance(r, int):
        if l != r:
            return l < r
    else:
        if isinstance(l, int):
            l = [l]

        if isinstance(r, int):
            r = [r]

        for l2, r2 in zip(l, r):
            comp = check(l2, r2, d+1)

            if comp is not None:
                return comp

        if len(l) != len(r):
            return len(l) < len(r)

print(sum([i+1 if check(l, r) else 0 for i, (l, r) in enumerate(packet_pairs)]))