#!/usr/bin/env python3

from collections import deque

DAY_NUM = 17
DAY_DESC = 'Day 17: Spinlock'

def calc(log, values, mode):
    value = int(values[0])

    spin = deque()
    spin.append(0)
    i = 0

    rounds = 2017 if mode == 0 else 50000000
    while rounds > 0:
        rounds -= 1
        spin.rotate(-value)
        i += 1
        spin.append(i)

    if mode == 0:
        return spin.popleft()
    else:
        while spin.popleft() != 0:
            pass
        return spin.popleft()

def test(log):
    values = [
        "3",
    ]

    if calc(log, values, 0) == 638:
        return True
    else:
        return False

def run(log, values):
    log("Part 1: %d" % (calc(log, values, 0),))
    log("Part 2: %d" % (calc(log, values, 1),))

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
