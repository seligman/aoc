#!/usr/bin/env python3

def get_desc():
    return 3, 'Day 3: Spiral Memory'


def calc(log, values):
    value = int(values[0])
    cur = 1
    x, y = 0, 0
    change = 1

    wrote = {(0,0): 1}

    while True:
        for dx, dy, inc in ((1, 0, 0), (0, -1, 1), (-1, 0, 0), (0, 1, 1)):
            for _ in range(change):
                x += dx
                y += dy
                cur += 1

                if wrote is not None:
                    write = 0
                    for ox, oy in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)):
                        ox += x
                        oy += y
                        write += wrote.get((ox, oy), 0)
                    if write > value:
                        log.show("First greater: " + str(write))
                        wrote = None
                    if wrote is not None:
                        wrote[(x, y)] = write

                if cur == value:
                    return abs(x) + abs(y)
            change += inc


def test(log):
    values = [
        "1024",
    ]

    if calc(log, values) == 31:
        return True
    else:
        return False


def run(log, values):
    log.show(calc(log, values))
