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

