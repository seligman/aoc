#!/usr/bin/env python

import re
from collections import defaultdict

def get_desc():
    return 2, 'Day 2: Password Philosophy'

def calc(log, values, mode):
    r = re.compile("([0-9]+)-([0-9]+) ([a-z]): ([a-z]+)")
    ret = 0
    for cur in values:
        m = r.search(cur)
        a, b = int(m.group(1)), int(m.group(2))
        target = m.group(3)
        pw = m.group(4)

        if mode == 1:
            counts = defaultdict(int)
            for x in pw:
                counts[x] += 1
            if counts[target] >= a and counts[target] <= b:
                ret += 1
        else:
            if (pw[a-1] == target and pw[b-1] != target) or (pw[a-1] != target and pw[b-1] == target):
                ret += 1

    return ret

def test(log):
    values = log.decode_values("""
        1-3 a: abcde
        1-3 b: cdefg
        2-9 c: ccccccccc
    """)

    log.test(calc(log, values, 1), 2)
    log.test(calc(log, values, 2), 1)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))
