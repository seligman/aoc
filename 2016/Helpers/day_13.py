#!/usr/bin/env python3

from collections import deque

DAY_NUM = 13
DAY_DESC = 'Day 13: A Maze of Twisty Little Cubicles'


def calc_point(x, y, num):
    num = ((x * x) + (3 * x) + (2 * x * y) + y + (y * y)) + num
    ret = 0
    while num > 0:
        if num & 1 == 1:
            ret += 1
        num >>= 1
    if ret % 2 == 0:
        return "."
    else:
        return "#"


def calc(values, target_x, target_y, target_dist):
    num = int(values[0])
    seen = set()
    todo = deque()

    todo.append([1, 1, 0])

    dirs = [[-1, 0], [1, 0], [0, -1], [0, 1]]
    while len(todo) > 0:
        sx, sy, cost = todo.popleft()
        if (sx, sy) not in seen:
            seen.add((sx, sy))
            skip = False
            if target_x is not None:
                if sx == target_x and sy == target_y:
                    return cost
            elif target_dist is not None:
                if cost == target_dist:
                    skip = True

            if not skip:
                for off_x, off_y in dirs:
                    x = off_x + sx
                    y = off_y + sy
                    if x >= 0 and y >= 0:
                        if calc_point(x, y, num) == ".":
                            todo.append((x, y, cost + 1))

    return len(seen)


def test(log):
    values = [
        "10",
    ]

    if calc(values, 7, 4, None) == 11:
        return True
    else:
        return False


def run(log, values):
    log(calc(values, 31, 39, None))
    log(calc(values, None, None, 50))

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
