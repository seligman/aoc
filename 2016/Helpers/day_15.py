#!/usr/bin/env python3

import re

DAY_NUM = 15
DAY_DESC = 'Day 15: Timing is Everything'

def calc(values, extra=None):
    discs = []
    r = re.compile("has ([0-9]+) positions; at time=0, it is at position ([0-9]+)\\.")
    for cur in values:
        m = r.search(cur)
        discs.append([int(x) for x in m.groups()])

    if extra is not None:
        discs.append(extra)

    tick = 0
    while True:
        good = True
        for i in range(len(discs)):
            if (tick + i + 1 + discs[i][1]) % (discs[i][0]) != 0:
                good = False
                break
        if good:
            return tick
        tick += 1

def test(log):
    values = [
        "Disc #1 has 5 positions; at time=0, it is at position 4.",
        "Disc #2 has 2 positions; at time=0, it is at position 1.",
    ]

    if calc(values) == 5:
        return True
    else:
        return False

def run(log, values):
    log("Part 1: %d" % (calc(values),))
    log("Part 2: %d" % (calc(values, (11, 0)),))

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
