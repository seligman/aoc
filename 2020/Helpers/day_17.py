#!/usr/bin/env python3

DAY_NUM = 17
DAY_DESC = 'Day 17: Conway Cubes'

def calc(log, values, mode, draw={"mode": "none"}, sample=(0,), max_count=None):
    from grid import Grid
    grid = Grid(default=".")
    y = 0
    for cur in values:
        x = 0
        for cube in cur:
            grid[x, y, 0, 0] = cube
            x += 1
        y += 1

    dirs = Grid.get_dirs(4)
    if mode == 1:
        dirs = [x for x in dirs if x[3] == 0]
        
    actives = 0
    if draw["mode"] == "draw":
        disp = Grid(' ')
        for x in range(len(draw["z"])):
            for y in range(len(draw["w"])):
                for xo in range(len(draw["x"]) + 2):
                    for yo in range(len(draw["y"]) + 2):
                        if xo == 0 or yo == 0 or xo == len(draw["x"]) + 1 or yo == len(draw["y"]) + 1:
                            disp[x * (len(draw["x"]) + 1) + xo, y * (len(draw["y"]) + 1) + yo] = "Gray"
        disp.draw_grid(show_lines=False)

    def draw_disp():
        for x in draw["x"]:
            for y in draw["y"]:
                for z in draw["z"]:
                    for w in draw["w"]:
                        xo = (z - draw["z"][0]) * (len(draw["x"]) + 1) + 1 + (x - draw["x"][0])
                        yo = (w - draw["w"][0]) * (len(draw["y"]) + 1) + 1 + (y - draw["y"][0])
                        if grid[x, y, z, w] == ".":
                            disp[xo, yo] = " "
                        else:
                            disp[xo, yo] = "star"
        disp.draw_grid(show_lines=False)

    if draw["mode"] == "draw":
        draw_disp()

    def show_grid():
        active_count = 0
        for z in grid.axis_range(2):
            for w in grid.axis_range(3):
                if mode == 1:
                    log(f"z={z}")
                else:
                    log(f"z={z}, w={w}")
                for y in sample[2]:
                    log("".join([grid[x, y, z, w] for x in sample[1]]))
                    active_count += len([grid[x, y, z, w] for x in sample[1] if grid[x, y, z, w] == "#"])
                log("")
        print(f"Total of {active_count} cells")

    if sample[0] == 2:
        log("Before any cycles:")
        show_grid()

    for round in range(6 if max_count is None else max_count):
        todo = []
        actives = 0
        for x in grid.axis_range(0, 1):
            for y in grid.axis_range(1, 1):
                for z in grid.axis_range(2, 1):
                    for w in grid.axis_range(3, 1):
                        temp = 0
                        for xo, yo, zo, wo in dirs:
                            if grid[x+xo, y+yo, z+zo, w+wo] == "#":
                                temp += 1
                        if grid[x, y, z, w] == "#":
                            if temp not in {2, 3}:
                                todo.append((x, y, z, w, None))
                            else:
                                actives += 1
                        elif grid[x, y, z, w] == "." and temp == 3:
                            todo.append((x, y, z, w, "#"))
                            actives += 1
        for x, y, z, w, value in todo:
            if value is None:
                del grid[x, y, z, w]
            else:
                grid[x, y, z, w] = value

        if sample[0] == 2:
            log(f"Round {round+1}")
            show_grid()

        if draw["mode"] == "draw":
            log(f"Drawing round {round+1}")
            draw_disp()

    if sample[0] == 1:
        return list(grid.axis_range(0)), list(grid.axis_range(1))

    if draw["mode"] == "calc":
        return {
            "mode": "draw",
            "x": list(grid.axis_range(0)),
            "y": list(grid.axis_range(1)),
            "z": list(grid.axis_range(2)),
            "w": list(grid.axis_range(3)),
        }

    return actives

def other_sample(describe, values):
    if describe:
        return "Produce a sample output"

    from dummylog import DummyLog
    log = DummyLog()
    values = log.decode_values("""
        .#.
        ..#
        ###
    """)
    log("---- Part 1 ----")
    xr, yr = calc(log, values, 1, sample=(1,), max_count=2)
    calc(log, values, 1, sample=(2, xr, yr), max_count=2)

    log("")
    log("---- Part 2 ----")
    xr, yr = calc(log, values, 2, sample=(1,), max_count=2)
    calc(log, values, 2, sample=(2, xr, yr), max_count=2)

def other_draw(describe, values):
    if describe:
        return "Animate this"
    
    from dummylog import DummyLog
    print("Finding ranges...")
    ranges = calc(DummyLog(), values, 2, draw={"mode": "calc"})
    print("Drawing frames...")
    calc(DummyLog(), values, 2, draw=ranges)

    import subprocess
    import os
    cmd = [
        "ffmpeg", "-y",
        "-hide_banner",
        "-f", "image2",
        "-framerate", "1", 
        "-i", "frame_%05d.png", 
        "-c:v", "libx264", 
        "-profile:v", "main", 
        "-pix_fmt", "yuv420p", 
        "-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2",
        "-an", 
        "-movflags", "+faststart",
        os.path.join("animations", "animation_%02d.mp4" % (get_desc()[0],)),
    ]
    print("$ " + " ".join(cmd))
    subprocess.check_call(cmd)

def test(log):
    values = log.decode_values("""
        .#.
        ..#
        ###
    """)

    log.test(calc(log, values, 1), 112)
    log.test(calc(log, values, 2), 848)

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
