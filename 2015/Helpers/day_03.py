#!/usr/bin/env python3

from collections import deque

DAY_NUM = 3
DAY_DESC = 'Day 3: Perfectly Spherical Houses in a Vacuum'


def calc(values, units):
    dirs = {
        '^': (0, -1),
        'v': (0, 1),
        '<': (-1, 0),
        '>': (1, 0),
    }

    locs = deque()
    for _ in range(units):
        locs.append((0, 0))

    seen = set()
    seen.add((0, 0))

    for line in values:
        for cur in line:
            if cur in dirs:
                x, y = locs.popleft()
                off = dirs[cur]
                x += off[0]
                y += off[1]
                seen.add((x, y))
                locs.append((x, y))

    return len(seen)


def test(log):
    values = [
        "^>v<",
    ]

    if calc(values, 1) == 4:
        return True
    else:
        return False


def run(log, values):
    log("With 1 worker: %d" % (calc(values, 1),))
    log("With 2 workers: %d" % (calc(values, 2),))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in [[], ["Puzzles"], ["..", "Puzzles"]]:
                cur = os.path.join(*(dn + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!"); exit(1)
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
