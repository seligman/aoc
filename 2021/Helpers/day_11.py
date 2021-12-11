#!/usr/bin/env python3

from collections import deque

def get_desc():
    return 11, 'Day 11: Dumbo Octopus'

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
        to_flash = deque()
        flashed = set()
        for xy, value in grid.grid.items():
            value += 1
            grid[xy] = value
            if value > 9:
                to_flash.append(xy)
                flashed.add(xy)

        while len(to_flash) > 0:
            x, y = to_flash.pop()
            for ox, oy in grid.neighbors(x, y, diagonals=True, valid_only=True):
                grid[ox, oy] += 1
                if grid[ox, oy] > 9:
                    if (ox, oy) not in flashed:
                        to_flash.append((ox, oy))
                        flashed.add((ox, oy))
        
        if mode == 2:
            if len(flashed) == total:
                return step

        ret += len(flashed)

        if draw:
            for key, value in grid.grid.items():
                grid[key] = str(min(10, value))
            grid.save_frame(extra_text=[f"Step {step}", f"Flashed: {ret}"])
            for key, value in grid.grid.items():
                grid[key] = int(value)

        for x, y in flashed:
            grid[x, y] = 0

        if draw:
            for key, value in grid.grid.items():
                grid[key] = str(min(10, value))
            grid.save_frame(extra_text=[f"Step {step}", f"Flashed: {ret}"])
            for key, value in grid.grid.items():
                grid[key] = int(value)

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
    animate.create_mp4(get_desc(), rate=10)

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
