class Number:
    def __init__(self, n: str):
        self.n = int(n)


input = [int(line) for line in open("../in/20.txt", "r").read().split("\n")]


def unmix(numbers, iterations=1):
    numbers = list(map(Number, numbers))
    to_move = numbers.copy()

    for i in range(iterations):
        for number in to_move:
            index = numbers.index(number)

            if number.n >= 0:
                new_index = (index + number.n + 1) % (len(numbers) - 1) - 1
            else:
                new_index = (index + number.n - 1) % (len(numbers) - 1) + 1

            if number.n:
                del numbers[index]
                numbers.insert(new_index, number)

    return [n.n for n in numbers]


unmixed = unmix(input)
zero_index = unmixed.index(0)
print(
    "part 1:",
    unmixed[(zero_index + 1000) % len(unmixed)]
    + unmixed[(zero_index + 2000) % len(unmixed)]
    + unmixed[(zero_index + 3000) % len(unmixed)],
)

unmixed = unmix([n * 811589153 for n in input], 10)
zero_index = unmixed.index(0)
print(
    "part 2:",
    unmixed[(zero_index + 1000) % len(unmixed)]
    + unmixed[(zero_index + 2000) % len(unmixed)]
    + unmixed[(zero_index + 3000) % len(unmixed)],
)
