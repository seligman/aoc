#!/usr/bin/env python3

# Animation: https://youtu.be/DYrIH225wHs
# Fix up version: https://youtu.be/-vaIkRA1w9k

DAY_NUM = 10
DAY_DESC = 'Day 10: Pipe Maze'

def calc(log, values, mode, draw=False):
    from grid import Grid, Point
    grid = Grid.from_text(values)

    if draw:
        shadow = Grid.from_text(values)

        for pt, val in shadow.grid.items():
            if val == "S": val = "Star"
            elif val == "|": val = "\u2503"
            elif val == "-": val = "\u2501"
            elif val == "L": val = "\u2517"
            elif val == "F": val = "\u250F"
            elif val == "7": val = "\u2513"
            elif val == "J": val = "\u251B"
            else: val = " "
            shadow[pt] = [val, (0, 0, 0), (0, 0, 128)]

    start = None
    for (x, y), val in grid.grid.items():
        if val == "S":
            start = (x, y)

    # Change the start cell from "S" to it's proper pipe
    if grid[start[0], start[1] - 1] in {"|", "F", "7"} and grid[start[0], start[1] + 1] in {"|", "L", "J"}:
        grid[start] = "|"
    elif grid[start[0] - 1, start[1]] in {"-", "F", "L"} and grid[start[0] + 1, start[1]] in {"-", "7", "J"}:
        grid[start] = "-"
    elif grid[start[0], start[1] - 1] in {"|", "F", "7"} and grid[start[0] - 1, start[1]] in {"-", "F", "L"}:
        grid[start] = "J"
    elif grid[start[0], start[1] - 1] in {"|", "F", "7"} and grid[start[0] + 1, start[1]] in {"-", "7", "J"}:
        grid[start] = "7"
    elif grid[start[0], start[1] + 1] in {"|", "L", "J"} and grid[start[0] - 1, start[1]] in {"-", "F", "L"}:
        grid[start] = "L"
    elif grid[start[0], start[1] + 1] in {"|", "L", "J"} and grid[start[0] + 1, start[1]] in {"-", "7", "J"}:
        grid[start] = "F"
    else:
        raise Exception()
    
    # Find the loop so we can ignore other pipe parts
    loop = {start: None}
    pos = start
    while True:
        if grid[pos] == "-": opts = [(-1, 0), (1, 0)]
        elif grid[pos] == "|": opts = [(0, -1), (0, 1)]
        elif grid[pos] == "L": opts = [(0, -1), (1, 0)]
        elif grid[pos] == "F": opts = [(0, 1), (1, 0)]
        elif grid[pos] == "7": opts = [(0, 1), (-1, 0)]
        elif grid[pos] == "J": opts = [(0, -1), (-1, 0)]
        else:
            raise Exception()
        opts = [(x[0] + pos[0], x[1] + pos[1]) for x in opts]
        if opts[0] not in loop:
            loop[opts[0]] = None
            pos = opts[0]
        elif opts[1] not in loop:
            loop[opts[1]] = None
            pos = opts[1]
        else:
            break

    ret = 0
    if mode == 1:
        ret = len(loop) // 2
    else:
        if draw:
            # Highlight the loop itself
            shadow.save_frame()
            for i, pt in enumerate(loop):
                shadow[pt][2] = (128, 128, 0)
                if i % 94 == 0:
                    log(f"Saving pipe {i}, frame #{len(shadow.frames)}...")
                    shadow.save_frame()
            shadow.save_frame()

        # Scan through and note any inside cells
        step = 0
        for y in grid.y_range():
            inside = False
            for x in grid.x_range():
                val = grid[x, y]
                if (x, y) in loop:
                    if val in {"|", "7", "F"}:
                        inside = not inside
                else:
                    if inside:
                        if draw:
                            shadow[(x, y)][1] = (255, 255, 0)
                        ret += 1
                    else:
                        if draw:
                            shadow[(x, y)][1] = (0, 0, 128)
                if draw:
                    if step % 130 == 0:
                        log(f"Saving find {step}, frame #{len(shadow.frames)}...")
                        shadow.save_frame()
                    step += 1

        if draw:
            shadow.save_frame()
            shadow.draw_frames(show_lines=False)

    return ret

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
.....
.S-7.
.|.|.
.L-J.
.....
    """)

    log.test(calc(log, values, 1), '4')

    values = log.decode_values("""
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
    """)

    log.test(calc(log, values, 2), '8')

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
