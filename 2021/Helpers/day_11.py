#!/usr/bin/env python3

from collections import deque

DAY_NUM = 11
DAY_DESC = 'Day 11: Dumbo Octopus'

def calc(log, values, mode, draw=False):
    from grid import Grid
    grid = Grid.from_text(values)
    total = len(grid.grid.keys())
    for key in grid.grid.keys():
        grid[key] = int(grid[key])

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
        '10': (255, 255, 255),
    }

    ret = 0
    step = 0
    while True:
        step += 1
        to_flash = deque(grid.grid)
        flashed = set()
        while len(to_flash):
            xy = to_flash.pop()
            grid[xy] += 1
            if grid[xy] > 9 and xy not in flashed:
                flashed.add(xy)
                to_flash.extend(x for x in grid.neighbors(xy, diagonals=True, valid_only=True))
        
        if mode == 2:
            if len(flashed) == total:
                return step

        ret += len(flashed)

        if draw:
            for xy, value in grid.grid.items():
                grid[xy] = str(min(10, value))
            grid.save_frame(extra_text=[f"Step {step}", f"Flashed: {ret}"])
            for xy, value in grid.grid.items():
                grid[xy] = int(value)

        for xy in flashed:
            grid[xy] = 0

        if draw:
            for xy, value in grid.grid.items():
                grid[xy] = str(min(10, value))
            grid.save_frame(extra_text=[f"Step {step}", f"Flashed: {ret}"])
            for xy, value in grid.grid.items():
                grid[xy] = int(value)

        if mode == 1:
            if step == 100:
                break

    if draw:
        grid.draw_frames(color_map=colors, cell_size=(15, 15))

    return ret

def other_draw(describe, values):
    if describe:
        return "Animate this"
    from dummylog import DummyLog
    import animate

    animate.prep()
    calc(DummyLog(), values, 1, draw=True)
    animate.create_mp4(DAY_NUM, rate=10)

def test(log):
    values = log.decode_values("""
        5483143223
        2745854711
        5264556173
        6141336146
        6357385478
        4167524645
        2176841721
        6882881134
        4846848554
        5283751526
    """)

    log.test(calc(log, values, 1), 1656)
    log.test(calc(log, values, 2), 195)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))

if __name__ == "__main__":
    import sys, os
    cur = None
    for cur in sys.argv[1:] + ["input.txt", "day_##_input.txt", "Puzzles/day_##_input.txt", "../Puzzles/day_##_input.txt"]:
        cur = os.path.join(*cur.split("/")).replace("##", f"{DAY_NUM:02d}")
        if os.path.isfile(cur): fn = cur; break
    if cur is None: print("Unable to find input file!"); exit(1)
    with open(fn) as f: values = f.readlines()
    print(f"Running day {DAY_DESC}:")
    run(print, values)
