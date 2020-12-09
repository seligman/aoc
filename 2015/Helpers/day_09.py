#!/usr/bin/env python3

import re
import itertools

def get_desc():
    return 9, 'Day 9: All in a Single Night'


def calc(log, values):
    r = re.compile("(.*) to (.*) = ([0-9]+)")

    cities = set()
    dists = {}

    for cur in values:
        m = r.search(cur)
        a, b, dist = m.groups()
        dist = int(dist)
        cities.add(a)
        cities.add(b)
        dists[(a, b)] = dist
        dists[(b, a)] = dist

    best_val = None
    worst_val = None

    for path in itertools.permutations(cities):
        last = None
        value = 0
        for cur in path:
            if last is not None:
                value += dists[(last, cur)]
            last = cur
        if best_val is None or value < best_val:
            best_val = value
        if worst_val is None or value > worst_val:
            worst_val = value

    log.show("Worst route: %d" % (worst_val,))    
    
    return best_val


def test(log):
    values = [
        "London to Dublin = 464",
        "London to Belfast = 518",
        "Dublin to Belfast = 141",
    ]

    if calc(log, values) == 605:
        return True
    else:
        return False


def run(log, values):
    log.show(calc(log, values))
