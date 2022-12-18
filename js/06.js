let input = require('fs').readFileSync('../in/06.txt', 'utf8')

console.log('part 1:', input.split('').findIndex((c, i, a) => new Set(a.slice(i, i + 4)).size === 4) + 4)
console.log('part 2:', input.split('').findIndex((c, i, a) => new Set(a.slice(i, i + 14)).size === 14) + 14)
