#!/usr/bin/env python3

DAY_NUM = 11
DAY_DESC = 'Day 11: Cosmic Expansion'

def calc(log, values, mode):
    import itertools
    from grid import Grid

    grid = Grid.from_text(values)

    empty_col = set(x for x in grid.x_range() if set(grid.column(x)) == {"."})
    empty_row = set(y for y in grid.y_range() if set(grid.row(y)) == {"."})
    
    stars = [pt for pt, val in grid.grid.items() if val == "#"]
    range_sets = {}

    def get_range_set(a, b):
        ret = range_sets.get((a, b), None)
        if ret is None:
            ret = set(range(a, b))
            range_sets[(a, b)] = ret
        return ret

    ret = 0
    mult = 1 if mode == 1 else (1000000 - 1)
    for (ax, ay), (bx, by) in itertools.combinations(stars, 2):
        ax, bx = min(ax, bx), max(ax, bx)
        ay, by = min(ay, by), max(ay, by)

        ret += (bx - ax) + len(empty_col & get_range_set(ax, bx + 1)) * mult
        ret += (by - ay) + len(empty_row & get_range_set(ay, by + 1)) * mult

    return ret

def test(log):
    values = log.decode_values("""
        ...#......
        .......#..
        #.........
        ..........
        ......#...
        .#........
        .........#
        ..........
        .......#..
        #...#.....
    """)

    log.test(calc(log, values, 1), '374')
    log.test(calc(log, values, 2), '82000210')

def run(log, values):
    log(f"Part 1: {calc(log, values, 1)}")
    log(f"Part 2: {calc(log, values, 2)}")

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2023/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
