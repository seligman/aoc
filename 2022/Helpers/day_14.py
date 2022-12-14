#!/usr/bin/env python3

DAY_NUM = 14
DAY_DESC = 'Day 14: Regolith Reservoir'

def calc(log, values, mode, get_floor=False, floor=None, draw=False):
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

    if floor is not None:
        for x in floor:
            grid[(x, max_y + 2)] = "#"

    skip = 0
    ret = -1
    paths = set()
    while True:
        ret += 1
        pt = Point(500, 0)
        if grid[pt] != 0:
            break
        
        found = None
        while True:
            if draw:
                paths.add(pt)
            if mode == 1:
                if pt.y > max_y:
                    return ret
            else:
                if pt.y == max_y + 1:
                    break
            good = False
            for d in [(0, 1), (-1, 1), (1, 1)]:
                if grid[pt + d] == 0:
                    good = True
                    pt = pt + d
                    break
            if not good:
                break
        grid[pt] = "Done"

        if draw:
            skip += 1
            if skip % 25 == 1:
                temp = set()
                for pt in paths:
                    if grid[pt] == 0:
                        grid[pt] = "Fall"
                        temp.add(pt)
                grid.save_frame()
                for pt in temp:
                    grid[pt] = 0
                paths = set()

    if draw:
        temp = set()
        for pt in paths:
            if grid[pt] == 0:
                grid[pt] = "Fall"
                temp.add(pt)
        grid.save_frame()
        for pt in temp:
            grid[pt] = 0
        grid.save_frame()
        grid.draw_frames({
            0: (0, 0, 0),
            "#": (255, 255, 255),
            "Fall": (246, 190, 0),
            "Done": (172, 159, 60),
        })
    if get_floor:
        return list(range(min(grid.x_range()) - 1, max(grid.x_range()) + 2))
    return ret

def other_draw(describe, values):
    if describe:
        return "Draw this"
    from dummylog import DummyLog
    import animate
    animate.prep()
    floor = calc(DummyLog(), values, 2, get_floor=True)
    calc(DummyLog(), values, 2, floor=floor, draw=True)
    # calc(DummyLog(), values, 2, draw=True, use_start=start)
    animate.create_mp4(DAY_NUM, rate=30, final_secs=5)

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
