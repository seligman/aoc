#!/usr/bin/env python3

DAY_NUM = 3
DAY_DESC = 'Day 3: Rucksack Reorganization'

def calc(log, values, mode):
    total = 0
    if mode == 1:
        for cur in values:
            a, b = cur[:len(cur)//2], cur[len(cur)//2:]
            both = set(a) & set(b)
            both = list(both)[0]
            if 'a' <= both <= 'z':
                val = ord(both) - ord('a') + 1
            else:
                val = ord(both) - ord('A') + 27
            total += val
    else:
        sets = []
        for cur in values:
            sets.append(set(cur))
            if len(sets) == 3:
                common = sets[0] & sets[1] & sets[2]
                both = list(common)[0]
                sets = []
                if 'a' <= both <= 'z':
                    val = ord(both) - ord('a') + 1
                else:
                    val = ord(both) - ord('A') + 27
                total += val

    return total

def test(log):
    values = log.decode_values("""
        vJrwpWtwJgWrhcsFMMfFFhFp
        jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
        PmmdzqPrVvPwwTWBwg
        wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
        ttgJtRGJQctTZtZT
        CrZsJsPPZsGzwwsLwLmpwMDw
    """)

    log.test(calc(log, values, 1), 157)
    log.test(calc(log, values, 2), 70)

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
