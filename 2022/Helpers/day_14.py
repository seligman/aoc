#!/usr/bin/env python3

DAY_NUM = 14
DAY_DESC = 'Day 14: Regolith Reservoir'

def calc(log, values, mode):
    from grid import Grid, Point
    grid = Grid()

    for row in values:
        last = None
        for xy in row.split(" -> "):
            xy = xy.split(",")
            pt = Point(int(xy[0]), int(xy[1]))
            if last is not None:
                if pt.x == last.x:
                    for y in range(min(pt.y, last.y), max(pt.y, last.y)+1):
                        grid[(pt.x, y)] = "#"
                elif pt.y == last.y:
                    for x in range(min(pt.x, last.x), max(pt.x, last.x)+1):
                        grid[(x, pt.y)] = "#"
            last = pt
    
    max_y = max(grid.y_range())

    ret = -1
    while True:
        ret += 1
        pt = Point(500, 0)
        if grid[pt] == "#":
            break
        
        found = None
        while True:
            if mode == 1:
                if pt.y > max_y:
                    return ret
            else:
                if pt.y == max_y + 1:
                    break
            good = False
            for d in [(0, 1), (-1, 1), (1, 1)]:
                if grid[pt + d] != "#":
                    good = True
                    pt = pt + d
                    break
            if not good:
                break
        grid[pt] = "#"

    return ret

def test(log):
    values = log.decode_values("""
        498,4 -> 498,6 -> 496,6
        503,4 -> 502,4 -> 502,9 -> 494,9
    """)

    log.test(calc(log, values, 1), 24)
    log.test(calc(log, values, 2), 93)

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
