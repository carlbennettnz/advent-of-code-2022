let input = require('fs').readFileSync('../in/02.txt', 'utf8')

console.log('part 1:', input.trim().split('\n').map(line => line.split(' ').map(choice => ['A', 'B', 'C', 'X', 'Y', 'Z'].indexOf(choice) % 3)).map(([them, me]) => me + 1 + [3, 6, 0][(3 + me - them) % 3]).reduce((a, b) => a + b))
console.log('part 2:', input.trim().split('\n').map(line => line.split(' ').map(choice => ['A', 'B', 'C', 'X', 'Y', 'Z'].indexOf(choice) % 3)).map(([them, result]) => [(2 + them + result) % 3, result]).map(([me, result]) => me + 1 + [0, 3, 6][result]).reduce((a, b) => a + b))
