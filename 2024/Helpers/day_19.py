#!/usr/bin/env python3

DAY_NUM = 19
DAY_DESC = 'Day 19: Linen Layout'

import functools

_patterns = None
@functools.cache
def count_hits(row):
    if len(row) == 0:
        ret = 1
    else:
        ret = 0
        for cur in _patterns:
            if row.startswith(cur):
                ret += count_hits(row[len(cur):])
    return ret

def calc(log, values, mode):
    global _patterns
    _patterns = values[0].split(", ")
    ret = 0
    for row in values[2:]:
        temp = count_hits(row)
        if mode == 1 and temp > 0:
            temp = 1
        ret += temp

    return ret

def test(log):
    values = log.decode_values("""
        r, wr, b, g, bwu, rb, gb, br

        brwrr
        bggr
        gbbr
        rrbgbr
        ubwu
        bwurrg
        brgr
        bbrgwb
    """)

    log.test(calc(log, values, 1), '6')
    log.test(calc(log, values, 2), '16')

def run(log, values):
    log(f"Part 1: {calc(log, values, 1)}")
    log(f"Part 2: {calc(log, values, 2)}")

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2024/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
