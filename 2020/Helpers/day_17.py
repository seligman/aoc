#!/usr/bin/env python3

def get_desc():
    return 17, 'Day 17: Conway Cubes'

def calc(log, values, mode):
    from grid import Grid
    grid = Grid(default=".")
    y = 0
    for cur in values:
        x = 0
        for cube in cur:
            grid[x, y, 0, 0] = cube
            x += 1
        y += 1

    start, stop = -1, len(values) + 1

    dirs = []
    for x in range(-1, 2):
        for y in range(-1, 2):
            for z in range(-1, 2):
                for a in [0] if mode == 1 else range(-1, 2):
                    if mode == 1:
                        if not (x == 0 and y == 0 and z == 0):
                            dirs.append((x, y, z, a))
                    else:
                        if not (x == 0 and y == 0 and z == 0 and a == 0):
                            dirs.append((x, y, z, a))
        
    actives = 0

    for _ in range(6):
        todo = []
        hit_start, hit_stop = False, False
        actives = 0
        for x in range(start, stop):
            for y in range(start, stop):
                for z in range(start, stop):
                    for a in [0] if mode == 1 else range(start, stop):
                        temp = 0
                        for xo, yo, zo, ao in dirs:
                            if grid[x+xo, y+yo, z+zo, a+ao] == "#":
                                temp += 1
                        if grid[x, y, z, a] == "#":
                            if temp in {2, 3}:
                                todo.append((x, y, z, a, "."))
                            else:
                                actives += 1
                        elif grid[x, y, z, a] == "." and temp == 3:
                            todo.append((x, y, z, a, "#"))
                            actives += 1
                            if x == start or y == start or z == start or a == start:
                                hit_start = True
                            if x == stop - 1 or y == stop - 1 or z == stop - 1 or a == stop - 1:
                                hit_stop = True

        if hit_start:
            start -= 1
        if hit_stop:
            stop += 1

        for x, y, z, a, value in todo:
            grid[x, y, z, a] = value

    return actives

def test(log):
    values = log.decode_values("""
        .#.
        ..#
        ###
    """)

    log.test(calc(log, values, 1), 112)
    log.test(calc(log, values, 2), 848)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))
