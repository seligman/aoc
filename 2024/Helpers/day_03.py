#!/usr/bin/env python3

DAY_NUM = 3
DAY_DESC = 'Day 3: Mull It Over'

import re

def calc(log, values, mode):
    ret = 0

    is_enabled = True
    instructions = {
        ("do", ""),
        ("don't", ""),
        ("mul", "(?P<mul1>[0-9]{1,3}),(?P<mul2>[0-9]{1,3})"),
    }
    r = "|".join(f"{re.escape(ins)}\\({args}\\)" for ins, args in instructions)
    r = re.compile("(?P<ins>" + r +")")

    for row in values:
        for m in r.finditer(row):
            ins = m.group("ins").split("(")[0]
            if ins == "do" and mode == 2:
                is_enabled = True
            elif ins == "don't" and mode == 2:
                is_enabled = False
            elif ins == "mul":
                if is_enabled:
                    ret += int(m.group("mul1")) * int(m.group("mul2"))
                
    return ret

def test(log):
    values = log.decode_values("xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))")
    log.test(calc(log, values, 1), '161')

    values = log.decode_values("xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))")
    log.test(calc(log, values, 2), '48')

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
