#!/usr/bin/env python3

DAY_NUM = 15
DAY_DESC = 'Day 15: Beacon Exclusion Zone'

def get_dist(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def walk_edge(x, y, dist):
    ox, oy = x - (dist + 1), y
    for dx, dy in [(1, -1), (1, 1), (-1, 1), (-1, -1)]:
        for move in range(dist + 2):
            yield ox, oy
            if move < dist + 2:
                ox += dx
                oy += dy

def calc(log, values, mode, is_test=False):
    from grid import Grid
    from parsers import get_ints
    grid = Grid()

    if is_test:
        target = 10
    else:
        target = 2000000

    targets = []
    for val in values:
        x, y, sx, sy = get_ints(val)
        dist = abs(x - sx) + abs(y - sy)
        targets.append((x, y, dist))
        grid[(x, y)] = "S"
        if mode == 1:
            grid[(sx, sy)] = "B"

    if mode == 2:
        minx, maxx = grid.axis_min(0), grid.axis_max(0)
        miny, maxy = grid.axis_min(1), grid.axis_max(1)

        targets.sort(key=lambda other: other[2])
        temp = []
        while len(targets) > 0:
            if len(targets) > 0: temp.append(targets.pop(0))
            if len(targets) > 0: temp.append(targets.pop(-1))
        targets = temp[::-1]

        for x, y, dist in targets:
            others = [other for other in targets if get_dist(x, y, other[0], other[1]) <= (other[2] + dist + 1)]
            others = [other for other in others if (x, y, dist) != other]

            if sum(1 for other in others if get_dist(x, y, other[0], other[1]) == (other[2] + dist)) == 1:
                for ox, oy in walk_edge(x, y, dist):
                    if minx <= ox <= maxx and miny <= oy <= maxy:
                        good = True
                        for tx, ty, tdist in others:
                            if get_dist(ox, oy, tx, ty) <= tdist:
                                good = False
                                break
                        if good:
                            return ox * 4000000 + oy

    grid_line = {}
    for (ox, oy), value in grid.grid.items():
        if oy == target:
            grid_line[ox] = value

    segments = []
    for x, y, dist in targets:
        a = x - (dist - abs(y - target))
        b = x + (dist - abs(y - target))
        if a <= b:
            while True:
                found = False
                for i, (oa, ob) in enumerate(segments):
                    if (oa <= a <= ob) or (oa <= b <= ob) or (a <= oa <= b) or (a <= ob <= b):
                        a, b = min(a, oa), max(b, ob)
                        segments.pop(i)
                        found = True
                        break
                if not found:
                    break
            segments.append([a, b])

    return sum((b - a) + 1 for a, b in segments) - len(grid_line)

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
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
