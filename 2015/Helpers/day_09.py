#!/usr/bin/env python3

import re
import itertools

DAY_NUM = 9
DAY_DESC = 'Day 9: All in a Single Night'

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

    log("Part 2: %d" % (worst_val,))    
    
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
    log("Part 1: %d" % (calc(log, values),))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2015/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
