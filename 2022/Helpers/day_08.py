#!/usr/bin/env python3

DAY_NUM = 8
DAY_DESC = 'Day 8: Treetop Tree House'

def calc(log, values, mode):
    from grid import Grid
    grid = Grid.from_text(values)
    grid.default = None

    count = 0
    best = 0

    for x in grid.x_range():
        for y in grid.y_range():
            good = True
            dist_value = 1
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                dist = 0
                good = True
                start = grid[(x,y)]
                ox, oy = x + dx, y + dy
                while grid[(ox, oy)] is not None:
                    dist += 1
                    if grid[(ox, oy)] >= start:
                        good = False
                        break
                    ox, oy = ox + dx, oy + dy
                dist_value *= dist
                if good and mode == 1:
                    break
            if mode == 2:
                best = max(best, dist_value)
            if good:
                count += 1

    if mode == 1:
        return count
    else:
        return best

def test(log):
    values = log.decode_values("""
        30373
        25512
        65332
        33549
        35390
    """)

    log.test(calc(log, values, 1), 21)
    log.test(calc(log, values, 2), 8)

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
