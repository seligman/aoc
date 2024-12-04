#!/usr/bin/env python3

import re
from collections import defaultdict

DAY_NUM = 2
DAY_DESC = 'Day 2: Password Philosophy'

def calc(log, values, mode):
    r = re.compile("([0-9]+)-([0-9]+) ([a-z]): ([a-z]+)")
    ret = 0
    for cur in values:
        m = r.search(cur)
        a, b = int(m.group(1)), int(m.group(2))
        target = m.group(3)
        pw = m.group(4)

        if mode == 1:
            counts = defaultdict(int)
            for x in pw:
                counts[x] += 1
            if counts[target] >= a and counts[target] <= b:
                ret += 1
        else:
            if (pw[a-1] == target and pw[b-1] != target) or (pw[a-1] != target and pw[b-1] == target):
                ret += 1

    return ret

def test(log):
    values = log.decode_values("""
        1-3 a: abcde
        1-3 b: cdefg
        2-9 c: ccccccccc
    """)

    log.test(calc(log, values, 1), 2)
    log.test(calc(log, values, 2), 1)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2020/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
