#!/usr/bin/env python3

import re

def get_desc():
    return 17, 'Day 17: Trick Shot'

def calc(log, values, mode):
    m = re.search(r"target area: x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)", values[0])
    x1, x2, y1, y2 = int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))

    possible = 0
    overall_best = 0

    for zy in range(-300, 300):
        for x in range(-300, 300):
            y = zy
            ox, oy = 0, 0
            best = 0

            for _ in range(300):
                ox += x
                oy += y
                y -= 1
                if x > 0:
                    x -= 1
                elif x < 0:
                    x += 1
                best = max(best, oy)

                if ox >= x1 and ox <= x2 and oy >= y1 and oy <= y2:
                    possible += 1
                    if mode == 1:
                        overall_best = max(best, overall_best)
                    break

    if mode == 1:
        return overall_best
    else:
        return possible

def test(log):
    values = log.decode_values("""
        target area: x=20..30, y=-10..-5
    """)

    log.test(calc(log, values, 1), 45)
    log.test(calc(log, values, 2), 112)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))
