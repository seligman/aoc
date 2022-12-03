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
    log(calc(log, values, 1))
    log(calc(log, values, 2))

if __name__ == "__main__":
    import sys, os
    cur = None
    for cur in sys.argv[1:] + ["input.txt", "day_##_input.txt", "Puzzles/day_##_input.txt", "../Puzzles/day_##_input.txt"]:
        cur = os.path.join(*cur.split("/")).replace("##", f"{DAY_NUM:02d}")
        if os.path.isfile(cur): fn = cur; break
    if cur is None: print("Unable to find input file!"); exit(1)
    with open(fn) as f: values = f.readlines()
    print(f"Running day {DAY_DESC}:")
    run(print, values)
