#!/usr/bin/env python3

DAY_NUM = 11
DAY_DESC = 'Day 11: Seating System'

def calc(log, values, mode, draw=False):
    from grid import Grid
    grid = Grid.from_text(values)
    next_grid = Grid.from_text(values)

    if draw:
        grid.save_frame()
        frame = 0

    width = grid.width()
    height = grid.height()

    last_seen = ""
    dirs = Grid.get_dirs(2)
    xys = [(x % grid.width(), x // grid.width()) for x in range(grid.width() * grid.height())]

    while True:
        for x, y in xys:
            occupied = 0
            if mode == 1:
                for dx, dy in dirs:
                    if grid[x + dx, y + dy] == "#":
                        occupied += 1
            else:
                for dx, dy in dirs:
                    tx, ty = x + dx, y + dy
                    while tx >= 0 and ty >= 0 and tx < width and ty < height:
                        spot = grid[tx, ty]
                        if spot == "L":
                            break
                        if spot == "#":
                            occupied += 1
                            break
                        tx, ty = tx + dx, ty + dy

            spot = grid[x, y]
            if spot == "L":
                if occupied == 0:
                    next_grid[x, y] = "#"
            elif spot == "#":
                if occupied >= (4 if mode == 1 else 5):
                    next_grid[x, y] = "L"

        grid, next_grid = next_grid, next_grid.copy()
        if draw:
            frame += 1
            if frame % 2 == 0:
                grid.save_frame()
                grid.save_frame()
        dump = grid.dump_grid()
        if dump == last_seen:
            break
        last_seen = dump

    if draw:
        grid.draw_frames(repeat_final=30, color_map={' ': (0, 0, 0), '.': (0, 0, 0), 'L': (255, 255, 255), '#': (128, 128, 192)})
        Grid.make_animation(file_format="mp4", output_name="animation_%02d_%d" % (get_desc()[0], mode))

    return len([x for x in grid.dump_grid() if x == "#"])

def other_draw_1(describe, values):
    if describe:
        return "Animate this"
    else:
        from dummylog import DummyLog
        calc(DummyLog(), values, 1, draw=True)

def other_draw_2(describe, values):
    if describe:
        return "Animate this"
    else:
        from dummylog import DummyLog
        calc(DummyLog(), values, 2, draw=True)

def test(log):
    values = log.decode_values("""
        L.LL.LL.LL
        LLLLLLL.LL
        L.L.L..L..
        LLLL.LL.LL
        L.LL.LL.LL
        L.LLLLL.LL
        ..L.L.....
        LLLLLLLLLL
        L.LLLLLL.L
        L.LLLLL.LL
    """)

    log.test(calc(log, values, 1), 37)
    log.test(calc(log, values, 2), 26)

def run(log, values):
    log(f"Part 1: {calc(log, values, 1)}")
    log(f"Part 2: {calc(log, values, 2)}")

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2020/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
