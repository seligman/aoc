#!/usr/bin/env python3

# Animation: https://youtu.be/5EWSnlYrt_0

DAY_NUM = 14
DAY_DESC = 'Day 14: Parabolic Reflector Dish'

def calc(log, values, mode, draw=False):
    from grid import Grid, Point
    grid = Grid.from_text(values)

    def get_score():
        ret = 0
        for (x, y), val in grid.grid.items():
            if val == "O":
                ret += grid.axis_max(1) - y + 1
        return ret

    shakes = [
        (0, -1, [(x, 0) for x in grid.x_range()], [(0, y) for y in grid.y_range()]),
        (-1, 0, [(0, y) for y in grid.y_range()], [(x, 0) for x in grid.x_range()]),
        (0, 1, [(x, 0) for x in grid.x_range()], [(0, y) for y in grid.y_range()][::-1]),
        (1, 0, [(0, y) for y in grid.y_range()], [(x, 0) for x in grid.x_range()][::-1]),
    ]

    if draw:
        grid.save_frame()
    step = 0
    seen = {}

    while True:
        for ox, oy, range1, range2 in shakes:
            while True:
                run_again = False
                for val1 in range1:
                    for val2 in range2:
                        x, y = val1[0] + val2[0], val1[1] + val2[1]
                        if draw and step < 3:
                            if grid[x, y] == "O" and grid[x + ox, y + oy] == ".":
                                grid[x, y], grid[x + ox, y + oy] = ".", "O"
                        else:
                            if grid[x, y] == "O":
                                total_x, total_y, moved = 0, 0, False
                                while grid[x + total_x + ox, y + total_y + oy] == ".":
                                    total_x, total_y = total_x + ox, total_y + oy
                                    moved = True
                                if moved:
                                    grid[x, y], grid[x + total_x, y + total_y] = ".", "O"
                if draw and step < 3:
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
    calc(DummyLog(), values, 2, draw=True)
    animate.create_mp4(DAY_NUM, rate=15, final_secs=5)

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
            for dn in [[], ["Puzzles"], ["..", "Puzzles"]]:
                cur = os.path.join(*(dn + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
