#!/usr/bin/env python

from collections import deque

def get_desc():
    return 17, 'Day 17: Spinlock'


def calc(log, values, mode):
    value = int(values[0])

    spin = deque()
    spin.append(0)
    i = 0

    rounds = 2017 if mode == 0 else 50000000
    while rounds > 0:
        rounds -= 1
        spin.rotate(-value)
        i += 1
        spin.append(i)

    if mode == 0:
        return spin.popleft()
    else:
        while spin.popleft() != 0:
            pass
        return spin.popleft()


def test(log):
    values = [
        "3",
    ]

    if calc(log, values, 0) == 638:
        return True
    else:
        return False


def run(log, values):
    log.show(calc(log, values, 0))
    log.show(calc(log, values, 1))
