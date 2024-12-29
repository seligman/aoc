#!/usr/bin/env python3

# Animation: https://youtu.be/3eFCQ2M4xf0

DAY_NUM = 18
DAY_DESC = 'Day 18: Lavaduct Lagoon'

from collections import defaultdict

def poly_area(poly):
    area = 0.0
    for i in range(len(poly)):
        j = (i + 1) % len(poly)
        area += poly[i][0] * poly[j][1]
        area -= poly[j][0] * poly[i][1]
    area = abs(area) / 2.0
    return area

def calc(log, values, mode, draw=False):
    lines = [(0, 0)]
    x, y = 0, 0
    line_len = 0
    if draw:
        from grid import Grid
        grid = Grid()
        colors = []

    for row in values:
        row = row.split(' ')
        if mode == 1:
            ox, oy = {
                "R": (1, 0),
                "D": (0, 1),
                "L": (-1, 0),
                "U": (0, -1),
            }[row[0]]
            l = int(row[1])
        else:
            ox, oy = {
                "0": (1, 0),
                "1": (0, 1),
                "2": (-1, 0),
                "3": (0, -1),
            }[row[2][-2]]
            l = int(row[2][2:7], 16)
        if draw:
            r, g, b = int(row[2][2:4], 16), int(row[2][4:6], 16), int(row[2][6:8], 16)
            r, g, b = int((r / 255) * 191 + 64), int((g / 255) * 191 + 64), int((b / 255) * 191 + 64)
            for i in range(l):
                grid[x + ox * i, y + oy * i] = (None, (r, g, b))
                colors.append((x + ox * i, y + oy * i))
        x, y = x + ox * l, y + oy * l
        lines.append((x, y))
        line_len += l
    if draw:
        inside = set()
        for y in grid.y_range():
            is_inside = False
            for x in grid.x_range():
                if grid[x, y] == 0:
                    if is_inside: inside.add((x, y))
                else:
                    if grid[x, y+1] != 0:
                        is_inside = not is_inside

        print(f"Draw step {grid.frame}")
        grid.draw_grid()

        step = 0
        while True:
            print(f"Step at {step}")
            seen_points = set()
            color_to_color = defaultdict(list)
            next_colors = []
            for x, y in colors:
                for ox, oy in grid.get_dirs(2, (x, y), True):
                    if (ox, oy) in inside:
                        if (ox, oy) not in seen_points:
                            next_colors.append((ox, oy))
                            seen_points.add((ox, oy))
                        color_to_color[(ox, oy)].append((x, y))
            if len(next_colors) == 0:
                break
            for x, y in next_colors:
                inside.remove((x, y))
            for x, y in next_colors:
                merge = color_to_color[(x, y)]
                r, g, b, count = 0, 0, 0, 0
                for pt in merge:
                    count += 1
                    rgb = grid[pt][1]
                    r, g, b = r + rgb[0], g + rgb[1], b + rgb[2]
                r = r // count
                g = g // count
                b = b // count
                grid[x, y] = (None, (r, g, b))
                step += 1
                if step % 100 == 0:
                    print(f"Draw step {grid.frame}")
                    grid.draw_grid()
            colors = next_colors
        print(f"Draw step {grid.frame}")
        grid.draw_grid()

    return int(poly_area(lines) + line_len // 2 + 1)

def other_draw(describe, values):
    if describe:
        return "Draw this"
    from dummylog import DummyLog
    import animate
    animate.prep()
    calc(DummyLog(), values, 1, draw=True)
    animate.create_mp4(DAY_NUM, rate=30, final_secs=5)

def test(log):
    values = log.decode_values("""
        R 6 (#70c710)
        D 5 (#0dc571)
        L 2 (#5713f0)
        D 2 (#d2c081)
        R 2 (#59c680)
        D 2 (#411b91)
        L 5 (#8ceee2)
        U 2 (#caa173)
        L 1 (#1b58a2)
        U 2 (#caa171)
        R 2 (#7807d2)
        U 3 (#a77fa3)
        L 2 (#015232)
        U 2 (#7a21e3)
    """)

    log.test(calc(log, values, 1), '62')
    log.test(calc(log, values, 2), '952408144115')

def run(log, values):
    log(f"Part 1: {calc(log, values, 1)}")
    log(f"Part 2: {calc(log, values, 2)}")

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2023/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
