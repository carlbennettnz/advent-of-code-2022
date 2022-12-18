// let input = require('fs').readFileSync('12s.txt', 'utf8')
let input = require('fs').readFileSync('12.txt', 'utf8')
let pf = require('pathfinding')

let letters = 'abcdefghijklmnopqrstuvwxyz'

let start = null
let dest = null
let grid = input.trim().split('\n').map(line => line.split('').map(point => letters[point] ?? point))
let coords = grid.flatMap((row, y) => row.map((_, x) => [x, y]))

for (let [x, y] of coords) {
    if (grid[y][x] === 'S') {
        start = [x, y]
        grid[y][x] = 0
    } else if (grid[y][x] === 'E') {
        dest = [x, y]
        grid[y][x] = 26
    } else {
        grid[y][x] = letters.indexOf(grid[y][x])
        console.log(x, y, grid[y][x])
    }
}

let loc = [...start]
let path = []
let subpath = []
let steps = 0

while (grid[loc[1]][loc[0]] < 26) {
    let vector = [dest[0] - loc[0], dest[1] - loc[1]]
    let [x, y] = loc
    let level = grid[y][x]

    let targets = coords
        .filter(([x, y]) => grid[y][x] === level + 1)
        .map(([x, y]) => [[x, y], Math.sqrt(Math.abs(x - dest[0])**2 + Math.abs(y - dest[1])**2)])
        .sort((a, b) => a[1] - b[1])
        .map(([p, _]) => p)

    targets.push([134, 21])

    subpath = []
    while (!subpath.length && targets.length) {
        const [targetX, targetY] = targets.shift()
        let pfgrid = new pf.Grid(grid[y].length, grid.length)

        for (let [x, y] of coords) {
            pfgrid.setWalkableAt(x, y, grid[y][x] === level || grid[y][x] === level + 1)
        }

        let finder = new pf.AStarFinder()
        console.log({x, y, targetX, targetY})
        // let visual = Array(grid.length).fill().map(_ => Array(grid[0].length).fill('.'))
        // for (let [x, y] of coords) {
        //     if (pfgrid.isWalkableAt(x, y)) visual[y][x] = '#'
        // }
        // console.log(visual[y][x])
        // console.log(visual[targetY][targetX])
        // visual[y][x] = 'F'
        // visual[targetY][targetX] = 'T'
        // console.log(visual.map(l => l.join('')).join('\n'))
        subpath = finder.findPath(x, y, targetX, targetY, pfgrid)
    }

    if (!subpath.length) {
        console.error('failed')
        break
    }

    console.log('subpath', subpath)

    loc = subpath.at(-1)
    path.push(...subpath.slice(1))
}

let visual = Array(grid.length).fill().map(_ => Array(grid[0].length).fill('.'))
let from = start

console.log('got to', path.at(-1), letters[grid[path.at(-1)[1]][path.at(-1)[0]]])

for (let [toX, toY] of path) {
    const [fromX, fromY] = from
    if (visual[fromY][fromX] !== '.') console.log('err', visual[fromY][fromX])
    if (toX > fromX) visual[fromY][fromX] = '>'
    else if (toX < fromX) visual[fromY][fromX] = '<'
    else if (toY > fromY) visual[fromY][fromX] = 'v'
    else if (toY < fromY) visual[fromY][fromX] = '^'
    from = [toX, toY]
}

for (let [x, y] of coords) {
    if (visual[y][x] !== '.') continue
    if (['o'].includes(letters[grid[y][x]])) visual[y][x] = letters[grid[y][x]]
}

visual[loc[1]][loc[0]] = '@'

console.log(visual.map(l => l.join('')).join('\n'))
console.log('steps', path.length)

grid[20][132] = '#'

// console.log(grid.map(l => l.map(p => p === 26 ? 'E' : letters[p] ?? p).join('')).join('\n'))
