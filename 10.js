// let input = require('fs').readFileSync('10s.txt', 'utf8')
let input = require('fs').readFileSync('10.txt', 'utf8')

let cycle = 0
let register = 1
let total = 0
let crt = Array(240).fill('.')

for (let line of input.trim().split('\n')) {
    if (line === "noop") {
        tick()
    } else {
        tick()
        tick()
        register += Number(line.split(' ')[1])
    }
}

function tick() {
    crt[cycle] = Math.abs(register - cycle % 40) <= 1 ? '#' : '.'
    cycle += 1

    if ((cycle + 20) % 40 === 0) {
        total += cycle * register
    }
}

console.log(total)

for (let l = 0; l < 240 / 40; l++) {
    console.log(crt.slice(l*40, l*40+40).join(''))
}

console.log(input.trim().split('\n').flatMap(line => line === "noop" ? [line] : ['noop', line]).reduce(([total, register], line, cycle) => [(cycle + 21) % 40 ? total : total + (cycle + 1) * register, line.startsWith('addx') ? register + 1*line.split(' ')[1] : register], [0, 1])[0])
console.log(input.trim().split('\n').flatMap(line => line === "noop" ? [line] : ['noop', line]).reduce(([crt, register], line, cycle) => [Object.values({...crt, [cycle]: Math.abs(register - cycle % 40) <= 1 ? '#' : '.'}), line.startsWith('addx') ? register + 1*line.split(' ')[1] : register], [Array(240).fill('.'), 1])[0].reduce((output, pixel, i) => i % 40 ? output + pixel : output + '\n' + pixel, ''))
