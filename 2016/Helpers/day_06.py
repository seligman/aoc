#!/usr/bin/env python3

from collections import defaultdict

DAY_NUM = 6
DAY_DESC = 'Day 6: Signals and Noise'


def calc(values, first_pass):
    ret = ""
    for i in range(len(values[0])):
        hist = defaultdict(int)
        for cur in values:
            hist[cur[i]] += 1
        letters = list(hist)
        letters.sort(key=lambda x: hist[x], reverse=first_pass)
        ret += letters[0]

    return ret


def test(log):
    values = [
        "eedadn",
        "drvtee",
        "eandsr",
        "raavrd",
        "atevrs",
        "tsrnev",
        "sdttsa",
        "rasrtv",
        "nssdts",
        "ntnada",
        "svetve",
        "tesnvt",
        "vntsnd",
        "vrdear",
        "dvrsen",
        "enarar",
    ]

    if calc(values, True) == "easter":
        return True
    else:
        return False


def run(log, values):
    log(calc(values, True))
    log(calc(values, False))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in [[], ["Puzzles"], ["..", "Puzzles"]]:
                cur = os.path.join(*(dn + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!"); exit(1)
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
