#!/usr/bin/env python3

import re
from collections import defaultdict

DAY_NUM = 4
DAY_DESC = 'Day 4: Security Through Obscurity'

def calc(log, values):
    r = re.compile("([a-z-]+)-([0-9]+)\\[([a-z]+)\\]")
    ret = 0

    for cur in values:
        m = r.search(cur).groups()
        counts = defaultdict(int)
        for sub in m[0]:
            if sub != '-':
                counts[sub] += 1
        letters = list(counts)
        letters.sort(key=lambda x:(-counts[x], x))
        letters = "".join(letters[0:5])

        if letters == m[2]:
            temp = ""
            for sub in m[0]:
                if sub == "-":
                    temp += " "
                else:
                    temp += chr((((ord(sub) - ord('a')) + int(m[1])) % 26) + ord('a'))
            if "north" in temp and "pole" in temp:
                log("Part 2: %s" % (m[1],))
            ret += int(m[1])

    return ret

def test(log):
    values = [
        "aaaaa-bbb-z-y-x-123[abxyz]",
        "a-b-c-d-e-f-g-h-987[abcde]",
        "not-a-real-room-404[oarel]",
        "totally-real-room-200[decoy]",
    ]

    if calc(log, values) == 1514:
        return True
    else:
        return False

def run(log, values):
    log("Part 1: %d" % (calc(log, values),))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2016/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
