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

    if mode == 2:
        minx, miny, maxx, maxy = targets[0][0], targets[0][1], targets[0][0], targets[0][1]
        for x, y, dist in targets:
            minx = min(minx, x)
            miny = min(miny, y)
            maxx = max(maxx, x)
            maxy = max(maxy, y)

        for offset, marker in [(1, "x")]:
            for x, y, dist in targets:
                others = targets[:]
                others.sort(key=lambda other: abs(x - other[0]) + abs(y - other[1]))
                ox, oy = x - (dist + offset), y
                for dx, dy in [(1, -1), (1, 1), (-1, 1), (-1, -1)]:
                    while True:
                        if minx <= ox <= maxx and miny <= oy <= maxy:
                            good = True
                            if marker == "x":
                                for tx, ty, tdist in others:
                                    if abs(ox - tx) + abs(oy - ty) <= tdist:
                                        good = False
                                        break
                            if good:
                                return ox * 4000000 + oy
                                grid[(ox, oy)] = marker
                        if abs(x - (ox + dx)) + abs(y - (oy + dy)) == dist + offset:
                            ox += dx
                            oy += dy
                        else:
                            break

    for val in values:
        m = r.search(val)
        x, y, sx, sy = list(map(int, m.groups()))
        grid[(x, y)] = "S"
        grid[(sx, sy)] = "B"

    if is_test:
        target = 10
    else:
        target = 2000000

    r = re.compile(r"Sensor at x=([\d-]+), y=([\d-]+): closest beacon is at x=([\d-]+), y=([\d-]+)")
    for val in values:
        m = r.search(val)
        x, y, sx, sy = list(map(int, m.groups()))

        dist = abs(x - sx) + abs(y - sy)
        for ox in range(x-dist, x+dist+1):
            if y-dist <= target < y + dist + 1:
                for oy in [target]:
                    dist2 = abs(x - ox) + abs(y - oy)
                    if dist2 <= dist:
                        if grid[(ox, oy)] == 0:
                            grid[(ox, oy)] = "#"

    ret = 0
    for y in [target]:
        for x in grid.x_range():
            if grid[(x, y)] in {"#", "S"}:
                ret += 1
    return ret

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
