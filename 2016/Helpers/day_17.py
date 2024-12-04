#!/usr/bin/env python3

from hashlib import md5
from collections import deque

DAY_NUM = 17
DAY_DESC = 'Day 17: Two Steps Forward'


def calc(values):
    valid = "bcdef"
    key = values[0]
    dirs = [[0, -1, "U", 0], [0, 1, "D", 1], [-1, 0, "L", 2], [1, 0, "R", 3]]

    todo = deque()
    todo.append([0, 0, ""])

    shortest, longest = None, 0

    while len(todo) > 0:
        x, y, path = todo.popleft()
        if x == 3 and y == 3:
            if shortest is None:
                shortest = path
            elif len(path) > longest:
                longest = len(path)
        else:
            cur_hash = md5((key + path).encode("utf8")).hexdigest()
            for ox, oy, step, code_index in dirs:
                if cur_hash[code_index] in valid:
                    tx = x + ox
                    ty = y + oy
                    if tx >= 0 and ty >= 0 and tx < 4 and ty < 4:
                        todo.append((tx, ty, path + step))

    return shortest, longest


def test(log):
    values = [
        "ulqzkmiv",
    ]

    if calc(values) == ("DRURDRUDDLLDLUURRDULRLDUUDDDRR", 830):
        return True
    else:
        return False


def run(log, values):
    vals = calc(values)
    log("The shortest path is: " + vals[0])
    log("The longest path took %d steps." % (vals[1],))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2016/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
