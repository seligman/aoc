#!/usr/bin/env python

import itertools

def get_desc():
    return 2, 'Day 2: Corruption Checksum'


def calc(log, values):
    values = [[int(y) for y in x.replace('\t', ' ').split(' ')] for x in values]
    ret = 0
    ret2 = 0

    for row in values:
        a, b = min(row), max(row)
        ret += b - a
        for a, b in itertools.combinations(row, 2):
            if b > a:
                a, b = b, a
            if a % b == 0:
                ret2 += a // b

    log.show("Second form: " + str(ret2))

    return ret


def test(log):
    values = [
        "5 1 9 5",
        "7 5 3",
        "2 4 6 8",
    ]

    if calc(log, values) == 18:
        return True
    else:
        return False


def run(log, values):
    log.show(calc(log, values))
