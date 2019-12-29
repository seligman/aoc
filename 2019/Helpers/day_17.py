#!/usr/bin/env python

def get_desc():
    return 17, 'Day 17: Set and Forget'


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
            start_x, start_y, cur_dir = x, y, {60: 3, 94: 0, 62: 1, 118: 2}[val]
        if val == 10:
            x = 0
            y += 1
        else:
            grid.set(val, x, y)
            x += 1

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
    steps = [""]
    dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    while True:
        valid = {35}
        if rotates == 0:
            valid = {35, "o"}
        if grid.get(x + dirs[cur_dir][0], y + dirs[cur_dir][1]) in valid:
            x += dirs[cur_dir][0]
            y += dirs[cur_dir][1]
            grid.set("o", x, y)
            rotates = 0
            if steps[-1].startswith("F"):
                steps[-1] += "F"
            else:
                steps.append("F")
        else:
            if steps[-1].startswith("R"):
                steps[-1] += "R"
            else:
                steps.append("R")
            cur_dir = (cur_dir + 1) % 4
            rotates += 1
            if rotates == 4:
                break
        
    # Normalize the path
    temp = []
    for cur in steps[1:]:
        if cur.startswith("F"):
            temp.append(str(len(cur)))
        elif cur == "R":
            temp.append("R")
        elif cur == "RR":
            temp.append("R")
            temp.append("R")
        elif cur == "RRR":
            temp.append("L")
        elif cur == "RRRR":
            pass
        else:
            raise Exception()
    steps = temp

    # Shorten it
    vars = []
    for var in ["A", "B", "C"]:
        best = None
        start = 0
        while steps[start] in {"A", "B", "C"}:
            start += 1
        for x in range(2, len(steps)):
            temp = ",".join(steps[start:start+x])
            if len(temp) > 20 or "A" in temp or "B" in temp or "C" in temp:
                break
            if ",".join(steps).count(temp) > 1 and temp[-1] in "0123456789":
                best = temp
        steps = ",".join(steps)
        steps = steps.replace(best, var)
        vars.append(best)
        steps = steps.split(",")

    steps = ",".join(steps)

    input_steps = steps + "\n"
    for cur in vars:
        input_steps += cur + "\n"

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
