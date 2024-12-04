#!/usr/bin/env python3

DAY_NUM = 5
DAY_DESC = 'Day 5: Alchemical Reduction'


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

    log("Best to remove %s: Down to %d" % (best_val, best))

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
    log(calc(log, values))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2018/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
