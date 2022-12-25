import re
import operator

ops = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.floordiv,
}
input = open("../in/21.txt", "r").read().strip()

monkeys = {}

for line in input.split("\n"):
    monkey, job = line.split(": ")

    if re.match(r"^\d+$", job):
        monkeys[monkey] = ("number", int(job))
    else:
        monkeys[monkey] = ("op", *job.split(" "))


def expr(monkey):
    match monkeys[monkey]:
        case "number", n:
            return n
        case "op", left, op, right:
            return ops[op](expr(left), expr(right))


print("part 1:", expr("root"))


def solve_for(cursor, target=None):
    if cursor not in monkeys:
        return target

    match monkeys[cursor]:
        case "number", n:
            return target
        case "op", left, op, right:
            try:
                left = expr(left)
            except:
                pass

            try:
                right = expr(right)
            except:
                pass

            match op:
                case "=":
                    if isinstance(left, int):
                        return solve_for(right, left)
                    else:
                        return solve_for(left, right)
                case "+":
                    if isinstance(left, int):
                        return solve_for(right, target - left)
                    else:
                        return solve_for(left, target - right)
                case "-":
                    if isinstance(left, int):
                        return solve_for(right, left - target)
                    else:
                        return solve_for(left, target + right)
                case "*":
                    if isinstance(left, int):
                        return solve_for(right, target // left)
                    else:
                        return solve_for(left, target // right)
                case "/":
                    if isinstance(left, int):
                        return solve_for(right, left // target)
                    else:
                        return solve_for(left, target * right)


monkeys["root"] = (*monkeys["root"][:2], "=", monkeys["root"][3])
del monkeys["humn"]
print("part 2:", solve_for("root"))
