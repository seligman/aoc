#!/usr/bin/env python3

from collections import defaultdict

DAY_NUM = 14
DAY_DESC = 'Day 14: Extended Polymerization'

def calc(log, values, mode):
    polymer = values[0]
    template = {}
    for cur in values[2:]:
        cur = cur.split(" -> ")
        template[cur[0]] = cur[1]
    
    counts = defaultdict(int)
    for i in range(len(polymer) - 1):
        counts[polymer[i: i + 2]] += 1

    for _ in range(10 if mode == 1 else 40):
        next_counts = defaultdict(int)
        for key, value in counts.items():
            next_counts[key[0] + template[key]] += value
            next_counts[template[key] + key[1]] += value
        counts = next_counts

    single = defaultdict(int)
    for key, value in counts.items():
        single[key[0]] += value
    single[polymer[-1]] += 1

    singles = sorted(y for x, y in single.items())
    return singles[-1] - singles[0]

def test(log):
    values = log.decode_values("""
        NNCB

        CH -> B
        HH -> N
        CB -> H
        NH -> C
        HB -> C
        HC -> B
        HN -> C
        NN -> C
        BH -> H
        NC -> B
        NB -> B
        BN -> B
        BB -> N
        BC -> B
        CC -> N
        CN -> C
    """)

    log.test(calc(log, values, 1), 1588)
    log.test(calc(log, values, 2), 2188189693529)

def run(log, values):
    log(f"Part 1: {calc(log, values, 1)}")
    log(f"Part 2: {calc(log, values, 2)}")

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2021/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
