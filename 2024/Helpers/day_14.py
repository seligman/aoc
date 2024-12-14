#!/usr/bin/env python3

DAY_NUM = 14
DAY_DESC = 'Day 14: Restroom Redoubt'

import re

class Robot:
    def __init__(self, row, size):
        m = re.search("p=(?P<x>[0-9-]+),(?P<y>[0-9-]+) v=(?P<vx>[0-9-]+),(?P<vy>[0-9-]+)", row)
        self.x = int(m["x"])
        self.y = int(m["y"])
        self.vx = int(m["vx"])
        self.vy = int(m["vy"])

def calc(log, values, mode, size=(101, 103)):
    from grid import Grid, Point

    robots = [Robot(row, size) for row in values]

    for y in range(size[1]):
        row = ""
        for x in range(size[0]):
            z = 0
            for cur in robots:
                if cur.x == x and cur.y == y:
                    z += 1
            row += "." if z == 0 else str(z)

    if mode == 2:
        i = 0
        while True:
            i += 1
            seen = set()
            for cur in robots:
                cur.x = (cur.x + cur.vx) % size[0]
                cur.y = (cur.y + cur.vy) % size[1]
                seen.add((cur.x, cur.y))
            if len(seen) == len(robots):
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
