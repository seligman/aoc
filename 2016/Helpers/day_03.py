#!/usr/bin/env python3

import re

DAY_NUM = 3
DAY_DESC = 'Day 3: Squares With Three Sides'


def calc(values, mode):
    valid = 0

    r = re.compile("([0-9]+) +([0-9]+) +([0-9]+)")
    tris = []
    for cur in values:
        m = r.search(cur)
        vals = [int(x) for x in m.groups()]
        tris.append(vals)

    if mode == 1:
        for i in range(0, len(tris), 3):
            tris[i], tris[i+1], tris[i+2] = (
                [tris[i][0], tris[i+1][0], tris[i+2][0]],
                [tris[i][1], tris[i+1][1], tris[i+2][1]],
                [tris[i][2], tris[i+1][2], tris[i+2][2]],
            )

    for vals in tris:
        m = max(vals)
        if sum(vals) - m > m:
            valid += 1

    return valid


def test(log):
    values = [
        "  5  10  25",
    ]

    if calc(values, 0) == 0:
        return True
    else:
        return False


def run(log, values):
    log.show(calc(values, 0))
    log.show(calc(values, 1))
