#!/usr/bin/env python3

from collections import defaultdict

def get_desc():
    return 10, 'Day 10: Adapter Array'

def calc(log, values, mode):
    values = [0] + sorted([int(x) for x in values])
    values.append(values[-1] + 3)

    if mode == 1:
        changes = defaultdict(int)
        for i in range(1, len(values)):
            changes[values[i] - values[i-1]] += 1
        return changes[1] * changes[3]
    else:
        ways = defaultdict(int, {0:1})
        for i in range(len(values)):
            for j in range(1, 4):
                if values[i] - values[i-j] <= 3:
                    ways[i] += ways[i-j]        
        return max(ways.values())

def test(log):
    values = log.decode_values("""
        28
        33
        18
        42
        31
        14
        46
        20
        48
        47
        24
        23
        49
        45
        19
        38
        39
        11
        1
        32
        25
        35
        8
        17
        7
        9
        4
        2
        34
        10
        3
    """)

    log.test(calc(log, values, 1), 220)
    log.test(calc(log, values, 2), 19208)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))
