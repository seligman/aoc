#!/usr/bin/env python3

DAY_NUM = 13
DAY_DESC = 'Day 13: Distress Signal'

from functools import cmp_to_key
from itertools import zip_longest
import json

def calc(log, values, mode):
    if mode == 2:
        values.append("[[2]]")
        values.append("[[6]]")

    def compare(a, b):
        if isinstance(a, str): a = json.loads(a)
        if isinstance(b, str): b = json.loads(b)
        for aa, bb in zip_longest(a, b):
            if aa is None:
                return 1
            elif bb is None:
                return -1
            elif isinstance(aa, int) and isinstance(bb, int):
                if aa > bb:
                    return -1
                elif aa < bb:
                    return 1
            else:
                if isinstance(aa, int):
                    aa = [aa]
                if isinstance(bb, int):
                    bb = [bb]
                
                test = compare(aa, bb)
                if test != 0:
                    return test
        return 0

    values = [x for x in values if len(x)]

    if mode == 2:
        values.sort(key=cmp_to_key(compare), reverse=True)
        ret = 1
        for i, x in enumerate(values):
            if x in {"[[2]]", "[[6]]"}:
                ret *= i + 1
        return ret

    ret = 0
    for i in range(0, len(values), 2):
        if compare(values[i], values[i+1]) == 1:
            ret += i // 2 + 1

    return ret

def test(log):
    values = log.decode_values("""
        [1,1,3,1,1]
        [1,1,5,1,1]

        [[1],[2,3,4]]
        [[1],4]

        [9]
        [[8,7,6]]

        [[4,4],4,4]
        [[4,4],4,4,4]

        [7,7,7,7]
        [7,7,7]

        []
        [3]

        [[[]]]
        [[]]

        [1,[2,[3,[4,[5,6,7]]]],8,9]
        [1,[2,[3,[4,[5,6,0]]]],8,9]
    """)

    log.test(calc(log, values, 1), 13)
    log.test(calc(log, values, 2), 140)

def run(log, values):
    log(f"Part 1: {calc(log, values, 1)}")
    log(f"Part 2: {calc(log, values, 2)}")

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2022/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
