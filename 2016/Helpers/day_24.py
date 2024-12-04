#!/usr/bin/env python3

from collections import deque
import itertools

DAY_NUM = 24
DAY_DESC = 'Day 24: Air Duct Spelunking'


def calc(log, values, zero_finish):
    values = [list(x) for x in values]
    digits = []
    digit_pos = {}

    for y in range(len(values)):
        for x in range(len(values[y])):
            cur = values[y][x]
            if cur not in {"#", "."}:
                if cur != "0":
                    digits.append(cur)
                digit_pos[cur] = (x, y)

    distances = {}

    for start, end in itertools.combinations(["0"] + digits, 2):
        todo = deque()
        seen = set()
        todo.append((0, digit_pos[start][0], digit_pos[start][1]))

        while True:
            steps, x, y = todo.popleft()
            if values[y][x] == end:
                distances[(start, end)] = steps
                distances[(end, start)] = steps
                break
            for tx, ty in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
                if (tx, ty) not in seen:
                    seen.add((tx, ty))
                    if tx >= 0 and ty >= 0 and tx < len(values[0]) and ty < len(values):
                        if values[ty][tx] != "#":
                            todo.append((steps + 1, tx, ty))

    best_total = None

    for perm in itertools.permutations(digits, len(digits)):
        perm = list(perm)
        perm.insert(0, "0")
        if zero_finish:
            perm.append("0")

        total = 0
        for i in range(1, len(perm)):
            total += distances[(perm[i-1], perm[i])]
            if best_total is not None and total >= best_total:
                break

        if best_total is None or total < best_total:
            best_total = total 

    return best_total


def test(log):
    values = [
        "###########",
        "#0.1.....2#",
        "#.#######.#",
        "#4.......3#",
        "###########",
    ]

    if calc(log, values, False) == 14:
        return True
    else:
        return False


def run(log, values):
    log("Finish anywhere: " + str(calc(log, values, False)))
    log("Finish at the start: " + str(calc(log, values, True)))

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
