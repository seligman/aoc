#!/usr/bin/env python3

import itertools

DAY_NUM = 2
DAY_DESC = 'Day 2: Corruption Checksum'


def calc(log, values):
    values = [[int(y) for y in x.replace('\t', ' ').split(' ')] for x in values]
    ret = 0
    ret2 = 0

    for row in values:
        a, b = min(row), max(row)
        ret += b - a
        for a, b in itertools.combinations(row, 2):
            if b > a:
                a, b = b, a
            if a % b == 0:
                ret2 += a // b

    log("Second form: " + str(ret2))

    return ret


def test(log):
    values = [
        "5 1 9 5",
        "7 5 3",
        "2 4 6 8",
    ]

    if calc(log, values) == 18:
        return True
    else:
        return False


def run(log, values):
    log(calc(log, values))

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
