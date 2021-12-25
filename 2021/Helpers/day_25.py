#!/usr/bin/env python3

def get_desc():
    return 25, 'Day 25: Sea Cucumber'

def calc(log, values, mode):
    from grid import Grid
    grid = Grid.from_text(values)

    w, h = grid.width(), grid.height()
    steps = 1
    while True:
        count = 0
        moved = Grid(default=".")
        for xy, val in grid.grid.items():
            if val == ">":
                nxy = (xy[0] + 1) % w, xy[1]
                if grid[nxy] == ".":
                    moved[nxy] = ">"
                    count += 1
                else:
                    moved[xy] = ">"
            elif val == "v":
                moved[xy] = val
        moved, grid = Grid(default="."), moved
        for xy, val in grid.grid.items():
            if val == "v":
                nxy = xy[0], (xy[1] + 1) % h
                if grid[nxy] == ".":
                    moved[nxy] = "v"
                    count += 1
                else:
                    moved[xy] = "v"
            elif val == ">":
                moved[xy] = val
        grid = moved
        if count == 0:
            return steps
        steps += 1

def test(log):
    values = log.decode_values("""
        v...>>.vv>
        .vv>>.vv..
        >>.>v>...v
        >>v>>.>.v.
        v>v.vv.v..
        >.>>..v...
        .vv..>.>v.
        v.v..>>v.v
        ....v..v.>
    """)

    log.test(calc(log, values, 1), 58)

def run(log, values):
    log(calc(log, values, 1))
