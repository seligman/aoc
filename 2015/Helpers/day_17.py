#!/usr/bin/env python3

import itertools
from collections import defaultdict

def get_desc():
    return 17, 'Day 17: No Such Thing as Too Much'


def calc(log, values, target):
    values = [int(x) for x in values]
    ret = 0
    used = defaultdict(int)
    for i in range(1, len(values)+1):
        for test in itertools.combinations(values, i):
            if sum(test) == target:
                ret += 1
                used[len(test)] += 1

    min_size = min(used)
    log.show("%d options with %d buckets" % (used[min_size], min_size))

    return ret


def test(log):
    values = [
        "20", 
        "15", 
        "10", 
        "5", 
        "5", 
    ]

    if calc(log, values, 25) == 4:
        return True
    else:
        return False


def run(log, values):
    log.show(calc(log, values, 150))
