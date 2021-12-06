#!/usr/bin/env python3

from collections import Counter, defaultdict

def get_desc():
    return 6, 'Day 6: Lanternfish'

def calc(log, values, mode):
    counts = Counter(int(x) for x in values[0].split(","))

    toshow = [
        65249347,       # AWS IPv4 addresses (as of 2021-12-05)
        3702258432,     # All public non-reserved IPv4 addresses
        340282366920938463463374607431768211456,    # All possible IPv6 addresses
        2.4 * 10**67,   # Atoms in the galaxy
        10 ** 78,       # Atoms in the universe
    ]

    days = {
        1: 80,
        2: 256,
        3: 10000,
    }
    for day in range(days[mode]):
        temp = defaultdict(int)
        for key, value in counts.items():
            if key == 0:
                temp[8] += value
                temp[6] += value
            else:
                temp[key - 1] += value
        counts = temp
        if mode == 3:
            if len(toshow) > 0:
                if sum(counts.values()) > toshow[0]:
                    log(f"Day #{day + 1}, {toshow[0]}")
                    toshow.pop(0)
                    if len(toshow) == 0:
                        break

    return sum(counts.values())

def other_howmuch(describe, values):
    if describe:
        return "Show how quickly things escape"
    from dummylog import DummyLog
    calc(DummyLog(), values, 3)

def test(log):
    values = log.decode_values("""
        3,4,3,1,2
    """)

    log.test(calc(log, values, 1), 5934)
    log.test(calc(log, values, 2), 26984457539)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))
