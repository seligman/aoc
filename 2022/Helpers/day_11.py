#!/usr/bin/env python3

import math
import re

DAY_NUM = 11
DAY_DESC = 'Day 11: Monkey in the Middle'

def build_helper(func_input):
    m = re.search("old \\* ([0-9]+)", func_input)
    if m is not None:
        a = int(m.group(1))
        def helper(x):
            return x * a
        return helper

    m = re.search("old \\+ ([0-9]+)", func_input)
    if m is not None:
        a = int(m.group(1))
        def helper(x):
            return x + a
        return helper

    m = re.search("old \\* old", func_input)
    if m is not None:
        def helper(x):
            return x * x
        return helper

    print("Need to handle: " + func_input)
    exit(1)

def calc(log, values, mode):
    monkey = []

    for row in values:
        m = re.search("Monkey (?P<val>[0-9]+):", row)
        if m is not None:
            monkey.append({"inspected": 0})
        m = re.search("Starting items: (?P<val>.+)", row)
        if m is not None:
            monkey[-1]['start'] = list(map(int, m['val'].split(", ")))
        m = re.search("Operation: (?P<val>.+)", row)
        if m is not None:
            monkey[-1]['op'] = build_helper(m['val'])
        m = re.search("Test: divisible by (?P<val>[0-9]+)", row)
        if m is not None:
            monkey[-1]['test'] = int(m['val'])
        m = re.search("If true: throw to monkey (?P<val>[0-9]+)", row)
        if m is not None:
            monkey[-1]['true'] = int(m['val'])
        m = re.search("If false: throw to monkey (?P<val>[0-9]+)", row)
        if m is not None:
            monkey[-1]['false'] = int(m['val'])

    limit = [x['test'] for x in monkey]
    limit.append(3)
    limit.append(4)
    limit = math.prod(limit)

    for _ in range(20 if mode == 1 else 10000):
        for cur in monkey:
            temp = cur['start']
            cur['start'] = []
            for x in temp:
                cur['inspected'] += 1
                x = (cur['op'](x) // (3 if mode == 1 else 1)) % limit
                if x % cur['test'] == 0:
                    monkey[cur['true']]['start'].append(x)
                else:
                    monkey[cur['false']]['start'].append(x)

    return math.prod(sorted([x['inspected'] for x in monkey])[-2:])

def test(log):
    values = log.decode_values("""
        Monkey 0:
        Starting items: 79, 98
        Operation: new = old * 19
        Test: divisible by 23
            If true: throw to monkey 2
            If false: throw to monkey 3

        Monkey 1:
        Starting items: 54, 65, 75, 74
        Operation: new = old + 6
        Test: divisible by 19
            If true: throw to monkey 2
            If false: throw to monkey 0

        Monkey 2:
        Starting items: 79, 60, 97
        Operation: new = old * old
        Test: divisible by 13
            If true: throw to monkey 1
            If false: throw to monkey 3

        Monkey 3:
        Starting items: 74
        Operation: new = old + 3
        Test: divisible by 17
            If true: throw to monkey 0
            If false: throw to monkey 1
    """)

    log.test(calc(log, values, 1), 10605)
    log.test(calc(log, values, 2), 2713310158)

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
