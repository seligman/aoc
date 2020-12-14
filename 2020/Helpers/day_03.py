#!/usr/bin/env python3

def get_desc():
    return 3, 'Day 3: Toboggan Trajectory'

def calc(log, values, mode):
    from grid import Grid
    grid = Grid.from_text(values)
    ret = []

    if mode == 1:
        passes = [[3,1]]
    else:
        passes = [[1,1],[3,1],[5,1],[7,1],[1,2]]
    for step_x, step_y in passes:
        ret.append(0)
        x, y = 0, 0 
        while True:
            x += step_x
            y += step_y
            x = x % grid.width()
            if y >= grid.height():
                break
            if grid[x, y] == "#":
                ret[-1] += 1

    value = 1
    for x in ret:
        value *= x

    return value

def test(log):
    values = log.decode_values("""
        ..##.......
        #...#...#..
        .#....#..#.
        ..#.#...#.#
        .#...##..#.
        ..#.##.....
        .#.#.#....#
        .#........#
        #.##...#...
        #...##....#
        .#..#...#.#
    """)

    log.test(calc(log, values, 1), 7)
    log.test(calc(log, values, 2), 336)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))
