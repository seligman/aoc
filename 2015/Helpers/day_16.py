#!/usr/bin/env python3

import re

DAY_NUM = 16
DAY_DESC = 'Day 16: Aunt Sue'


def calc(values, mode):
    target = {
        "children": 3,
        "cats": 7,
        "samoyeds": 2,
        "pomeranians": 3,
        "akitas": 0,
        "vizslas": 0,
        "goldfish": 5,
        "trees": 3,
        "cars": 2,
        "perfumes": 1,
    }

    sues = {}
    r = re.compile("Sue ([0-9]+): (.*)")

    for cur in values:
        m = r.search(cur)
        vals = {}
        for cur in m.group(2).split(", "):
            cur = cur.split(": ")
            vals[cur[0]] = int(cur[1])
        sues[int(m.group(1))] = vals

    for sue in sues:
        good = True
        for key in target:
            value = target[key]
            if key in sues[sue]:
                if mode == 0:
                    if value != sues[sue][key]:
                        good = False
                else:
                    if key in {'cats', 'trees'}:
                        if value >= sues[sue][key]:
                            good = False
                    elif key in {'pomeranians', 'goldfish'}:
                        if value <= sues[sue][key]:
                            good = False
                    else:
                        if value != sues[sue][key]:
                            good = False
        if good:
            return sue

    return -1


def test(log):
    return True


def run(log, values):
    log(calc(values, 0))
    log(calc(values, 1))

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
