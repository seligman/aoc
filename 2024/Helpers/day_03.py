#!/usr/bin/env python3

DAY_NUM = 3
DAY_DESC = 'Day 3: Mull It Over'

import re

def calc(log, values, mode):
    ret = 0
    is_enabled = True

    for row in values:
        for m in re.finditer("(?P<ins>do\\(\\)|don't\\(\\)|mul\\((?P<v1>[0-9]{1,3}),(?P<v2>[0-9]{1,3})\\))", row):
            if m.group("ins").startswith("mul("):
                if is_enabled:
                    ret += int(m.group('v1')) * int(m.group('v2'))
            elif m.group("ins").startswith("don't(") and mode == 2:
                is_enabled = False
            elif m.group("ins").startswith("do(") and mode == 2:
                is_enabled = True
                
    return ret

def test(log):
    values = log.decode_values("""
        xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
    """)

    log.test(calc(log, values, 1), '161')

    values = log.decode_values("""
        xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
    """)

    log.test(calc(log, values, 2), '48')

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))

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
