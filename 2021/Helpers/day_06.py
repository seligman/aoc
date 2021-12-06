#!/usr/bin/env python3

from collections import defaultdict

def get_desc():
    return 6, 'Day 6: Lanternfish'

def calc(log, values, mode):
    values = [int(x) for x in values[0].split(",")]
    counts = defaultdict(int)
    for x in values:
        counts[x] += 1

    for _ in range(80 if mode == 1 else 256):
        temp = defaultdict(int)
        for key, value in counts.items():
            if key == 0:
                temp[8] += value
                temp[6] += value
            else:
                temp[key - 1] += value
        counts = temp

    return sum(counts.values())

def test(log):
    values = log.decode_values("""
        3,4,3,1,2
    """)

    log.test(calc(log, values, 1), 5934)
    log.test(calc(log, values, 2), 26984457539)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))
