#!/usr/bin/env python3

import re

DAY_NUM = 11
DAY_DESC = 'Day 11: Corporate Policy'


def is_valid(r, value):
    if "i" in value or "o" in value or "l" in value:
        return False
    if r.search(value) is None:
        return False
    expected = "-"
    run = 1
    for cur in value:
        if cur == expected:
            run += 1
            if run == 3:
                return True
        else:
            run = 1
        expected = chr(ord(cur) + 1)
    return False


def calc(values):
    r = re.compile("(.)\\1.*?(.)\\2")
    value = list(values[0])

    while True:
        dig = len(value) - 1
        while True:
            if value[dig] == "z":
                value[dig] = "a"
                dig -= 1
            else:
                value[dig] = chr(ord(value[dig]) + 1)
                break
        if is_valid(r, "".join(value)):
            return "".join(value)


def test(log):
    values = [
        "ghijklmn",
    ]

    if calc(values) == 'ghjaabcc':
        return True
    else:
        return False


def run(log, values):
    ret = calc(values)
    log(ret)
    ret = calc([ret])
    log(ret)

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
