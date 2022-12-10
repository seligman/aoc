#!/usr/bin/env python3

import re

DAY_NUM = 6
DAY_DESC = 'Day 6: Probably a Fire Hazard'


def calc(values, rules):
    r = re.compile("(turn on|turn off|toggle) ([0-9]+),([0-9]+) through ([0-9]+),([0-9]+)")
    grid = [[0] * 1000 for _ in range(1000)]

    for cur in values:
        m = r.search(cur)
        if m:
            step, x1, y1, x2, y2 = m.groups()
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            x_range = range(x1, x2 + 1)
            y_range = range(y1, y2 + 1)

            if rules == 0:
                if step == "turn on":
                    for x in x_range:
                        for y in y_range:
                            grid[x][y] = 1
                elif step == "turn off":
                    for x in x_range:
                        for y in y_range:
                            grid[x][y] = 0
                elif step == "toggle":
                    for x in x_range:
                        for y in y_range:
                            grid[x][y] = 1 - grid[x][y]
            else:
                if step == "turn on":
                    for x in x_range:
                        for y in y_range:
                            grid[x][y] += 1
                elif step == "turn off":
                    for x in x_range:
                        for y in y_range:
                            if grid[x][y] > 0:
                                grid[x][y] -= 1
                elif step == "toggle":
                    for x in x_range:
                        for y in y_range:
                            grid[x][y] += 2

    return sum([sum(x) for x in grid])


def test(log):
    values = [
        "turn on 499,499 through 500,500",
    ]

    if calc(values, 0) == 4:
        return True
    else:
        return False


def run(log, values):
    log.show(calc(values, 0))
    log.show(calc(values, 1))
