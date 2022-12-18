// let input = require('fs').readFileSync('11s.txt', 'utf8')
let input = require('fs').readFileSync('11.txt', 'utf8')

let monkeys = input.split('\n\n').map(config => {
    const [name, items, operation, test, ifTrue, ifFalse] = config.split('\n')
    return {
        items: items.match(/\d+/g).map(Number),
        operation: {
            'new = old * 19': (n) => n * 19,
            'new = old * old': (n) => n * n,
            'new = old + 2': (n) => n + 2,
            'new = old + 3': (n) => n + 3,
            'new = old + 4': (n) => n + 4,
            'new = old + 6': (n) => n + 6,
            'new = old + 7': (n) => n + 7,
            'new = old + 8': (n) => n + 8,
            'new = old * 3': (n) => n * 3,
        }[operation.match(/new = .*/)[0]],
        test: test.match(/\d+/)[0],
        ifTrue: 1*ifTrue.match(/\d+/)[0],
        ifFalse: 1*ifFalse.match(/\d+/)[0],
        count: 0,
    }
})

let commonMultiple = monkeys.map(m => m.test).reduce((t, x) => t*x, BigInt(1))

for (let round = 0; round < 10000; round++) {
    for (let monkey of monkeys) {
        for (let item of monkey.items) {
            let worryLevel = monkey.operation(item)
            let dest = worryLevel % monkey.test === 0 ? monkey.ifTrue : monkey.ifFalse
            monkeys[dest].items.push(worryLevel % commonMultiple)
            monkey.count++
        }
        monkey.items = []
    }
}

console.log(monkeys.map(m => m.count))
console.log(monkeys.sort((a, b) => b.count - a.count).slice(0, 2).map(monkey => monkey.count).reduce((score, x) => score * x, 1))