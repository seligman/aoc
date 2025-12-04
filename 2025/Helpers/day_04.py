#!/usr/bin/env python3

DAY_NUM = 4
DAY_DESC = 'Day 4: Printing Department'

def calc(log, values, mode):
    from grid import Grid, Point
    grid = Grid.from_text(values)

    ret = 0
    while True:
        to_remove = []
        for xy in grid.xy_range():
            xy = Point(xy)
            if grid[xy] == "@":
                total = 0
                for oxy in Grid.get_dirs(2):
                    oxy = Point(oxy)
                    if grid[xy + oxy] == "@":
                        total += 1
                if total < 4:
                    ret += 1
                    to_remove.append(xy)
        if mode == 1 or len(to_remove) == 0:
            break
        for xy in to_remove:
            grid[xy] = "."

    return ret

def test(log):
    values = log.decode_values("""
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.

    """)

    log.test(calc(log, values, 1), '13')
    log.test(calc(log, values, 2), '43')

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
