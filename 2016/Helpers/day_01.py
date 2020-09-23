#!/usr/bin/env python

from collections import defaultdict

def get_desc():
    return 1, 'Day 1: No Time for a Taxicab'


def calc(log, values):
    values = values[0].split(", ")

    x, y = 0, 0
    face = 0
    path = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    seen = defaultdict(int)
    shown = False

    seen[(x, y)] += 1

    for cur in values:
        if cur[0] == "L":
            face = (face + 3) % 4
        else:
            face = (face + 1) % 4
        mul = int(cur[1:])

        for _ in range(mul):
            x += 1 * path[face][0]
            y += 1 * path[face][1]
            seen[(x, y)] += 1
            if not shown:
                if seen[(x, y)] == 2:
                    shown = True
                    log.show("Visited %s[%d] x %s[%d] twice, which is %d away." % (
                        "W" if x < 0 else "E",
                        abs(x), 
                        "N" if y < 0 else "S",
                        abs(y), 
                        abs(x) + abs(y)))

    return abs(x) + abs(y)


def test(log):
    values = [
        "R5, L5, R5, R3",
    ]

    if calc(log, values) == 12:
        return True
    else:
        return False


def run(log, values):
    log.show(calc(log, values))
