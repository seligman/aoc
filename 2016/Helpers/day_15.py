#!/usr/bin/env python3

import re

DAY_NUM = 15
DAY_DESC = 'Day 15: Timing is Everything'


def calc(values, extra=None):
    discs = []
    r = re.compile("has ([0-9]+) positions; at time=0, it is at position ([0-9]+)\\.")
    for cur in values:
        m = r.search(cur)
        discs.append([int(x) for x in m.groups()])

    if extra is not None:
        discs.append(extra)

    tick = 0
    while True:
        good = True
        for i in range(len(discs)):
            if (tick + i + 1 + discs[i][1]) % (discs[i][0]) != 0:
                good = False
                break
        if good:
            return tick
        tick += 1


def test(log):
    values = [
        "Disc #1 has 5 positions; at time=0, it is at position 4.",
        "Disc #2 has 2 positions; at time=0, it is at position 1.",
    ]

    if calc(values) == 5:
        return True
    else:
        return False


def run(log, values):
    log.show(calc(values))
    log.show(calc(values, (11, 0)))
