#!/usr/bin/env python3

DAY_NUM = 4
DAY_DESC = 'Day 4: Camp Cleanup'

def calc(log, values, mode):
    ret = 0
    for row in values:
        row = row.split(",")
        a = list(map(int, row[0].split("-")))
        b = list(map(int, row[1].split("-")))
        a = set(range(a[0], a[1] + 1))
        b = set(range(b[0], b[1] + 1))
        if mode == 1:
            if len(a & b) == min(len(a), len(b)):
                ret += 1
        else:
            if len(a & b) > 0:
                ret += 1
    return ret

def test(log):
    values = log.decode_values("""
        2-4,6-8
        2-3,4-5
        5-7,7-9
        2-8,3-7
        6-6,4-6
        2-6,4-8
    """)

    log.test(calc(log, values, 1), 2)
    log.test(calc(log, values, 2), 4)

def run(log, values):
    log(f"Part 1: {calc(log, values, 1)}")
    log(f"Part 2: {calc(log, values, 2)}")

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2022/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
