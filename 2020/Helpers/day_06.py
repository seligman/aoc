#!/usr/bin/env python3

from collections import defaultdict

DAY_NUM = 6
DAY_DESC = 'Day 6: Custom Customs'

def calc(log, values, mode):
    total_answers = 0
    this_group = defaultdict(int)
    for value in values + [""]:
        if len(value) == 0:
            if len(this_group) > 0:
                if mode == 1:
                    total_answers += len(this_group) - 1
                else:
                    total_answers += len([x for x in this_group if this_group[x] == this_group['people']]) - 1
                this_group = defaultdict(int)
        else:
            for answer in value:
                this_group[answer] += 1
            this_group['people'] += 1

    return total_answers

def test(log):
    values = log.decode_values("""
        abc

        a
        b
        c

        ab
        ac

        a
        a
        a
        a

        b
    """)

    log.test(calc(log, values, 1), 11)
    log.test(calc(log, values, 2), 6)

def run(log, values):
    log(f"Part 1: {calc(log, values, 1)}")
    log(f"Part 2: {calc(log, values, 2)}")

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2020/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
