#!/usr/bin/env python3

DAY_NUM = 18
DAY_DESC = 'Day 18: Boiling Boulders'

from collections import deque

def calc(log, values, mode):
    from parsers import get_ints
    from grid import Grid

    seen = []
    grid = Grid()

    for cur in values:
        x, y, z = get_ints(cur)
        seen.append((x, y, z))
        grid[(x, y, z)] = "#"

    grid[(-1, -1, -1)] = 0
    grid[(max(x for x,y,z in seen)+1, max(y for x,y,z in seen)+1, max(z for x,y,z in seen)+1)] = 0

    def all_edges(x, y, z):
        for ox, oy, oz in [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]:
            yield (x + ox, y + oy, z + oz)

    if mode == 1:
        ret = 0
        for pt in seen:
            for pt in all_edges(*pt):
                if grid[pt] == 0:
                    ret += 1
        return ret

    if mode == 2:
        todo = [(-1, -1, -1)]
        used = set(todo)
        escapes_cube = set(todo)

        def in_axis(val, axis):
            return grid.axis_min(axis) <= val <= grid.axis_max(axis)

        while len(todo) > 0:
            pt = todo.pop(0)
            for pt in all_edges(*pt):
                if pt not in used:
                    used.add(pt)
                    if in_axis(pt[0], 0) and in_axis(pt[1], 1) and in_axis(pt[2], 2) and grid[pt] == 0:
                        escapes_cube.add(pt)
                        todo.append(pt)

        ret = 0
        for pt in seen:
            for pt in all_edges(*pt):
                if pt in escapes_cube:
                    ret += 1
        return ret

    return sum(x[3] for x in seen)

def test(log):
    values = log.decode_values("""
        2,2,2
        1,2,2
        3,2,2
        2,1,2
        2,3,2
        2,2,1
        2,2,3
        2,2,4
        2,2,6
        1,2,5
        3,2,5
        2,1,5
        2,3,5
    """)

    log.test(calc(log, values, 1), 64)
    log.test(calc(log, values, 2), 58)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in [[], ["Puzzles"], ["..", "Puzzles"]]:
                cur = os.path.join(*(dn + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!"); exit(1)
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
