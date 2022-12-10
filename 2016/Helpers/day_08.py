#!/usr/bin/env python3

import re

DAY_NUM = 8
DAY_DESC = 'Day 8: Two-Factor Authentication'


def calc(log, values, width, height, show):
    grid = [["."] * width for _ in range(height)]
    for cur in values:
        m = re.search("rect ([0-9]+)x([0-9]+)", cur)
        if m:
            for x in range(int(m.group(1))):
                for y in range(int(m.group(2))):
                    grid[y][x] = "#"

        m = re.search("rotate column x=([0-9]+) by ([0-9]+)", cur)
        if m:
            shift = int(m.group(2))
            x = int(m.group(1))
            vals = [grid[y][x] for y in range(height)]
            for y in range(height):
                grid[(y + shift) % height][x] = vals[y]

        m = re.search("rotate row y=([0-9]+) by ([0-9]+)", cur)
        if m:
            shift = int(m.group(2))
            y = int(m.group(1))
            vals = [grid[y][x] for x in range(width)]
            for x in range(width):
                grid[y][(x + shift) % width] = vals[x]

    ret = 0

    for row in grid:
        for cell in row:
            if cell == "#":
                ret += 1

    if show:
        for row in grid:
            log("".join(row))

    return ret


def test(log):
    values = [
        "rect 3x2",
        "rotate column x=1 by 1",
        "rotate row y=0 by 4",
        "rotate column x=1 by 1",
    ]

    if calc(log, values, 7, 3, True) == 6:
        return True
    else:
        return False


def run(log, values):
    log(calc(log, values, 50, 6, True))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in [[], ["Puzzles"], ["..", "Puzzles"]]:
                cur = os.path.join(*(dn + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!"); exit(1)
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
