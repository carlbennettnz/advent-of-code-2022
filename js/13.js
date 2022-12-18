
let input = require('fs').readFileSync('13.txt', 'utf8')
let a = [[2]]
let b = [[6]]
let compare = (a, b) => (a, b) => typeof a === 'number' && typeof b === 'number' ? a - b : (Array.isArray(a) ? a : [a])
    .find((ai, i) => compare(ai, (Array.is))
[...input.trim().split('\n').filter(x => x).map(JSON.parse), a, b]
.sort(