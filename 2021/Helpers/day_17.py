#!/usr/bin/env python3

import re

DAY_NUM = 17
DAY_DESC = 'Day 17: Trick Shot'

def calc(log, values, mode, results=None):
    m = re.search(r"target area: x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)", values[0])
    x1, x2, y1, y2 = int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))

    if results is not None:
        results["target"] = (x1, x2, y1, y2)
        results["trails"] = []

    possible = 0
    overall_best = 0

    # Can't go further than the target in one step
    for start_x in range(min(0, x1, x2), max(0, x1, x2)+1):
        # Can't go higher or lower than the target in one step
        for start_y in range(min(0, y1, y2), max(abs(y1), abs(y2))+1):
            x, y = start_x, start_y
            ox, oy = 0, 0
            best = 0
            if results is not None:
                trail = [(ox, oy)]

            # Find the bounds, to speed up checking later
            min_y12 = min(y1, y2)
            min_x12 = min(x1, x2)
            max_x12 = max(x1, x2)

            # Just keep trying till we escape the possibility of 
            # capture in the target range
            while True:
                ox += x
                oy += y
                y -= 1
                x -= x and (1, -1)[x < 0]
                best = max(best, oy)
                if results is not None:
                    trail.append((ox, oy))
                if x1 <= ox <= x2 and y1 <= oy <= y2:
                    if results is not None:
                        results["trails"].append(trail)
                    possible += 1
                    overall_best = max(best, overall_best)
                    break
                if oy < min_y12 and y <= 0:
                    # We're below the target and going down
                    break
                if x == 0 and (ox < x1 or ox > x2):
                    # Outside of the target and stopped moving left or right
                    break
                if (ox > max_x12 and x >= 0) or (ox < min_x12 and x <= 0):
                    # Beyond the target and still moving past, or stopped
                    break

    return overall_best, possible

def other_draw(describe, values):
    if describe:
        return "Animate this"
    from dummylog import DummyLog
    import animate
    animate.prep()
    results = {}
    calc(DummyLog(), values, 1, results=results)
    from grid import Grid
    grid = Grid()
    for trail in results["trails"][:-1]:
        for x, y in trail:
            if abs(y) < 200:
                grid[x, -y] = "."
    for x in range(results["target"][0], results["target"][1] + 1):
        for y in range(results["target"][2], results["target"][3] + 1):
            grid[x, -y] = "Star"
    temp = []
    for trail in results["trails"]:
        for x, y in trail[:-1]:
            if abs(y) < 200:
                grid[x, -y] = "#"
        temp.append(trail)
        if len(temp) == 10:
            grid.save_frame(extra=[grid.axis_min(0), grid.axis_min(1), temp])
            temp = []
    if len(temp) > 0:
        grid.save_frame(extra=[grid.axis_min(0), grid.axis_min(1), temp])
    grid.draw_frames(cell_size=(4, 4), show_lines=False, extra_callback=draw_trail, use_multiproc=False)
    animate.create_mp4(DAY_NUM, rate=15, final_secs=5)

def draw_trail(d, extra):
    xmin, ymin, trails = extra
    for trail in trails:
        line = []
        for x, y in trail:
            line.append((((x - xmin) * 5) + 2 + 5, ((-y - ymin) * 5) + 2 + 5))
        d.line(line, (255, 255, 255))

def test(log):
    values = log.decode_values("""
        target area: x=20..30, y=-10..-5
    """)

    overall_best, possible = calc(log, values, 1)
    log.test(overall_best, 45)
    log.test(possible, 112)

def run(log, values):
    overall_best, possible = calc(log, values, 1)
    log(overall_best)
    log(possible)

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
