#!/usr/bin/env python3

from collections import deque

DAY_NUM = 10
DAY_DESC = 'Day 10: Elves Look, Elves Say'


def calc(values, loops):
    look = deque(values[0])

    while loops > 0:
        loops -= 1
        last = None
        count = 0
        say = deque()
        for cur in look:
            if last is not None:
                if last != cur:
                    say.extend("%d%s" % (count, last))
                    count = 0
            last = cur
            count += 1
        say.extend("%d%s" % (count, last))
        look = say

    return len(look)


def test(log):
    values = [
        "1",
    ]

    if calc(values, 5) == len("312211"):
        return True
    else:
        return False


def run(log, values):
    log(calc(values, 40))
    log(calc(values, 50))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2015/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
