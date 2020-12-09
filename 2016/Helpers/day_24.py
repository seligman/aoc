#!/usr/bin/env python3

from collections import deque
import itertools

def get_desc():
    return 24, 'Day 24: Air Duct Spelunking'


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
    log.show("Finish anywhere: " + str(calc(log, values, False)))
    log.show("Finish at the start: " + str(calc(log, values, True)))
