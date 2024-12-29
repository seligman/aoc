#!/usr/bin/env python3

# Animation: https://youtu.be/Oqo4ee30pXU

DAY_NUM = 14
DAY_DESC = 'Day 14: Regolith Reservoir'

def calc(log, values, mode, get_floor=False, floor=None, draw=False):
    from grid import Grid, Point
    grid = Grid()

    for row in values:
        last = None
        for xy in row.split(" -> "):
            pt = Point(*map(int, xy.split(",")))
            if last is not None:
                for cur in pt.line_to(last):
                    grid[cur] = "#"
            last = pt
    
    max_y = max(grid.y_range())

    if floor is not None:
        for x in floor:
            grid[(x, max_y + 2)] = "#"

    skip = 0
    ret = -1

    ages = [set() for _ in range(20)]
    drip = [Point(500, 0)]

    while grid[(500, 0)] == 0:
        ret += 1
        down = False

        while len(drip) > 0 and not down:
            pt = drip[-1]
            while True:
                if mode == 1:
                    if pt.y > max_y:
                        return ret
                good = False
                for d in [(0, 1), (-1, 1), (1, 1)]:
                    if grid[pt + d] == 0 and pt.y < max_y + 1:
                        good = True
                        pt = pt + d
                        break
                if not good:
                    if not down:
                        drip.pop(-1)
                    break
                drip.append(pt)
                down = True
        if draw:
            ages[-1].add(pt)
            for other in drip:
                ages[-1].add(other)

        grid[pt] = "#"

        if draw:
            skip += 1
            if skip % 25 == 1:
                temp = set()
                temp = grid.grid.copy()
                for i, age in enumerate(ages):
                    for pt in age:
                        grid[pt] = f"level_{i}"
                grid.save_frame()
                grid.grid = temp
                ages = [ages[0] | ages[1]] + ages[2:] + [set()]

    if draw:
        for _ in range(len(ages)):
            temp = set()
            temp = grid.grid.copy()
            for i, age in enumerate(ages):
                for pt in age:
                    grid[pt] = f"level_{i}"
            grid.save_frame()
            grid.grid = temp
            ages = [ages[0] | ages[1]] + ages[2:] + [set()]
        grid.draw_frames(create_color_map())

    if get_floor:
        return list(range(min(grid.x_range()) - 1, max(grid.x_range()) + 2))

    return ret + 1

def create_color_map():
    colors = [
        [86, 80, 30],
        [246, 190, 0],
    ]
    map = {}
    for i in range(20):
        x = (i / 25) * (len(colors) - 1)
        if x == int(x):
            rgb = tuple(colors[int(x)])
        else:
            a = int(x)
            b = int(x+1)
            c = x - int(x)
            rgb = (
                int((1 - c) * colors[a][0] + c * colors[b][0]),
                int((1 - c) * colors[a][1] + c * colors[b][1]),
                int((1 - c) * colors[a][2] + c * colors[b][2]),
            )
        map[f"level_{i}"] = rgb
    map["#"] = (255, 255, 255)
    map[0] = (0, 0, 0)
    return map

def other_draw(describe, values):
    if describe:
        return "Draw this"
    from dummylog import DummyLog
    import animate
    animate.prep()
    floor = calc(DummyLog(), values, 2, get_floor=True)
    calc(DummyLog(), values, 2, floor=floor, draw=True)
    animate.create_mp4(DAY_NUM, rate=30, final_secs=5)

def test(log):
    values = log.decode_values("""
        498,4 -> 498,6 -> 496,6
        503,4 -> 502,4 -> 502,9 -> 494,9
    """)

    log.test(calc(log, values, 1), 24)
    log.test(calc(log, values, 2), 93)

def run(log, values):
    log(f"Part 1: {calc(log, values, 1)}")
    log(f"Part 2: {calc(log, values, 2)}")

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2022/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
