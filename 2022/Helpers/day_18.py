#!/usr/bin/env python3

# Animation: https://imgur.com/a/e0rbktk

DAY_NUM = 18
DAY_DESC = 'Day 18: Boiling Boulders'

from collections import deque

def calc(log, values, mode, draw=False):
    from parsers import get_ints
    from grid import Grid

    seen = []
    grid = Grid()

    for cur in values:
        x, y, z = get_ints(cur)
        seen.append((x, y, z))
        grid[(x, y, z)] = "#"

    grid[(-1, -1, -1)] = 0
    grid[(max(x for x,y,z in seen)+1, max(y for x,y,z in seen)+1, max(z for x,y,z in seen)+1)] = 0

    if mode == 1:
        ret = 0
        for pt in seen:
            for pt in Grid.get_dirs(3, pt, False):
                if grid[pt] == 0:
                    ret += 1
        return ret

    if mode == 2:
        todo = [(-1, -1, -1)]
        used = set(todo)
        escapes_cube = set(todo)

        def in_axis(val, axis):
            return grid.axis_min(axis) <= val <= grid.axis_max(axis)

        while len(todo) > 0:
            pt = todo.pop(0)
            for pt in Grid.get_dirs(3, pt, False):
                if pt not in used:
                    used.add(pt)
                    if in_axis(pt[0], 0) and in_axis(pt[1], 1) and in_axis(pt[2], 2) and grid[pt] == 0:
                        escapes_cube.add(pt)
                        todo.append(pt)

        if draw:
            return grid, escapes_cube
        ret = 0
        for pt in seen:
            for pt in Grid.get_dirs(3, pt, False):
                if pt in escapes_cube:
                    ret += 1
        return ret

def other_draw(describe, values):
    if describe:
        return "Draw this"
    from dummylog import DummyLog
    from grid import Grid
    import animate
    animate.prep()
    grid, escapes_cube = calc(DummyLog(), values, 2, draw=True)

    import matplotlib.pyplot as plt
    import numpy as np

    for limit in range(22):
        print(f"Working on frame {limit}")
        cubes = np.zeros((grid.axis_max(0), grid.axis_max(1), grid.axis_max(2)))
        colors = np.zeros(cubes.shape + (3,))
        cubes.astype(int)

        for (x, y, z), val in grid.grid.items():
            if val != 0 and z <= limit:
                color = (1, 0, 0)
                for pt in Grid.get_dirs(3, (x, y, z), False):
                    if pt in escapes_cube:
                        color = (1, 0, 1)
                        break
                    if grid[pt] == 0:
                        color = (.5, .5, .5)
                cubes[x][y][z] = 1
                colors[x][y][z] = color

        my_dpi = 100
        ax = plt.figure(figsize=(800/my_dpi, 800/my_dpi), dpi=my_dpi).add_subplot(projection='3d')
        ax.voxels(cubes, facecolors=colors, edgecolors='k') # facecolors=colors
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        ax.w_xaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
        ax.w_yaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
        ax.w_zaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
        ax.set_facecolor('black') 
        ax.grid(False)
        plt.tight_layout()
        plt.savefig(f"frame_{limit:05d}.png", dpi=my_dpi, format='png', facecolor='black', transparent=False)
        plt.close()

    animate.create_mp4(DAY_NUM, rate=2, final_secs=1)

def test(log):
    values = log.decode_values("""
        2,2,2
        1,2,2
        3,2,2
        2,1,2
        2,3,2
        2,2,1
        2,2,3
        2,2,4
        2,2,6
        1,2,5
        3,2,5
        2,1,5
        2,3,5
    """)

    log.test(calc(log, values, 1), 64)
    log.test(calc(log, values, 2), 58)

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
