#!/usr/bin/env python3

import re

def get_desc():
    return 5, 'Day 5: Hydrothermal Venture'

def calc(log, values, mode):
    from grid import Grid
    grid = Grid()
    r = re.compile("(\d+),(\d+) -> (\d+),(\d+)")
    for cur in values:
        m = r.search(cur)
        if m:
            x1, y1, x2, y2 = int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))
            if x1 == x2 or y1 == y2 or mode == 2:
                x, y = x1, y1
                while True:
                    grid[x, y] += 1
                    if (x, y) == (x2, y2):
                        break
                    if x2 > x1: x += 1
                    elif x2 < x1: x -= 1
                    if y2 > y1: y += 1
                    elif y2 < y1: y -= 1
    return len([x for x in grid.grid.values() if x > 1])

def test(log):
    values = log.decode_values("""
        0,9 -> 5,9
        8,0 -> 0,8
        9,4 -> 3,4
        2,2 -> 2,1
        7,0 -> 7,4
        6,4 -> 2,0
        0,9 -> 2,9
        3,4 -> 1,4
        0,0 -> 8,8
        5,5 -> 8,2
    """)

    log.test(calc(log, values, 1), 5)
    log.test(calc(log, values, 2), 12)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))
