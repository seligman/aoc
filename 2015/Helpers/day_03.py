#!/usr/bin/env python3

from collections import deque

def get_desc():
    return 3, 'Day 3: Perfectly Spherical Houses in a Vacuum'


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
    log.show("With 1 worker: %d" % (calc(values, 1),))
    log.show("With 2 workers: %d" % (calc(values, 2),))
