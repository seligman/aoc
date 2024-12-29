#!/usr/bin/env python3

import re

DAY_NUM = 10
DAY_DESC = 'Day 10: Balance Bots'

def calc(log, values):
    bots = {}

    while True:
        for i in range(len(values)):
            if values[i] is not None:
                m = re.search("value ([0-9]+) goes to (bot [0-9]+)", values[i])
                if m:
                    if m.group(2) not in bots:
                        bots[m.group(2)] = []
                    bots[m.group(2)].append(m.group(1))
                    values[i] = None

            if values[i] is not None:
                m = re.search("(bot [0-9]+) gives low to (.*) and high to (.*)", values[i])
                if m:
                    if m.group(1) in bots and len(bots[m.group(1)]) == 2:
                        a, b = m.group(2), m.group(3)
                        if a not in bots:
                            bots[a] = []
                        if b not in bots:
                            bots[b] = []

                        if bots[m.group(1)][0] in {"61", "17"} and bots[m.group(1)][1] in {"61", "17"}:
                            log("Part 1: " + m.group(1).split(" ")[-1])

                        if int(bots[m.group(1)][0]) < int(bots[m.group(1)][1]):
                            bots[a].append(bots[m.group(1)][0])
                            bots[b].append(bots[m.group(1)][1])
                        else:
                            bots[a].append(bots[m.group(1)][1])
                            bots[b].append(bots[m.group(1)][0])

                        a = bots.get("output 0", None)
                        b = bots.get("output 1", None)
                        c = bots.get("output 2", None)

                        if a is not None and b is not None and c is not None:
                            log("Part 2: " + str(int(a[0]) * int(b[0]) * int(c[0])))
                            return

                        bots[m.group(1)] = []

def test(log):
    return True

def run(log, values):
    calc(log, values)

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
