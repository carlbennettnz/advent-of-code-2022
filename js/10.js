let input = require('fs').readFileSync('../in/10.txt', 'utf8')

console.log(input.trim().split('\n').flatMap(line => line === "noop" ? [line] : ['noop', line]).reduce(([total, register], line, cycle) => [(cycle + 21) % 40 ? total : total + (cycle + 1) * register, line.startsWith('addx') ? register + 1*line.split(' ')[1] : register], [0, 1])[0])
console.log(input.trim().split('\n').flatMap(line => line === "noop" ? [line] : ['noop', line]).reduce(([crt, register], line, cycle) => [Object.values({...crt, [cycle]: Math.abs(register - cycle % 40) <= 1 ? '#' : '.'}), line.startsWith('addx') ? register + 1*line.split(' ')[1] : register], [Array(240).fill('.'), 1])[0].reduce((output, pixel, i) => i % 40 ? output + pixel : output + '\n' + pixel, ''))
