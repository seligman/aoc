#!/usr/bin/env python3

def get_desc():
    return 5, 'Day 5: Alchemical Reduction'


def decode(polymer):
    found = True
    i = 0
    while found:
        found = False
        while i < len(polymer) - 1:
            a, b = list(polymer[i:i+2])
            if a != b and a.lower() == b.lower():
                polymer = polymer[0:i] + polymer[i+2:]
                found = True
                if i > 0:
                    i -= 1
                break
            i += 1

    return len(polymer)


def calc(log, values):
    polymer = values[0]
    values = set()
    for cur in polymer:
        values.add(cur.lower())

    best = None
    best_val = None
    for cur in values:
        test = decode(polymer.replace(cur, "").replace(cur.upper(), ""))
        if best is None or test < best:
            best = test
            best_val = cur

    log.show("Best to remove %s: Down to %d" % (best_val, best))

    return decode(polymer)


def test(log):
    values = [
        "dabAcCaCBAcCcaDA",
    ]

    if calc(log, values) == 10:
        return True
    else:
        return False


def run(log, values):
    log.show(calc(log, values))
