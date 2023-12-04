#!/usr/bin/env python3

DAY_NUM = 4
DAY_DESC = 'Day 4: Scratchcards'

def calc(log, values, mode):
    ret = 0
    mult = {}
    for i, cur in enumerate(values):
        if i not in mult:
            mult[i] = 1

        cur = cur[8:]
        cur = cur.split("|")
        good = [x for x in cur[0].split(" ") if len(x)]
        hits = [x for x in cur[1].split(" ") if len(x)]
        x = len(set(good) & set(hits))

        if mode == 1:
            if x > 0:
                ret += 2 ** (x - 1)
        else:
            for j in range(i + 1, min(len(values), i + x + 1)):
                mult[j] = mult.get(j, 1) + mult[i]
        
    if mode == 1:
        return ret
    else:
        return sum(mult.values())

def test(log):
    values = log.decode_values("""
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
    """)

    log.test(calc(log, values, 1), '13')
    log.test(calc(log, values, 2), '30')

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
