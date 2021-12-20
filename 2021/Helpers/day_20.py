#!/usr/bin/env python3

def get_desc():
    return 20, 'Day 20: Trench Map'

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
    animate.create_mp4(get_desc(), rate=5, final_secs=5)

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
