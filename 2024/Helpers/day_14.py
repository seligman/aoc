#!/usr/bin/env python3

DAY_NUM = 14
DAY_DESC = 'Day 14: Restroom Redoubt'

import re

class Robot:
    def __init__(self, robot_id, row, size):
        m = re.search("p=(?P<x>[0-9-]+),(?P<y>[0-9-]+) v=(?P<vx>[0-9-]+),(?P<vy>[0-9-]+)", row)
        self.robot_id = robot_id
        self.x = int(m["x"])
        self.y = int(m["y"])
        self.vx = int(m["vx"])
        self.vy = int(m["vy"])

def other_draw(describe, values):
    if describe:
        return "Draw this"
    from dummylog import DummyLog
    import animate
    animate.prep()
    calc(DummyLog(), values, 2, draw=True)
    animate.create_mp4(DAY_NUM, rate=15, final_secs=5)

def calc(log, values, mode, size=(101, 103), draw=False, return_robots=False):
    from grid import Grid, Point

    if draw:
        start_animation, final_pos = calc(log, values, mode, size=size, return_robots=True)
        start_animation -= 3

    robots = [Robot(i, row, size) for i, row in enumerate(values)]

    if draw:
        colors = {}
        for x in range(size[0]):
            for y in range(size[1]):
                for cur in final_pos:
                    if cur.x == x and cur.y == y:
                        if (((x % 2) + (y % 2)) % 2) == 0:
                            colors[cur.robot_id] = (128, 255, 128)
                        else:
                            colors[cur.robot_id] = (255, 128, 128)

    for y in range(size[1]):
        row = ""
        for x in range(size[0]):
            z = 0
            for cur in robots:
                if cur.x == x and cur.y == y:
                    z += 1
            row += "." if z == 0 else str(z)

    if mode == 2:
        if draw:
            chunks = []
            grid = Grid(default=".")
            for cur in robots:
                grid[cur.x, cur.y] = "#"
            grid.ensure_ratio(16/9)
            grid.pad(2)
            grid.save_frame()

        i = 0
        chunks = []
        while True:
            i += 1
            seen = set()
            if draw and i > start_animation:
                log(f"Frame {i}")
                for cur in robots:
                    cur.at = Point(cur.x, cur.y)
                    cur.to = Point(cur.x + cur.vx, cur.y + cur.vy)
                    cur.line = list(cur.at.line_to(cur.to, True))
                rate = 50
                for perc in range(rate + 1):
                    perc = perc / rate
                    chunks.append([])
                    for cur in robots:
                        chunks[-1].append([])
                        while len(cur.line) > 0 and cur.line[0][1] <= perc:
                            chunks[-1][-1].append((cur.line[0][0].x % size[0], cur.line[0][0].y % size[1]))
                            cur.line.pop(0)
                        if len(chunks[-1][-1]) == 0:
                            if len(chunks[-1]) == 1:
                                chunks[-1][-1].append(cur.at)
                            else:
                                chunks[-1][-1].append(chunks[-1][-2][-1])
                    for xy in grid.xy_range():
                        grid[xy] = "."
                    while len(chunks) > 20:
                        chunks.pop(0)
                    for perc, chunk in enumerate(chunks):
                        perc = 1 if len(chunks) == 1 else perc / (len(chunks) - 1)
                        c = (" ", (int(perc * 128), int(perc * 128), int(perc * 128)))
                        for line in chunk:
                            for cur in line:
                                grid[cur] = c
                    for robot_id, line in enumerate(chunks[-1]):
                        grid[line[-1]] = (" ", colors[robot_id])
                    grid.save_frame()

            for cur in robots:
                cur.x = (cur.x + cur.vx) % size[0]
                cur.y = (cur.y + cur.vy) % size[1]
                seen.add((cur.x, cur.y))
            
            if len(seen) == len(robots):
                if draw:
                    final = set()
                    for robot_id, line in enumerate(chunks[-1]):
                        final.add((robot_id, line[-1]))
                    target = len(chunks)
                    while len(chunks) > 0:
                        chunks.pop(0)
                        for xy in grid.xy_range():
                            grid[xy] = "."
                        for perc, chunk in enumerate(chunks):
                            perc = 1 if target else perc / (target - 1)
                            c = (" ", (int(perc * 128), int(perc * 128), int(perc * 128)))
                            for line in chunk:
                                for cur in line:
                                    grid[cur] = c
                        for robot_id, cur in final:
                            grid[cur] = (" ", colors[robot_id])
                        grid.save_frame()

                    grid.draw_frames(show_lines=False)
                if return_robots:
                    return i, robots
                else:
                    return i


    for _ in range(100):
        for cur in robots:
            cur.x = (cur.x + cur.vx) % size[0]
            cur.y = (cur.y + cur.vy) % size[1]

    ret = 1
    for x in [0, size[0] // 2 + 1]:
        for y in [0, size[1] // 2 + 1]:
            count = 0
            for cur in robots:
                if cur.x >= x and cur.x < x + size[0] // 2 and cur.y >= y and cur.y < y + size[1] // 2:
                    count += 1
            ret *= count

    return ret

def test(log):
    values = log.decode_values("""
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
    """)

    log.test(calc(log, values, 1, size=(11, 7)), '12')
    # log.test(calc(log, values, 2), 'TODO')

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2024/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
