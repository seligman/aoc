#!/usr/bin/env python3

import re

DAY_NUM = 5
DAY_DESC = 'Day 5: Doesn\'t He Have Intern-Elves For This?'


def calc(log, values):
    vowels = {"a", "e", "i", "o", "u"}
    bad = ["ab", "cd", "pq", "xy"]
    total_good = 0
    total_good_v2 = 0

    for cur in values:
        good = False
        vowel_count = 0
        for sub in cur:
            if sub in vowels:
                vowel_count += 1
                if vowel_count == 3:
                    good = True
                    break
        
        if good:
            for bad_word in bad:
                if bad_word in cur:
                    good = False
                    break

        if good:
            last = ""
            good = False
            for sub in cur:
                if last == sub:
                    good = True
                    break
                last = sub

        if good:
            total_good += 1

        if re.search("(..).*\\1", cur) and re.search("(.).\\1", cur):
            total_good_v2 += 1

    log("Ver 2: " + str(total_good_v2))

    return total_good


def test(log):
    values = [
        "ugknbfddgicrmopn",
        "aaa",
        "jchzalrnumimnmhp",
        "haegwjzuvuyypxyu",
        "dvszwmarrgswjxmb",
    ]

    if calc(log, values) == 2:
        return True
    else:
        return False


def run(log, values):
    log(calc(log, values))

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
