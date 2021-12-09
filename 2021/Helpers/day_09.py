#!/usr/bin/env python3

def get_desc():
    return 9, 'Day 9: Smoke Basin'

def calc(log, values, mode):
    from grid import Grid
    grid = Grid.from_text(values)

    ret = 0
    points = []
    for x in grid.x_range():
        for y in grid.y_range():
            cur = grid[x, y]
            for ox, oy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                ox = x + ox
                oy = y + oy
                if ox >= 0 and ox <= grid.axis_max(0) and oy >= 0 and oy <= grid.axis_max(1):
                    temp = grid[ox, oy]
                    if temp <= cur:
                        cur = None
                        break
            if cur is not None:
                points.append((x, y))
                ret += 1 + int(cur)

    if mode == 2:
        sizes = []
        for sx, sy in points:
            to_check = [(sx, sy)]
            seen = set([(sx, sy)])
            in_basin = set([(sx, sy)])
            while len(to_check) > 0:
                x, y = to_check.pop(0)
                for ox, oy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    ox = x + ox
                    oy = y + oy
                    if ox >= 0 and ox <= grid.axis_max(0) and oy >= 0 and oy <= grid.axis_max(1):
                        if (ox, oy) not in seen:
                            seen.add((ox, oy))
                            if grid[ox, oy] != '9':
                                in_basin.add((ox, oy))
                                to_check.append((ox, oy))
            sizes.append(len(in_basin))
        sizes.sort()
        ret = sizes[-3] * sizes[-2] * sizes[-1]

    return ret

def test(log):
    values = log.decode_values("""
        2199943210
        3987894921
        9856789892
        8767896789
        9899965678
    """)

    log.test(calc(log, values, 1), 15)
    log.test(calc(log, values, 2), 1134)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))
