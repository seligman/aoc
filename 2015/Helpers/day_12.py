#!/usr/bin/env python3

import json

DAY_NUM = 12
DAY_DESC = 'Day 12: JSAbacusFramework.io'


def summarize(data, red_pass):
    ret = 0
    if isinstance(data, dict):
        skip = False
        if red_pass:
            if "red" in data.values():
                skip = True
            elif "red" in data:
                skip = True
        if not skip:
            for value in data.values():
                ret += summarize(value, red_pass)
    elif isinstance(data, list):
        for key in data:
            ret += summarize(key, red_pass)
    elif isinstance(data, int):
        ret += data
    return ret


def calc(values, red_pass):
    data = values[0]
    data = json.loads(data)

    return summarize(data, red_pass)


def test(log):
    values = [
        '{"a":[-1,1]}',
    ]

    if calc(values, False) == 0:
        return True
    else:
        return False


def run(log, values):
    log(calc(values, False))
    log(calc(values, True))

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
