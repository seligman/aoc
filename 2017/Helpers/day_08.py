#!/usr/bin/env python3

from collections import defaultdict

DAY_NUM = 8
DAY_DESC = 'Day 8: I Heard You Like Registers'

def comp(a, b, c):
    if b == "==":
        return a == c
    elif b == ">":
        return a > c
    elif b == "<":
        return a < c
    elif b == ">=":
        return a >= c
    elif b == "<=":
        return a <= c
    elif b == "!=":
        return a != c
    else:
        raise Exception()

def calc(log, values):
    r = defaultdict(int)
    m_val = 0

    for cur in values:
        cur = cur.split(' ')
        if comp(r[cur[4]], cur[5], int(cur[6])):
            if cur[1] == "inc":
                r[cur[0]] += int(cur[2])
            elif cur[1] == "dec":
                r[cur[0]] -= int(cur[2])
            else:
                raise Exception()
        m_val = max(m_val, max(r.values()))

    log("Part 2: " + str(m_val))

    return max(r.values())

def test(log):
    values = [
        "b inc 5 if a > 1",
        "a inc 1 if b < 5",
        "c dec -10 if a >= 1",
        "c inc -20 if c == 10",
    ]

    if calc(log, values) == 1:
        return True
    else:
        return False

def run(log, values):
    log("Part 1: %d" % (calc(log, values),))

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
