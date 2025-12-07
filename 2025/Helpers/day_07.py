#!/usr/bin/env python3

DAY_NUM = 7
DAY_DESC = 'Day 7: Laboratories'

from functools import cache

_grid = None

@cache
def dest_count(start):
    from grid import Grid, Point
    todo = [start]
    ret = 1
    while len(todo) > 0:
        pt = todo.pop(0)
        while True:
            pt += Point(0, 1)
            if _grid[pt] == "^":
                ret += dest_count(pt + Point(1, 0)) - 1
                ret += dest_count(pt + Point(-1, 0)) 
                break
            elif _grid[pt] == ".":
                pass
            else:
                break
    return ret

def calc(log, values, mode):
    from grid import Grid, Point
    grid = Grid.from_text(values)
    global _grid
    _grid = grid
    for xy in grid.xy_range(as_point=True):
        if grid[xy] == "S":
            start = xy

    if mode == 1:
        ret = 0
        pts = [start]
        ret = 0
        seen = set()
        while True:
            todo = []
            for pt in pts:
                if pt not in seen:
                    seen.add(pt)
                    pt += Point(0, 1)
                    if grid[pt] == "^":
                        ret += 1
                        todo.append(pt + Point(1, 0))
                        todo.append(pt + Point(-1, 0))
                        pass
                    elif grid[pt] == ".":
                        todo.append(pt)
            if len(todo) == 0:
                break
            pts = todo
        return ret
    else:
        return dest_count(start)

def test(log):
    values = log.decode_values("""
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............

    """)

    log.test(calc(log, values, 1), '21')
    log.test(calc(log, values, 2), '40')

def run(log, values):
    log("Part 1")
    log(calc(log, values, 1))
    log("Part 2")
    log(calc(log, values, 2))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2024/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
