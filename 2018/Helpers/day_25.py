#!/usr/bin/env python3

from collections import deque

DAY_NUM = 25
DAY_DESC = 'Day 25: Four-Dimensional Adventure'


def get_points(values):
    ret = []
    for cur in values:
        ret.append([int(x) for x in cur.split(",")])
    return ret


def dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2]) + abs(a[3] - b[3])


def calc(values):
    points = get_points(values)
    
    ret = 0
    all_used = set()

    while True:
        used = set()
        to_check = deque()
        for i in range(len(points)):
            if i not in all_used:
                to_check.append(i)
                break

        while len(to_check) > 0:
            cur = to_check.popleft()
            used.add(cur)
            all_used.add(cur)
            for i in range(len(points)):
                if i not in used and i not in all_used:
                    if dist(points[i], points[cur]) <= 3:
                        to_check.append(i)

        if len(used) == 0:
            break
        ret += 1

    return ret


def test(log):
    values = [
        "-1,2,2,0",
        "0,0,2,-2",
        "0,0,0,-2",
        "-1,2,0,0",
        "-2,-2,-2,2",
        "3,0,2,-1",
        "-1,3,2,2",
        "-1,0,-1,0",
        "0,2,1,-2",
        "3,0,0,0",
    ]

    if calc(values) == 4:
        return True
    else:
        return False


def run(log, values):
    log(calc(values))

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
