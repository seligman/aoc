#!/usr/bin/env python3

# Animation: https://youtu.be/DYrIH225wHs

DAY_NUM = 10
DAY_DESC = 'Day 10: Pipe Maze'

from collections import deque

def calc(log, values, mode, draw=False):
    from grid import Grid, Point
    grid = Grid.from_text(values)

    if draw:
        shadow = Grid.from_text(values)

        for pt, val in shadow.grid.items():
            if val == "S": shadow[pt] = "Star"
            elif val == "|": shadow[pt] = "\u2503"
            elif val == "-": shadow[pt] = "\u2501"
            elif val == "L": shadow[pt] = "\u2517"
            elif val == "F": shadow[pt] = "\u250F"
            elif val == "7": shadow[pt] = "\u2513"
            elif val == "J": shadow[pt] = "\u251B"

    start = None
    for (x, y), val in grid.grid.items():
        if val == "S":
            start = (x, y)

    ret = 0
    if mode == 1:
        to_check = [(start, 0)]
        seen = set()
        while len(to_check) > 0:
            (x, y), dist = to_check.pop(0)
            if (x, y) not in seen:
                seen.add((x, y))
                ret = max(ret, dist)

                if grid[x - 1, y] in {"-", "L", "F"}: to_check.append(((x - 1, y), dist + 1))
                if grid[x + 1, y] in {"-", "J", "7"}: to_check.append(((x + 1, y), dist + 1))
                if grid[x, y - 1] in {"|", "F", "7"}: to_check.append(((x, y - 1), dist + 1))
                if grid[x, y + 1] in {"|", "L", "J"}: to_check.append(((x, y + 1), dist + 1))
    else:
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
    
        if draw:
            shadow.save_frame()
            for i, pt in enumerate(loop):
                shadow[pt] = [shadow[pt], (128, 128, 0)]
                if i % 100 == 0:
                    log(f"Saving pipe {i}...")
                    shadow.save_frame()
            shadow.save_frame()

        for (x, y), val in grid.grid.items():
            if (x, y) not in loop:
                grid[x, y] = "."

        temp = Grid()
        for (x, y), val in grid.grid.items():
            x *= 2
            y *= 2
            temp[x + 1, y] = "."
            temp[x, y + 1] = "."
            temp[x + 1, y + 1] = "."
            temp[x, y] = val
            if val in {"-", "L", "F", "S"} and grid[x // 2 + 1, y // 2] in {"-", "7", "J"}:
                temp[x + 1, y] = "X"
            if val in {"|", "7", "F", "S"} and grid[x // 2, (y // 2) + 1] in {"|", "J", "L"}:
                temp[x, y + 1] = "X"
        
        grid = temp
        max_x = grid.axis_max(0) + 1
        max_y = grid.axis_max(1) + 1
        todo = [(-1, -1)]
        seen = set()
        step = 0
        while len(todo):
            x, y = todo.pop(0)
            if (x, y) not in seen:
                seen.add((x, y))
                if draw:
                    if x % 2 == 0 and y % 2 == 0:
                        if isinstance(shadow[x // 2, y // 2], list):
                            shadow[x // 2, y // 2] = [shadow[x // 2, y // 2][0], (128, 128, 128)]
                        else:
                            shadow[x // 2, y // 2] = ["" if shadow[x // 2, y // 2] in {0, "."} else shadow[x // 2, y // 2], (128, 128, 128)]
                        step += 1
                        if step % 25 == 0:
                            log(f"Saving flood {step}...")
                            shadow.save_frame()
                grid[x, y] = "#"
                for x, y in grid.get_dirs(2, (x, y)):
                    if x >= -1 and y >= -1 and x <= max_x and y <= max_y:
                        if grid[x, y] in {".", 0}:
                            todo.append((x, y))

        step = 0
        for (x, y), val in grid.grid.items():
            if x % 2 == 0 and y % 2 == 0:
                if val == ".":
                    if draw:
                        if isinstance(shadow[x // 2, y // 2], list):
                            shadow[x // 2, y // 2] = [shadow[x // 2, y // 2][0], (255, 255, 0)]
                        else:
                            shadow[x // 2, y // 2] = ["" if shadow[x // 2, y // 2] in {0, "."} else shadow[x // 2, y // 2], (255, 255, 0)]
                        step += 1
                        if step % 5 == 0:
                            log(f"Saving find {step}...")
                            shadow.save_frame()
                    ret += 1

        if draw:
            shadow.save_frame()
            shadow.draw_frames()

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
