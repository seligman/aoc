#!/usr/bin/env python3

DAY_NUM = 9
DAY_DESC = 'Day 9: Movie Theater'

_intervals = None
_y_by_index = None
_y_offsets = None

def rect_in_poly(x1, y1, x2, y2):
    for y in _y_by_index[_y_offsets[y1]: _y_offsets[y2]+1]:
        covered = False
        for start, end in _intervals[y]:
            if start <= x1 and x2 <= end:
                covered = True
                break

        if not covered:
            return False

    return True

def build_interval_cache(points):
    global _y_by_index, _intervals, _y_offsets

    edges = list(zip(points, points[1:] + points[0:1]))
    _y_by_index = sorted(set(p.y for p in points))
    _y_offsets = {x: i for i, x in enumerate(_y_by_index)}
    _intervals = {}

    for y in _y_by_index:
        crossings = []
        horizontal_edges = []

        for p1, p2 in edges:
            if p1.y == p2.y and p1.y == y:
                horizontal_edges.append((min(p1.x, p2.x), max(p1.x, p2.x)))
            else:
                if min(p1.y, p2.y) < y <= max(p1.y, p2.y):
                    if p1.x == p2.x:
                        crossings.append(p1.x)
                    else:
                        raise Exception()

        crossings.sort()

        filled_intervals = []
        for i in range(0, len(crossings) - 1, 2):
            filled_intervals.append((crossings[i], crossings[i + 1]))

        for h_start, h_end in horizontal_edges:
            filled_intervals.append((h_start, h_end))

        filled_intervals.sort()
        merged = []
        current_start, current_end = filled_intervals[0]

        for start, end in filled_intervals[1:]:
            if start <= current_end + 1:
                current_end = max(current_end, end)
            else:
                merged.append((current_start, current_end))
                current_start, current_end = start, end

        merged.append((current_start, current_end))
        _intervals[y] = merged

def calc(log, values, mode):
    from itertools import combinations
    from grid import Grid, Point

    to_check = []
    for row in values:
        x, y = [int(i) for i in row.split(",")]
        to_check.append(Point(x, y))
    
    if mode == 2:
        build_interval_cache(to_check)

    best = 0
    for a, b in combinations(to_check, 2):
        x1, x2 = min(a.x, b.x), max(a.x, b.x)
        y1, y2 = min(a.y, b.y), max(a.y, b.y)

        if mode == 1:
            area = (x2 - x1 + 1) * (y2 - y1 + 1)
            if area > best:
                best = area
        elif mode == 2:
            if rect_in_poly(x1, y1, x2, y2):
                area = (x2 - x1 + 1) * (y2 - y1 + 1)
                if area > best:
                    best = area

    return best

def test(log):
    values = log.decode_values("""
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
    """)

    log.test(calc(log, values, 1), '50')
    log.test(calc(log, values, 2), '24')

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
