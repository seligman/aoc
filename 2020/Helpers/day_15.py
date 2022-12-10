#!/usr/bin/env python3

from collections import defaultdict, deque

DAY_NUM = 15
DAY_DESC = 'Day 15: Rambunctious Recitation'

def calc(log, values, mode):
    numbers = [int(x) for x in values[0].split(",")]

    said = {}
    last = None

    for i in range(len(numbers)):
        said[last], last = i, numbers[i]

    for i in range(len(numbers), 2020 if mode == 1 else 30000000):
        said[last], last = i, i - said.get(last, i)
        if (mode == 1 and i % 1000 == 19) or (mode == 2 and i % 5000000 == 999999):
            log.show(f"For round {i:8d}, {last:8d} was said")

    return last

def test(log):
    values = log.decode_values("""
        0,3,6
    """)

    log.test(calc(log, values, 1), 436)
    # log.test(calc(log, values, 2), 175594)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))
