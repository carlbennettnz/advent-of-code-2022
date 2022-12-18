let input = require('fs').readFileSync('../in/01.txt', 'utf8')

console.log('part 1:', input.split('\n').reduce(([best, curr], line) => line ? [best, curr + 1 * line] : [Math.max(best, curr), 0], [0,0])[0])
console.log('part 2:', input.split('\n').reduce(([totals, curr], line) => line ? [totals, curr + 1 * line] : [[...totals, curr], 0], [[],0])[0].sort((a, b) => b - a).slice(0, 3).reduce((x, y) => x + y))
