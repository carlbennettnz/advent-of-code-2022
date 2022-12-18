let input = require('fs').readFileSync('../in/04.txt', 'utf8')

console.log('part 1:', input.trim().split('\n').map(line => line.match(/\d+/g).map(Number)).filter(([a1, a2, b1, b2]) => (a1 <= b1 && a2 >= b2) || (a1 >= b1 && a2 <= b2)).length)
console.log('part 2:', input.trim().split('\n').map(line => line.match(/\d+/g).map(Number)).filter(([a1, a2, b1, b2]) => a1 <= b2 && a2 >= b1).length)
