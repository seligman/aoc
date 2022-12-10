#!/usr/bin/env python3

from collections import deque

DAY_NUM = 12
DAY_DESC = 'Day 12: Digital Plumber'


def calc(log, values):
    progs = {}
    remaining = set()
    for cur in values:
        cur = cur.split(" <-> ")
        remaining.add(cur[0])
        progs[cur[0]] = cur[1].split(", ")

    groups = []

    while len(remaining) > 0:
        cur = list(remaining)[0]
        seen = set()
        seen.add(cur)
        todo = deque()
        todo.append(cur)
        remaining.remove(cur)
        while len(todo) > 0:
            cur = todo.popleft()
            for sub in progs[cur]:
                if sub not in seen:
                    remaining.remove(sub)
                    seen.add(sub)
                    todo.append(sub)
        groups.append(seen)

    log("There are " + str(len(groups)) + " groups")

    for group in groups:
        if "0" in group:
            return len(group)

    return None


def test(log):
    values = [
        "0 <-> 2",
        "1 <-> 1",
        "2 <-> 0, 3, 4",
        "3 <-> 2, 4",
        "4 <-> 2, 3, 6",
        "5 <-> 6",
        "6 <-> 4, 5",
    ]

    if calc(log, values) == 6:
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
    if fn is None: print("Unable to find input file!"); exit(1)
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
