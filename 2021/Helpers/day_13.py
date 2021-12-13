#!/usr/bin/env python3

def get_desc():
    return 13, 'Day 13: Transparent Origami'

def calc(log, values, mode):
    from grid import Grid
    grid = Grid()
    for cur in values:
        if "," in cur:
            cur = tuple(int(x) for x in cur.split(","))
            grid[cur] = "#"
        elif cur.startswith("fold along x="):
            cur = int(cur[13:])
            for x,y in list(grid.grid):
                if x >= cur:
                    grid[(cur - 1) - (x - cur)+1, y] = "#"
                    del grid.grid[(x, y)]
            if mode == 1:
                break
        elif cur.startswith("fold along y="):
            cur = int(cur[13:])
            for x,y in list(grid.grid):
                if y >= cur:
                    grid[x, (cur - 1) - (y - cur)+1] = "#"
                    del grid.grid[(x, y)]
            if mode == 1:
                break

    if mode == 2:
        grid.show_grid(log)

    return len([x for x in grid.grid.values() if x == "#"])

def test(log):
    values = log.decode_values("""
        6,10
        0,14
        9,10
        0,3
        10,4
        4,11
        6,0
        6,12
        4,1
        0,13
        10,12
        3,4
        3,0
        8,4
        1,10
        2,14
        8,10
        9,0

        fold along y=7
        fold along x=5
    """)

    log.test(calc(log, values, 1), 17)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))
