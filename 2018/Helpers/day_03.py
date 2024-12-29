#!/usr/bin/env python3

import re

DAY_NUM = 3
DAY_DESC = 'Day 3: No Matter How You Slice It'

def calc(log, values):
    max_width = 0
    max_height = 0
    for _claim, left, top, width, height in values:
        max_width = max(max_width, left + width)
        max_height = max(max_height, top + height)

    grid = [0] * (max_width * max_height)
    valid = []
    for _claim, left, top, width, height in values:
        for x in range(left, left + width):
            for y in range(top, top + height):
                i = x + y * max_width
                grid[i] += 1

    for claim, left, top, width, height in values:
        good = True
        for x in range(left, left + width):
            if not good:
                break
            for y in range(top, top + height):
                i = x + y * max_width
                if grid[i] != 1:
                    good = False
                    break
        if good:
            valid.append(claim)

    over_used = 0

    for tile in grid:
        if tile > 1:
            over_used += 1

    log("Part 2: " + ", ".join([str(x) for x in valid]))

    return over_used

def test(log):
    return True

def run(log, values):
    r = re.compile("#([0-9]+) @ ([0-9]+),([0-9]+): ([0-9]+)x([0-9]+)")
    temp = []
    for cur in values:
        m = r.search(cur)
        if m:
            temp.append([int(x) for x in m.groups()])
    log("Part 1: %d" % (calc(log, temp),))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2018/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
