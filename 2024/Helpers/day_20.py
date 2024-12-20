#!/usr/bin/env python3

DAY_NUM = 20
DAY_DESC = 'Day 20: Race Condition'

from collections import deque   

def calc(log, values, mode, savings, cheats):
    from grid import Grid, Point
    grid = Grid.from_text(values, default="#")

    for xy in grid.xy_range():
        if grid[xy] == "S":
            start = xy
        elif grid[xy] == "E":
            stop = xy

    todo = deque([(start, 1, [start])])
    seen = set()
    while len(todo) > 0:
        xy, steps, path = todo.popleft()
        for o in grid.get_dirs(2, xy, False):
            if o not in seen:
                seen.add(o)
                if o == stop:
                    todo = []
                    break
                elif grid[o] == ".":
                    todo.append((o, steps + 1, path + [o]))

    path.append(stop)

    ret = 0
    path = [(i, x, y) for i, (x, y) in enumerate(path)]
    for i, x, y in path:
        min_x, max_x = x - cheats, x + cheats
        min_y, max_y = y - cheats, y + cheats
        for j, ox, oy in [(j, ox, oy) for j, ox, oy in path[i + 2 + savings:] if min_x <= ox <= max_x and min_y <= oy <= max_y]:
            dist = abs(x - ox) + abs(y - oy)
            if dist <= cheats and (j - i) - dist >= savings:
                ret += 1
    return ret

def test(log):
    values = log.decode_values("""
        ###############
        #...#...#.....#
        #.#.#.#.#.###.#
        #S#...#.#.#...#
        #######.#.#.###
        #######.#.#...#
        #######.#.###.#
        ###..E#...#...#
        ###.#######.###
        #...###...#...#
        #.#####.#.###.#
        #.#...#.#.#...#
        #.#.#.#.#.#.###
        #...#...#...###
        ###############
    """)

    log.test(calc(log, values, 1, 1, 2), '44')
    log.test(calc(log, values, 2, 50, 20), '285')

def run(log, values):
    log(calc(log, values, 1, 100, 2))
    log(calc(log, values, 2, 100, 20))

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
