#!/usr/bin/env python3

from collections import defaultdict

DAY_NUM = 8
DAY_DESC = 'Day 8: I Heard You Like Registers'


def comp(a, b, c):
    if b == "==":
        return a == c
    elif b == ">":
        return a > c
    elif b == "<":
        return a < c
    elif b == ">=":
        return a >= c
    elif b == "<=":
        return a <= c
    elif b == "!=":
        return a != c
    else:
        raise Exception()


def calc(log, values):
    r = defaultdict(int)
    m_val = 0

    for cur in values:
        cur = cur.split(' ')
        if comp(r[cur[4]], cur[5], int(cur[6])):
            if cur[1] == "inc":
                r[cur[0]] += int(cur[2])
            elif cur[1] == "dec":
                r[cur[0]] -= int(cur[2])
            else:
                raise Exception()
        m_val = max(m_val, max(r.values()))

    log.show("Max value: " + str(m_val))

    return max(r.values())


def test(log):
    values = [
        "b inc 5 if a > 1",
        "a inc 1 if b < 5",
        "c dec -10 if a >= 1",
        "c inc -20 if c == 10",
    ]

    if calc(log, values) == 1:
        return True
    else:
        return False


def run(log, values):
    log.show(calc(log, values))
