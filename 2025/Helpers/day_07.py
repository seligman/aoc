#!/usr/bin/env python3

DAY_NUM = 7
DAY_DESC = 'Day 7: Laboratories'

from functools import cache

_grid = None
_seen = None

def other_draw(describe, values):
    if describe:
        return "Draw this"
    from dummylog import DummyLog
    import animate
    animate.prep()
    calc(DummyLog(), values, 1, draw=True)
    animate.create_mp4(DAY_NUM, rate=15, final_secs=5)

_helper = None
@cache
def dest_count_cached(pt):
    return dest_count(pt)

def dest_count(pt):
    from grid import Grid, Point
    ret = 1
    while True:
        pt += Point(0, 1)
        if _seen is not None and pt in _seen:
            break

        if _seen is not None:
            _seen.add(pt)
        if _grid[pt] == "^":
            ret += _helper(pt + Point(1, 0)) - 1
            ret += _helper(pt + Point(-1, 0)) 
            break
        elif _grid[pt] == ".":
            pass
        else:
            break
    return ret

def calc(log, values, mode, draw=False):
    from grid import Grid, Point
    grid = Grid.from_text(values)
    global _grid
    _grid = grid
    for xy in grid.xy_range(as_point=True):
        if grid[xy] == "S":
            start = xy

    if draw:
        grid.save_frame()
        pts = [start]
        seen = set()
        while True:
            grid.save_frame()
            todo = []
            for pt in pts:
                if pt not in seen:
                    seen.add(pt)
                    pt += Point(0, 1)
                    if grid[pt] == "^":
                        grid[pt] = "|"
                        todo.append(pt + Point(1, 0))
                        todo.append(pt + Point(-1, 0))
                        pass
                    elif grid[pt] == ".":
                        grid[pt] = "|"
                        todo.append(pt)
            if len(todo) == 0:
                break
            pts = todo
        grid.draw_frames(color_map={"^": (0, 255, 0), ".": (0, 0, 0), "|": (255, 96, 0)})
        return

    global _seen, _helper
    if mode == 1:
        if draw:
            grid.save_frame()
        _seen = set()
        _helper = dest_count
        ret = dest_count(start) - 1
        if draw:
            grid.draw_frames(color_map={"^": (0, 255, 0), ".": (0, 0, 0), "|": (255, 96, 0)})
        return ret
    else:
        _seen = None
        _helper = dest_count_cached
        return dest_count_cached(start)

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
