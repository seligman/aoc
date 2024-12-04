#!/usr/bin/env python3

DAY_NUM = 20
DAY_DESC = 'Day 20: Trench Map'

def calc(log, values, mode, draw=False):
    values = values[:]
    codes = values.pop(0).replace("#", "1").replace(".", "0")
    values.pop(0)

    from grid import Grid
    grid = Grid.from_text([x.replace("#", "1").replace(".", "0") for x in values])
    grid.default = "0"

    if draw:
        save = Grid()
        save.grid = grid.grid.copy()
        save.save_frame()

    for _ in range(2 if mode == 1 else 50):
        next_grid = Grid()
        # Tricky tricky tricky .. deal with zero position from the algo being "1"
        next_grid.default = codes[int(grid.default * 9, 2)]
        for x in grid.x_range(pad = 2):
            for y in grid.y_range(pad = 2):
                z = ""
                for i in range(9):
                    z += grid[i % 3 - 1 + x, i // 3 - 1 + y]
                next_grid[x, y] = codes[int(z, 2)]
        grid = next_grid
        if draw:
            save.grid = grid.grid.copy()
            save.save_frame()

    if draw:
        save.draw_frames(color_map={"0": (0, 0, 0), "1": (255, 255, 255)}, cell_size=(2, 2), show_lines=False)

    return len("".join(x for x in grid.grid.values() if x == "1"))

def other_draw(describe, values):
    if describe:
        return "Draw this"
    from dummylog import DummyLog
    import animate
    animate.prep()
    calc(DummyLog(), values, 2, draw=True)
    animate.create_mp4(DAY_NUM, rate=5, final_secs=5)

def test(log):
    values = log.decode_values("""
        ..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

        #..#.
        #....
        ##..#
        ..#..
        ..###
    """)

    log.test(calc(log, values, 1), 35)
    log.test(calc(log, values, 2), 3351)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))

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
