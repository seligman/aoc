#!/usr/bin/env python3

DAY_NUM = 14
DAY_DESC = 'Day 14: Parabolic Reflector Dish'

def calc(log, values, mode):
    # TODO: Delete or use these
    # from parsers import get_ints, get_floats
    from grid import Grid, Point
    grid = Grid.from_text(values)
    # from program import Program
    # program = Program(values)
    from collections import Counter

    if mode == 1:
        start = grid.axis_max(1)
        for x in grid.x_range():
            y = start
            while True:
                change = False
                for y in range(start, 0, -1):
                    if grid[x, y] == "O" and grid[x, y - 1] == ".":
                        grid[x, y] = "."
                        grid[x, y - 1] = "O"
                        change = True
                if not change:
                    break
    else:
        step = 0
        step_skip = 0
        seen = {}
        while True:
            for rot in range(4):
                while True:
                    change = False
                    for (x, y), val in list(grid.grid.items()):
                        if val == "O":
                            if rot == 0: pt = (x, y - 1)
                            elif rot == 1: pt = (x - 1, y)
                            elif rot == 2: pt = (x, y + 1)
                            elif rot == 3: pt = (x + 1, y)
                            if grid[pt] == ".":
                                grid[x, y], grid[pt] = ".", "O"
                                change = True
                    if not change:
                        break

            ret = 0
            for (x, y), val in grid.grid.items():
                if val == "O":
                    ret += grid.axis_max(1) - y + 1
            
            val = grid.dump_grid()
            if val in seen:
                rule = (step, seen[val][0])
                x = ((1000000000 - rule[0]) % (rule[1] - rule[0])) + rule[0] - 1
                for a, b in seen.items():
                    if b[0] == x:
                        return b[1]

            seen[val] = (step, ret)
            step += 1

    ret = 0
    for (x, y), val in grid.grid.items():
        if val == "O":
            ret += start - y + 1
    return ret

def test(log):
    values = log.decode_values("""
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
    """)

    log.test(calc(log, values, 1), '136')
    log.test(calc(log, values, 2), '64')

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
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
