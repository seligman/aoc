#!/usr/bin/env python3

# Animation: https://youtu.be/5EWSnlYrt_0
# Smoothed version: https://youtu.be/qvfBEnJZfsU

DAY_NUM = 14
DAY_DESC = 'Day 14: Parabolic Reflector Dish'

import math

def calc(log, values, mode, draw=False, smoothed=False, steps_to_animate=1):
    from grid import Grid, Point
    grid = Grid.from_text(values)

    def get_score():
        ret = 0
        for (x, y), val in grid.grid.items():
            if val == "O":
                ret += grid.axis_max(1) - y + 1
        return ret

    shakes = [
        (0, -1, [(x, 0) for x in grid.x_range()], [(0, y) for y in grid.y_range()], "north"),
        (-1, 0, [(0, y) for y in grid.y_range()], [(x, 0) for x in grid.x_range()], "west"),
        (0, 1, [(x, 0) for x in grid.x_range()], [(0, y) for y in grid.y_range()][::-1], "south"),
        (1, 0, [(0, y) for y in grid.y_range()], [(x, 0) for x in grid.x_range()][::-1], "east"),
    ]

    if draw:
        circle = {}
        for ox in range(10):
            for oy in range(10):
                dist = math.sqrt((4.5 - ox) ** 2 + (4.5 - oy) ** 2)
                circle[(ox, oy)] = dist
        if smoothed:
            shadow = Grid()
            for x in grid.x_range():
                for y in grid.y_range():
                    if grid[x, y] == "#":
                        for (ox, oy), dist in circle.items():
                            if ox < 5 and grid[x-1, y] == "#": dist = 0
                            if ox >= 5 and grid[x+1, y] == "#": dist = 0
                            if oy < 5 and grid[x, y-1] == "#": dist = 0
                            if oy >= 5 and grid[x, y+1] == "#": dist = 0
                            shadow[x * 10 + ox, y * 10 + oy] = "#" if dist <= 5 else "."
                    else:
                        for (ox, oy), dist in circle.items():
                            shadow[x * 10 + ox, y * 10 + oy] = "."
        else:
            grid.save_frame()
    step = 0
    seen = {}
    last_set = set()

    if draw and smoothed:
        shadow.draw_frames_quickly(color_map={
            '.': (0, 0, 0),
            '#': (255, 255, 255),
            'O': (192, 192, 255),
        }, scale=0.1)

    while True:
        for ox, oy, range1, range2, direction in shakes:
            while True:
                run_again = False
                if draw:
                    stones = []
                for val1 in range1:
                    for val2 in range2:
                        x, y = val1[0] + val2[0], val1[1] + val2[1]
                        if draw and step < steps_to_animate:
                            if grid[x, y] == "O":
                                if grid[x + ox, y + oy] == ".":
                                    run_again = True
                                    grid[x, y], grid[x + ox, y + oy] = ".", "O"
                                    stones.append((x*10, y*10, (x + ox) * 10, (y + oy) * 10))
                                else:
                                    stones.append((x*10, y*10, x*10, y*10))
                        else:
                            if grid[x, y] == "O":
                                total_x, total_y, moved = 0, 0, False
                                while grid[x + total_x + ox, y + total_y + oy] == ".":
                                    total_x, total_y = total_x + ox, total_y + oy
                                    moved = True
                                if moved:
                                    grid[x, y], grid[x + total_x, y + total_y] = ".", "O"
                if draw and step < steps_to_animate and run_again:
                    print(f"Handling drawing, step {step}/{direction}, {shadow.quick_frame if smoothed else grid.frames} frames")
                    if smoothed:
                        for i in range(2, 11, 2):
                            to_set = set()
                            for x1, y1, x2, y2 in stones:
                                x = int(x1 * ((10 - i) / 10) + x2 * (i / 10))
                                y = int(y1 * ((10 - i) / 10) + y2 * (i / 10))
                                for (circle_x, circle_y), dist in circle.items():
                                    if dist <= 5:
                                        to_set.add((x+circle_x, y+circle_y))
                            for pt in last_set - to_set:
                                shadow[pt] = "."
                            for pt in to_set - last_set:
                                shadow[pt] = "O"
                            shadow.save_frame(final_frame=(i == 10 and step == steps_to_animate - 1))
                            last_set = to_set
                    else:
                        grid.save_frame()
                if not run_again:
                    break
            if mode == 1:
                return get_score()
        val = grid.dump_grid()
        score = get_score()
        if val in seen:
            for other_step, score in seen.values():
                if other_step == ((1000000000 - step) % (seen[val][0] - step)) + step - 1:
                    if draw:
                        if smoothed:
                            shadow.finish_quick_draw()
                        else:
                            grid.draw_frames(color_map={
                                '.': (0, 0, 0),
                                '#': (255, 255, 255),
                                'O': (192, 192, 255),
                            })
                    return score
        seen[val] = (step, score)
        step += 1

def other_draw(describe, values):
    if describe:
        return "Draw this"
    from dummylog import DummyLog
    import animate
    animate.prep()
    calc(DummyLog(), values, 2, draw=True, steps_to_animate=3)
    animate.create_mp4(DAY_NUM, rate=15, final_secs=5)

def other_draw_smooth(describe, values):
    if describe:
        return "Draw this, smoothed animation"
    from dummylog import DummyLog
    import animate
    from grid import Grid
    animate.prep()
    calc(DummyLog(), values, 2, draw=True, smoothed=True, steps_to_animate=5)
    animate.create_mp4(DAY_NUM, rate=60, final_secs=5, extra="_smoothed")

def test(log):
    values = log.decode_values("""
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
    """)

    log.test(calc(log, values, 1), '136')
    log.test(calc(log, values, 2), '64')

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))

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
