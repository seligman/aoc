#!/usr/bin/env python

import re

def get_desc():
    return 3, 'Day 3: No Matter How You Slice It'


def calc(log, values):
    max_width = 0
    max_height = 0
    for _claim, left, top, width, height in values:
        max_width = max(max_width, left + width)
        max_height = max(max_height, top + height)

    grid = [0] * (max_width * max_height)
    valid = []
    for _claim, left, top, width, height in values:
        for x in range(left, left + width):
            for y in range(top, top + height):
                i = x + y * max_width
                grid[i] += 1

    for claim, left, top, width, height in values:
        good = True
        for x in range(left, left + width):
            if not good:
                break
            for y in range(top, top + height):
                i = x + y * max_width
                if grid[i] != 1:
                    good = False
                    break
        if good:
            valid.append(claim)

    over_used = 0

    for tile in grid:
        if tile > 1:
            over_used += 1

    log.show("Valid Claims: " + ", ".join([str(x) for x in valid]))

    return over_used


def test(log):
    return True


def run(log, values):
    r = re.compile("#([0-9]+) @ ([0-9]+),([0-9]+): ([0-9]+)x([0-9]+)")
    temp = []
    for cur in values:
        m = r.search(cur)
        if m:
            temp.append([int(x) for x in m.groups()])
    log.show(calc(log, temp))
