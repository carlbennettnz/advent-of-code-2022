input = open("../in/25.txt", "r").read().strip().split("\n")

neg_map = {"-": -1, "=": -2}
decimal_to_snafu_digit = {
    0: ("0", 0),
    1: ("1", 0),
    2: ("2", 0),
    3: ("=", 1),
    4: ("-", 1),
}


def to_decimal(snafu: str) -> int:
    digits = [neg_map.get(digit) if digit in neg_map else int(digit) for digit in snafu]
    value = 0

    for i, digit in enumerate(digits[::-1]):
        value += 5**i * digit

    return value


def to_snafu(value: int) -> str:
    print(f"{value=}")
    snafu = ""
    carry = 0
    i = 1

    while value + carry:
        value_in_place_pre_carry = value % 5

        if value_in_place_pre_carry == 4 and carry:
            digit, carry = "0", 1
        else:
            digit, carry = decimal_to_snafu_digit[value_in_place_pre_carry + carry]
        snafu = digit + snafu
        print(f"{snafu=}, {value=}, {value_in_place_pre_carry=}, {carry=}, {5**i=}")
        value //= 5
        i += 1

    return snafu


s = sum(to_decimal(snafu) for snafu in input)
print(to_snafu(s))

# n = 0
# while True:
#     n += 1
#
#     if to_decimal(to_snafu(n)) != n:
#         print(n)
#         break
