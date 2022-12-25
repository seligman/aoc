#!/usr/bin/env python3

import codecs

DAY_NUM = 8
DAY_DESC = 'Day 8: Matchsticks'


def calc(log, values):
    total_size = 0
    total_decoded = 0
    total_encoded = 0

    for cur in values:
        total_size += len(cur)
        total_decoded += len(codecs.escape_decode(cur[1:-1])[0])

        cur = cur.replace("\\", "\\\\")
        cur = cur.replace('"', '\\"')

        total_encoded += len(cur) + 2

    log("Increased: %d" % (total_encoded - total_size,))

    return total_size - total_decoded


def test(log):
    return True


def run(log, values):
    log(calc(log, values))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in [[], ["Puzzles"], ["..", "Puzzles"]]:
                cur = os.path.join(*(dn + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
