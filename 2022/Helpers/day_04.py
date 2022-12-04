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

    return 0

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
    log(calc(log, values, 1))
    log(calc(log, values, 2))

if __name__ == "__main__":
    import sys, os
    cur = None
    for cur in sys.argv[1:] + ["input.txt", "day_##_input.txt", "Puzzles/day_##_input.txt", "../Puzzles/day_##_input.txt"]:
        cur = os.path.join(*cur.split("/")).replace("##", f"{DAY_NUM:02d}")
        if os.path.isfile(cur): fn = cur; break
    if cur is None: print("Unable to find input file!"); exit(1)
    with open(fn) as f: values = f.readlines()
    print(f"Running day {DAY_DESC}:")
    run(print, values)
