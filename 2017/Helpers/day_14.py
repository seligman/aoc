#!/usr/bin/env python3

from collections import deque

DAY_NUM = 14
DAY_DESC = 'Day 14: Disk Defragmentation'


def knot_hash(value):
    values = [ord(x) for x in list(value)] + [17, 31, 73, 47, 23]
    i = 0
    skip = 0
    elements = list(range(256))

    for _ in range(64):
        for cur in values:
            for x in range(cur // 2):
                a, b = (i + x) % len(elements), (i + (cur-1) - x) % len(elements)
                elements[a], elements[b] = elements[b], elements[a]
            i = (i + skip + cur) % len(elements)
            skip += 1

    ret = ""
    for i in range(0, 256, 16):
        temp = 0
        for j in range(16):
            temp ^= elements[i+j]
        ret += "%02x" % (temp,)

    return ret


def calc(log, values):
    ret = 0

    bits = {
        "0": 0, "1": 1, "2": 1, "3": 2,
        "4": 1, "5": 2, "6": 2, "7": 3,
        "8": 1, "9": 2, "a": 2, "b": 3,
        "c": 2, "d": 3, "e": 3, "f": 4,
    }

    grids = {
        '0': [],
        '1': [3],
        '2': [2],
        '3': [3, 2],
        '4': [1],
        '5': [3, 1],
        '6': [2, 1],
        '7': [3, 2, 1],
        '8': [0],
        '9': [3, 0],
        'a': [2, 0],
        'b': [3, 2, 0],
        'c': [1, 0],
        'd': [3, 1, 0],
        'e': [2, 1, 0],
        'f': [3, 2, 1, 0],
    }

    grid = set()

    for i in range(128):
        val = knot_hash(values[0] + "-" + str(i))
        x = 0
        for cur in val:
            ret += bits[cur]
            for bit in grids[cur]:
                grid.add((x + bit, i))
            x += 4

    groups = 0
    while len(grid) > 0:
        todo = deque()
        x, y = list(grid)[0]
        todo.append((x, y))
        grid.remove((x, y))
        groups += 1
        while len(todo) > 0:
            x, y = todo.popleft()
            for tx, ty in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                if (tx, ty) in grid:
                    grid.remove((tx, ty))
                    todo.append((tx, ty))

    log("There are " + str(groups) + " groups.")

    return ret


def test(log):
    values = [
        "flqrgnkx",
    ]

    if calc(log, values) == 8108:
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
