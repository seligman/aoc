#!/usr/bin/env python

from collections import deque

def get_desc():
    return 10, 'Day 10: Elves Look, Elves Say'


def calc(values, loops):
    look = deque(values[0])

    while loops > 0:
        loops -= 1
        last = None
        count = 0
        say = deque()
        for cur in look:
            if last is not None:
                if last != cur:
                    say.extend("%d%s" % (count, last))
                    count = 0
            last = cur
            count += 1
        say.extend("%d%s" % (count, last))
        look = say

    return len(look)


def test(log):
    values = [
        "1",
    ]

    if calc(values, 5) == len("312211"):
        return True
    else:
        return False


def run(log, values):
    log.show(calc(values, 40))
    log.show(calc(values, 50))
