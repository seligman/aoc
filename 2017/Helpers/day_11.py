#!/usr/bin/env python3

from collections import deque

DAY_NUM = 11
DAY_DESC = 'Day 11: Hex Ed'

def dist(tx, ty):
    tx = abs(tx)
    ty = abs(ty)

    if ty > tx:
        return ty + tx // 2
    else:
        return tx

def calc(log, values):
    longest = 0

    x, y = 0, 0
    left = 0
    for cur in values[0].split(","):
        left += 1

    for cur in values[0].split(","):
        left -= 1
        if x % 2 == 0:
            offs = {"nw": (-1, -1), "n": (0, -1), "ne": (1, -1), "sw": (-1, 0), "s": (0, 1), "se": (1, 0)}
        else:
            offs = {"nw": (-1, 0), "n": (0, -1), "ne": (1, 0), "sw": (-1, 1), "s": (0, 1), "se": (1, 1)}
        x, y = x + offs[cur][0], y + offs[cur][1]
        cur_dist = dist(x, y)
        if cur_dist > longest:
            longest = cur_dist

    log("Part 2: " + str(longest))

    return dist(x, y)

def test(log):
    values = [
        "se,sw,se,sw,sw",
    ]

    if calc(log, values) == 2:
        return True
    else:
        return False

def run(log, values):
    log("Part 1: %d" % (calc(log, values),))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2017/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
