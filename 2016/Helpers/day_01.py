#!/usr/bin/env python3

from collections import defaultdict

DAY_NUM = 1
DAY_DESC = 'Day 1: No Time for a Taxicab'


def calc(log, values):
    values = values[0].split(", ")

    x, y = 0, 0
    face = 0
    path = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    seen = defaultdict(int)
    shown = False

    seen[(x, y)] += 1

    for cur in values:
        if cur[0] == "L":
            face = (face + 3) % 4
        else:
            face = (face + 1) % 4
        mul = int(cur[1:])

        for _ in range(mul):
            x += 1 * path[face][0]
            y += 1 * path[face][1]
            seen[(x, y)] += 1
            if not shown:
                if seen[(x, y)] == 2:
                    shown = True
                    log("Visited %s[%d] x %s[%d] twice, which is %d away." % (
                        "W" if x < 0 else "E",
                        abs(x), 
                        "N" if y < 0 else "S",
                        abs(y), 
                        abs(x) + abs(y)))

    return abs(x) + abs(y)


def test(log):
    values = [
        "R5, L5, R5, R3",
    ]

    if calc(log, values) == 12:
        return True
    else:
        return False


def run(log, values):
    log(calc(log, values))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2016/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
