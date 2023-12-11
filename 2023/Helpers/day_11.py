#!/usr/bin/env python3

DAY_NUM = 11
DAY_DESC = 'Day 11: Cosmic Expansion'

def calc(log, values, mode):
    from grid import Grid, Point
    grid = Grid.from_text(values)

    temp = Grid()
    empty_col = []
    empty_row = []

    for x in grid.x_range():
        if sum(0 if grid[x, y] == "." else 1 for y in grid.y_range()) == 0:
            empty_col.append(x)
    for y in grid.y_range():
        if sum(0 if grid[x, y] == "." else 1 for x in grid.x_range()) == 0:
            empty_row.append(y)
    
    stars = []
    for (x, y), val in grid.grid.items():
        if val == "#":
            stars.append((x, y))

    ret = 0
    for i in range(len(stars)):
        for j in range(i + 1, len(stars)):
            ax, ay = stars[i]
            bx, by = stars[j]

            ax, bx = min(ax, bx), max(ax, bx)
            ay, by = min(ay, by), max(ay, by)

            count = 0
            count -= 1
            for x in range(ax, bx + 1):
                if x in empty_col:
                    count += 1 if mode == 1 else (1000000 - 1)
                count += 1
            count -= 1
            for y in range(ay, by + 1):
                if y in empty_row:
                    count += 1 if mode == 1 else (1000000 - 1)
                count += 1
            ret += count

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

    log.test(calc(log, values, 1), 'TODO')
    log.test(calc(log, values, 2), 'TODO')

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
