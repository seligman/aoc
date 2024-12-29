#!/usr/bin/env python3

DAY_NUM = 2
DAY_DESC = 'Day 2: Red-Nosed Reports'

def is_valid(row):
    good_pos, good_neg, bad = 0, 0, 0

    for i in range(1, len(row)):
        diff = row[i] - row[i-1]
        if good_neg == 0 and diff in {1, 2, 3}:
            good_pos += 1
        elif good_pos == 0 and diff in {-1, -2, -3}:
            good_neg += 1
        else:
            bad += 1
            break
    
    return bad == 0

def calc(log, values, mode):
    values = [list(map(int, x.split())) for x in values]
    ret = 0

    for row in values:
        if is_valid(row):
            ret += 1
        elif mode == 2:
            ret += 1 if any(is_valid(row[:i] + row[i+1:]) for i in range(len(row))) else 0

    return ret

def test(log):
    values = log.decode_values("""
        7 6 4 2 1
        1 2 7 8 9
        9 7 6 2 1
        1 3 2 4 5
        8 6 4 4 1
        1 3 6 7 9
    """)

    log.test(calc(log, values, 1), '2')
    log.test(calc(log, values, 2), '4')

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
