#!/usr/bin/env python3

def get_desc():
    return 17, 'Day 17: Conway Cubes'

def calc(log, values, mode, draw=False):
    from grid import Grid
    grid = Grid(default=".")
    y = 0
    for cur in values:
        x = 0
        for cube in cur:
            grid[x, y, 0, 0] = cube
            x += 1
        y += 1

    dirs = []
    if mode == 1:
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                for z in [-1, 0, 1]:
                    if not (x == 0 and y == 0 and z == 0):
                        dirs.append((x, y, z, 0))
    else:
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                for z in [-1, 0, 1]:
                    for a in [-1, 0, 1]:
                        if not (x == 0 and y == 0 and z == 0 and a == 0):
                            dirs.append((x, y, z, a))
        
    actives = 0

    if draw:
        disp = Grid(' ')
        for x in range(13):
            for y in range(13):
                for xo in range(19):
                    for yo in range(18):
                        if xo == 0 or yo == 0 or xo == 18 or yo == 17:
                            disp[x * 18 + xo, y * 17+ yo] = "Gray"
        disp.draw_grid(show_lines=False)

    def draw_disp():
        if draw:
            for x in range(-4, 13):
                for y in range(-4, 12):
                    for z in range(-6, 7):
                        for a in range(-6, 7):
                            xo = (z + 6) * 18 + 1 + (x + 4)
                            yo = (a + 6) * 17 + 1 + (y + 4)
                            if grid[x, y, z, a] == ".":
                                disp[xo, yo] = " "
                            else:
                                disp[xo, yo] = "star"
            disp.draw_grid(show_lines=False)

    draw_disp()

    for _ in range(6):
        todo = []
        actives = 0
        for x in [-4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] if draw else grid.axis_range(0, 1):
            for y in [-4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] if draw else grid.axis_range(1, 1):
                for z in [-6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6] if draw else grid.axis_range(2, 1):
                    for a in [-6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6] if draw else grid.axis_range(3, 1):
                        temp = 0
                        for xo, yo, zo, ao in dirs:
                            if grid[x+xo, y+yo, z+zo, a+ao] == "#":
                                temp += 1
                        if grid[x, y, z, a] == "#":
                            if temp not in {2, 3}:
                                todo.append((x, y, z, a, "."))
                            else:
                                actives += 1
                        elif grid[x, y, z, a] == "." and temp == 3:
                            todo.append((x, y, z, a, "#"))
                            actives += 1
        for x, y, z, a, value in todo:
            grid[x, y, z, a] = value
        draw_disp()

    # print("x", list(grid.axis_range(0)))
    # print("y", list(grid.axis_range(1)))
    # print("z", list(grid.axis_range(2)))
    # print("a", list(grid.axis_range(3)))

    return actives

def other_draw(describe, values):
    if describe:
        return "Animate this"
    
    from dummylog import DummyLog
    calc(DummyLog(), values, 2, draw=True)

    import subprocess
    cmd = [
        "ffmpeg", 
        "-hide_banner",
        "-f", "image2",
        "-framerate", "1", 
        "-i", "frame_%05d.png", 
        "animation_17.mp4",
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
    log(calc(log, values, 1))
    log(calc(log, values, 2))
