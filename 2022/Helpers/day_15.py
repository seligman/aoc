#!/usr/bin/env python3

DAY_NUM = 15
DAY_DESC = 'Day 15: Beacon Exclusion Zone'

import re

def calc(log, values, mode, is_test=False):
    from grid import Grid, Point
    grid = Grid()

    r = re.compile(r"Sensor at x=([\d-]+), y=([\d-]+): closest beacon is at x=([\d-]+), y=([\d-]+)")
    targets = []
    for val in values:
        m = r.search(val)
        x, y, sx, sy = list(map(int, m.groups()))
        dist = abs(x - sx) + abs(y - sy)
        targets.append((x, y, dist))
        grid[(x, y)] = "S"
        if mode == 1:
            grid[(sx, sy)] = "B"

    if mode == 2:
        minx, maxx = grid.axis_min(0), grid.axis_max(0)
        miny, maxy = grid.axis_min(1), grid.axis_max(1)
        centerx, centery = (minx + maxx) // 2, (miny + maxy) // 2

        targets.sort(key=lambda other: other[2])
        temp = []
        while len(targets) > 0:
            if len(targets) > 0: temp.append(targets.pop(0))
            if len(targets) > 0: temp.append(targets.pop(-1))
        targets = temp[::-1]

        for x, y, dist in targets:
            others = targets[:]
            others.sort(key=lambda other: abs(x - other[0]) + abs(y - other[1]))

            ox, oy = x - (dist + 1), y
            for dx, dy in [(1, -1), (1, 1), (-1, 1), (-1, -1)]:
                for move in range(dist + 2):
                    if minx <= ox <= maxx and miny <= oy <= maxy:
                        good = True
                        for tx, ty, tdist in others:
                            if abs(ox - tx) + abs(oy - ty) <= tdist:
                                good = False
                                break
                        if good:
                            return ox * 4000000 + oy
                    if move < dist + 2:
                        ox += dx
                        oy += dy

    if is_test:
        target = 10
    else:
        target = 2000000

    grid_line = {}
    for (ox, oy), value in grid.grid.items():
        if oy == target:
            grid_line[ox] = value

    for val in values:
        m = r.search(val)
        x, y, sx, sy = list(map(int, m.groups()))

        dist = abs(x - sx) + abs(y - sy)
        for ox in range(x-dist, x+dist+1):
            if y-dist <= target < y + dist + 1:
                dist2 = abs(x - ox) + abs(y - target)
                if dist2 <= dist:
                    if ox not in grid_line:
                        grid_line[ox] = "#"

    return sum(1 for x in grid_line.values() if x == "#")

def test(log):
    values = log.decode_values("""
        Sensor at x=2, y=18: closest beacon is at x=-2, y=15
        Sensor at x=9, y=16: closest beacon is at x=10, y=16
        Sensor at x=13, y=2: closest beacon is at x=15, y=3
        Sensor at x=12, y=14: closest beacon is at x=10, y=16
        Sensor at x=10, y=20: closest beacon is at x=10, y=16
        Sensor at x=14, y=17: closest beacon is at x=10, y=16
        Sensor at x=8, y=7: closest beacon is at x=2, y=10
        Sensor at x=2, y=0: closest beacon is at x=2, y=10
        Sensor at x=0, y=11: closest beacon is at x=2, y=10
        Sensor at x=20, y=14: closest beacon is at x=25, y=17
        Sensor at x=17, y=20: closest beacon is at x=21, y=22
        Sensor at x=16, y=7: closest beacon is at x=15, y=3
        Sensor at x=14, y=3: closest beacon is at x=15, y=3
        Sensor at x=20, y=1: closest beacon is at x=15, y=3
    """)

    log.test(calc(log, values, 1, is_test=True), 26)
    log.test(calc(log, values, 2), 56000011)

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
