#!/usr/bin/env python3

from collections import deque

DAY_NUM = 19
DAY_DESC = 'Day 19: An Elephant Named Joseph'


def calc2(values):
    elves = int(values[0])
    left = deque()
    right = deque()
    for i in range(1, elves + 1):
        if i < (elves / 2) + 1:
            left.append(i)
        else:
            right.appendleft(i)

    while len(left) > 0 and len(right) > 0:
        if len(left) > len(right):
            left.pop()
        else:
            right.pop()

        right.appendleft(left.popleft())
        left.append(right.pop())

    if len(left) > 0:
        return left.pop()
    else:
        return right.pop()


def calc(values):
    elves = int(values[0])
    has_presents = deque(range(1, elves + 1))

    while len(has_presents) > 1:
        has_presents.rotate(-1)
        has_presents.popleft()

    return has_presents.pop()


def test(log):
    values = [
        "5",
    ]

    if calc(values) == 3:
        if calc2(values) == 2:
            return True
        else:
            return False
    else:
        return False


def run(log, values):
    log("To the left: " + str(calc(values)))
    log("Across the circle: " + str(calc2(values)))

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
