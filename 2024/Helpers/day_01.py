#!/usr/bin/env python3

DAY_NUM = 1
DAY_DESC = 'Day 1: Historian Hysteria'

from collections import Counter

def calc(log, values, mode):
    values = [list(map(int, x.split())) for x in values]
    a, b = [x[0] for x in values], [x[1] for x in values]

    ret = 0    
    if mode == 1:
        for a, b in zip(sorted(a), sorted(b)):
            ret += abs(a - b)
    else:
        b = Counter(b)
        for val, hits in Counter(a).items():
            ret += hits * val * b[val]
    return ret

def test(log):
    values = log.decode_values("""
        3   4
        4   3
        2   5
        1   3
        3   9
        3   3
    """)

    log.test(calc(log, values, 1), 11)
    log.test(calc(log, values, 2), 31)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in [[], ["Puzzles"], ["..", "Puzzles"]]:
                cur = os.path.join(*(dn + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
