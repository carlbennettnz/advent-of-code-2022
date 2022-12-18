let input = require('fs').readFileSync('../in/03.txt', 'utf8')

console.log('part 1:', input.trim().split('\n').flatMap(line => line.split('').filter((item, i) => i < line.length / 2 && !line.slice(0, i).includes(item) && line.slice(line.length / 2).includes(item)).map(item => item.charCodeAt(0)).map(item => item > 96 ? item - 96 : item - 64 + 26)).reduce((a, b) => a + b))
console.log('part 2:', input.trim().split('\n').flatMap((line, i, arr) => i % 3 === 2 ? [line.split('').find(item => arr[i - 1].includes(item) && arr[i - 2].includes(item))] : []).map(item => item.charCodeAt(0)).map(item => item > 96 ? item - 96 : item - 64 + 26).reduce((a, b) => a + b))

