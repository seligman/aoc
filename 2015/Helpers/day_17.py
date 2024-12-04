#!/usr/bin/env python3

import itertools
from collections import defaultdict

DAY_NUM = 17
DAY_DESC = 'Day 17: No Such Thing as Too Much'


def calc(log, values, target):
    values = [int(x) for x in values]
    ret = 0
    used = defaultdict(int)
    for i in range(1, len(values)+1):
        for test in itertools.combinations(values, i):
            if sum(test) == target:
                ret += 1
                used[len(test)] += 1

    min_size = min(used)
    log("%d options with %d buckets" % (used[min_size], min_size))

    return ret


def test(log):
    values = [
        "20", 
        "15", 
        "10", 
        "5", 
        "5", 
    ]

    if calc(log, values, 25) == 4:
        return True
    else:
        return False


def run(log, values):
    log(calc(log, values, 150))

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
