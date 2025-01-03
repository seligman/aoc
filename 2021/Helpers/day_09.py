#!/usr/bin/env python3

from collections import deque

DAY_NUM = 9
DAY_DESC = 'Day 9: Smoke Basin'

def calc(log, values, mode, draw=False):
    from grid import Grid
    grid = Grid.from_text(values)
    grid_draw = Grid.from_text(values)

    ret = 0
    points = []
    colors = {
        '0': (12, 7, 134),
        '1': (69, 3, 158),
        '2': (114, 0, 168),
        '3': (155, 23, 158),
        '4': (188, 54, 133),
        '5': (215, 86, 108),
        '6': (236, 120, 83),
        '7': (250, 157, 58),
        '8': (252, 199, 38),
        '9': (239, 248, 33),
        'working': (255, 192, 192),
        'done': (64, 64, 64),
    }
    for x in grid.x_range():
        for y in grid.y_range():
            cur = grid[x, y]
            for ox, oy in grid.neighbors(x, y, valid_only=True):
                temp = grid[ox, oy]
                if temp <= cur:
                    cur = None
                    break
            if cur is not None:
                points.append((x, y))
                ret += 1 + int(cur)

    if draw:
        grid_draw.save_frame()

    if mode == 2:
        sizes = []
        sizes_full = []
        if draw:
            import random
            random.seed(42)
            random.shuffle(points)
        for sx, sy in points:
            to_check = deque([(sx, sy)])
            seen = set([(sx, sy)])
            in_basin = set([(sx, sy)])
            to_undo = []
            sizes_full.append([(sx, sy)])
            if draw:
                grid_draw[sx, sy] = 'working'
                to_undo.append((sx, sy))
                grid_draw.save_frame()
            while len(to_check) > 0:
                x, y = to_check.pop()
                for ox, oy in grid.neighbors(x, y, valid_only=True):
                    if (ox, oy) not in seen:
                        seen.add((ox, oy))
                        if grid[ox, oy] != '9':
                            in_basin.add((ox, oy))
                            to_check.append((ox, oy))
                            if draw:
                                grid_draw[ox, oy] = 'working'
                                to_undo.append((ox, oy))
                                sizes_full[-1].append((ox, oy))
                                if len(to_undo) % 20 == 0:
                                    grid_draw.save_frame()
            if draw:
                grid_draw.save_frame()
                for cur in to_undo:
                    grid_draw[cur] = 'done'
                grid_draw.save_frame()
            sizes.append(len(in_basin))
        sizes.sort()
        ret = sizes[-3] * sizes[-2] * sizes[-1]

    if draw:
        sizes_full.sort(key=lambda x: len(x), reverse=True)
        sizes_full = sizes_full[:3]
        for basin in sizes_full:
            for i, temp in enumerate(basin):
                grid_draw[temp] = 'working'
                if i % 5 == 0:
                    grid_draw.save_frame()
            grid_draw.save_frame()
        
        for _ in range(30):
            grid_draw.save_frame()

        grid_draw.draw_frames(color_map=colors)

    return ret

def other_draw(describe, values):
    if describe:
        return "Animate this"
    from dummylog import DummyLog
    import animate

    animate.prep()
    calc(DummyLog(), values, 2, draw=True)
    animate.create_mp4(DAY_NUM, rate=30)
    
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
    log(f"Part 1: {calc(log, values, 1)}")
    log(f"Part 2: {calc(log, values, 2)}")

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2021/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
