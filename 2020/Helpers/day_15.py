#!/usr/bin/env python3

from collections import defaultdict, deque

DAY_NUM = 15
DAY_DESC = 'Day 15: Rambunctious Recitation'

def calc(log, values, mode):
    numbers = [int(x) for x in values[0].split(",")]

    said = {}
    last = None

    for i in range(len(numbers)):
        said[last], last = i, numbers[i]

    for i in range(len(numbers), 2020 if mode == 1 else 30000000):
        said[last], last = i, i - said.get(last, i)
        if (mode == 1 and i % 1000 == 19) or (mode == 2 and i % 5000000 == 999999):
            log(f"For round {i:8d}, {last:8d} was said")

    return last

def test(log):
    values = log.decode_values("""
        0,3,6
    """)

    log.test(calc(log, values, 1), 436)
    # log.test(calc(log, values, 2), 175594)

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
