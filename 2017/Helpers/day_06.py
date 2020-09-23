#!/usr/bin/env python

def get_desc():
    return 6, 'Day 6: Memory Reallocation'


def calc(log, values, redo):
    banks = [int(x) for x in values[0].replace("\t", " ").split(" ")]

    seen = set()
    while True:
        key = tuple(banks)
        if key in seen:
            if redo == 0:
                break
            else:
                seen = set()
                redo -= 1
        seen.add(key)
        i = banks.index(max(banks))
        val = banks[i]
        banks[i] = 0
        for x in range(val):
            banks[(i + 1 + x) % len(banks)] += 1

    return len(seen)


def test(log):
    values = [
        "0 2 7 0",
    ]

    if calc(log, values, 0) == 5:
        if calc(log, values, 1) == 4:
            return True
        else:
            return False
    else:
        return False


def run(log, values):
    log.show(calc(log, values, 0))
    log.show(calc(log, values, 1))
