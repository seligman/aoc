#!/usr/bin/env python3

import re

def get_desc():
    return 17, 'Day 17: Trick Shot'

def calc(log, values, mode):
    m = re.search(r"target area: x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)", values[0])
    x1, x2, y1, y2 = int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))

    possible = 0
    overall_best = 0

    for zy in range(-max(abs(y1), abs(y2))*2, max(abs(y1), abs(y2))*2+1):
        for x in range(0, abs(x2)+1):
            y = zy
            ox, oy = 0, 0
            best = 0

            for _ in range(max(abs(x1), abs(x2), abs(y1), abs(y2))*2):
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
                if oy < -500 and y <= 0:
                    break
                if x == 0 and (ox < x1 or ox > x2):
                    break

    return overall_best, possible

def test(log):
    values = log.decode_values("""
        target area: x=20..30, y=-10..-5
    """)

    overall_best, possible = calc(log, values, 1)
    log.test(overall_best, 45)
    log.test(possible, 112)

def run(log, values):
    overall_best, possible = calc(log, values, 1)
    log(overall_best)
    log(possible)
