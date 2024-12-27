#!/usr/bin/env python3

DAY_NUM = 17
DAY_DESC = 'Day 17: Set and Forget'


def calc(log, values, animate=False):
    # Draw the grid out
    from program import Program
    from grid import Grid
    prog = Program.from_values(values, log)
    grid = Grid()
    x, y, start_x, start_y = 0, 0, 0, 0
    prog.tick_till_end()
    grid_size = len(prog.output)
    while len(prog.output) > 0:
        val = prog.get_output()
        if val in {60, 94, 62, 118}:
            start_x, start_y, cur_dir = x, y, {ord("^"): 0, ord(">"): 1, ord("v"): 2, ord("<"): 3}[val]
        if val == ord("\n"):
            x = 0
            y += 1
        else:
            grid.set(val, x, y)
            x += 1

    # grid.show_grid(log, {47: "/", 46: ".", 35: "#", 94: "^"})
    # exit(0)

    ret = 0
    for x in grid.x_range():
        for y in grid.y_range():
            if grid.get(x, y) == 35:
                count = 0
                for xo, yo in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    if grid.get(x + xo, y + yo) == 35:
                        count += 1
                if count == 4:
                    ret += x * y

    log("Intersections sum: " + str(ret))

    # Find a path through
    x, y = start_x, start_y
    rotates = 0
    steps = []
    dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    grid.set("o", x, y)
    while True:
        if grid.get(x + dirs[cur_dir][0], y + dirs[cur_dir][1]) in {ord("#"), "o"}:
            x += dirs[cur_dir][0]
            y += dirs[cur_dir][1]
            grid.set("o", x, y)
            if len(steps) == 0 or isinstance(steps[-1], str):
                steps.append(1)
            else:
                steps[-1] += 1
        else:
            if grid.get(x + dirs[(cur_dir + 1) % 4][0], y + dirs[(cur_dir + 1) % 4][1]) == ord("#"):
                cur_dir = (cur_dir + 1) % 4
                steps.append("R")
            elif grid.get(x + dirs[(cur_dir - 1) % 4][0], y + dirs[(cur_dir - 1) % 4][1]) == ord("#"):
                cur_dir = (cur_dir - 1) % 4
                steps.append("L")
            elif grid.get(x + dirs[(cur_dir + 2) % 4][0], y + dirs[(cur_dir + 2) % 4][1]) == ord("#"):
                cur_dir = (cur_dir + 2) % 4
                steps.append("RR")
            else:
                break

    steps = [str(x) for x in steps]

    # Shorten it
    def find_repeat(path, registers=[], sequence=[]):
        cleared = False
        while not cleared:
            cleared = True

            for i, prev in enumerate(registers):
                if len(prev) <= len(path) and path[:len(prev)] == prev:
                    path = path[len(prev):]
                    sequence.append(i)
                    cleared = False
                    break

        if len(registers) == 3:
            return (True, registers, sequence) if len(path) == 0 else (False, None, None)

        register_len = min(len(path), 20 // 2)

        while len(",".join(path[:register_len])) > 20 or path[register_len - 1] in {'R', 'L'}:
            register_len -= 1

        while register_len > 0:
            res, matches, seq = find_repeat(path, registers + [path[:register_len]], sequence.copy())
            if res:
                return res, matches, seq
            register_len -= 2

        return False, [], []

    valid, funcs, prog = find_repeat(steps)

    input_steps = ",".join(chr(ord('A') + x) for x in prog) + "\n"
    for cur in funcs:
        input_steps += ",".join(cur) + "\n"

    prog = Program.from_values(values, log)
    prog.ticker[0] = 2
    [prog.add_to_input(ord(x)) for x in input_steps + "n\n"]
    prog.tick_till_end()

    # Find the location of the final output
    score_offset = None
    for key in prog.ticker:
        if prog.ticker[key] == prog.last_output:
            score_offset = key
            break

    log("Found location for score at: " + str(score_offset))

    # And finally, draw the solution (or just run it)
    prog = Program.from_values(values, log)
    prog.ticker[0] = 2
    [prog.add_to_input(ord(x)) for x in input_steps + ("y\n" if animate else "n\n")]

    while prog.flag_running:
        prog.tick()
        if len(prog.output) == grid_size:
            if prog.peek_output() not in {ord("#"), ord(".")}:
                while True:
                    val = prog.get_output()
                    if val == 10:
                        break
            else:
                x, y = 0, 0
                while len(prog.output) > 0:
                    val = prog.get_output()
                    if val == 10:
                        y += 1
                        x = 0
                    else:
                        if val in {60, 94, 62, 118}:
                            grid.set(val, x, y)
                        x += 1
                if animate:
                    grid.save_frame(extra_text=["Dust Cleared: |%06d" % (prog.ticker[score_offset],)])

    if animate:
        Grid.clear_frames()
        grid.draw_frames(color_map={
            ord("."): (0, 0, 0),
            ord("#"): (255, 255, 255),
            ord("v"): (128, 128, 192),
            ord("<"): (128, 128, 192),
            ord(">"): (128, 128, 192),
            ord("^"): (128, 128, 192),
            "o": (255, 255, 255),
        }, repeat_final=30)
        Grid.make_animation(output_name="animation_%02d" % (get_desc()[0],), file_format="mp4")

    log("Cleaning readout: " + str(prog.last_output))

    return prog.last_output


def test(log):
    return True


def other_animate(describe, values):
    if describe:
        return "Animate the work"
    from dummylog import DummyLog
    calc(DummyLog(), values, animate=True)
    print("Done, created animation...")


def run(log, values):
    calc(log, values)

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2019/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
