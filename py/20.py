class Number:
    def __init__(self, n: str):
        self.n = int(n)


input = [int(line) for line in open("../in/20.txt", "r").read().split("\n")]
print(input)


def unmix(numbers):
    numbers = list(map(Number, numbers))
    to_move = numbers.copy()

    for number in to_move:
        index = numbers.index(number)

        if number.n >= 0:
            new_index = (index + number.n + 1) % (len(numbers) - 1) - 1
        else:
            new_index = (index + number.n - 1) % (len(numbers) - 1) + 1

        if number.n:
            # print(f"{number.n=}, {index=}, {new_index=}")
            # print([n.n for n in numbers])
            del numbers[index]
            numbers.insert(new_index, number)
            # print([n.n for n in numbers])

    return [n.n for n in numbers]


def test(before, after):
    unmixed = unmix(before)
    if unmixed != after:
        print(f"expected unmix({before}) == {unmixed} == {after}")
        exit(1)


test([1, 0, 0, 0], [0, 1, 0, 0])
test([0, 0, 0, 1], [0, 1, 0, 0])
test([0, 0, -1, 0], [0, -1, 0, 0])
test([0, -1, 0, 0], [0, 0, 0, -1])
test([0, -2, 0, 0], [0, 0, -2, 0])
print("==== ACTUAL ====")
# test(input, [1, 2, -3, 4, 0, 3, -2])

unmixed = unmix(input)
zero_index = unmixed.index(0)
print(
    unmixed[(zero_index + 1000) % len(unmixed)]
    + unmixed[(zero_index + 2000) % len(unmixed)]
    + unmixed[(zero_index + 3000) % len(unmixed)]
)
