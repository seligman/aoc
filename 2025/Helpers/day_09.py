#!/usr/bin/env python3

DAY_NUM = 9
DAY_DESC = 'Day 9: Movie Theater'

def is_pt_on_seg(px, py, x1, y1, x2, y2):
    cross = (x2 - x1) * (py - y1) - (y2 - y1) * (px - x1)
    if abs(cross) > 0:
        return False
    if px < min(x1, x2) or px > max(x1, x2):
        return False
    if py < min(y1, y2) or py > max(y1, y2):
        return False
    return True

def is_pt_in_poly(px, py, poly):
    inside = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i].tuple
        x2, y2 = poly[(i + 1) % n].tuple
        if is_pt_on_seg(px, py, x1, y1, x2, y2):
            return True
        if ((y1 > py) != (y2 > py)):
            x_intersect = (x2 - x1) * (py - y1) / (y2 - y1) + x1
            if px < x_intersect:
                inside = not inside
    return inside

def get_orient(ax, ay, bx, by, cx, cy):
    v = (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)
    if v > 0:
        return 1
    if v < 0:
        return -1
    return 0

def get_seg_inter(a1, a2, b1, b2):
    x1, y1 = a1
    x2, y2 = a2
    x3, y3 = b1
    x4, y4 = b2
    o1 = get_orient(x1, y1, x2, y2, x3, y3)
    o2 = get_orient(x1, y1, x2, y2, x4, y4)
    o3 = get_orient(x3, y3, x4, y4, x1, y1)
    o4 = get_orient(x3, y3, x4, y4, x2, y2)
    return o1 * o2 < 0 and o3 * o4 < 0

def rect_in_poly(x1, x2, y1, y2, points):
    for cx, cy in [(x1, y1),(x1, y2),(x2, y1),(x2, y2)]:
        if not is_pt_in_poly(cx, cy, points):
            return False
    n = len(points)
    for e1 in [((x1, y1), (x2, y1)), ((x2, y1), (x2, y2)), ((x2, y2), (x1, y2)),((x1, y2), (x1, y1))]:
        for i in range(n):
            e2 = ((points[i].x, points[i].y), (points[(i + 1) % n].x, points[(i + 1) % n].y))
            if get_seg_inter(e1[0], e1[1], e2[0], e2[1]):
                return False
    return True

def calc(log, values, mode):
    from itertools import combinations
    from grid import Grid, Point

    to_check = []
    for row in values:
        x, y = [int(i) for i in row.split(",")]
        # grid[x, y] = "#"
        to_check.append(Point(x, y))
    
    best = 0
    for a, b in combinations(to_check, 2):
        x1, x2 = min(a.x, b.x), max(a.x, b.x)
        y1, y2 = min(a.y, b.y), max(a.y, b.y)

        if mode == 1:
            for other in to_check:
                hit = False
                if x1 <= other.x <= x2 and y1 <= other.y <= y2:
                    hit = True
                    break
                if not hit:
                    area = (x2 - x1 + 1) * (y2 - y1 + 1)
                    if area > best:
                        best = area
        elif mode == 2:
            if rect_in_poly(x1, x2, y1, y2, to_check):
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
