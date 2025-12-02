#!/usr/bin/env python3

DAY_NUM = 1
DAY_DESC = 'Day 1: Secret Entrance'

def calc(log, values, mode):
    pos = 50
    ret = 0
    for row in values:
        if mode == 2:
            for _ in range(int(row[1:])):
                pos = (pos + (1 if row[0] == "L" else -1)) % 100
                if pos == 0:
                    ret += 1
        else:
            pos = (pos + int(row[1:]) * (1 if row[0] == "L" else -1)) % 100
            if pos == 0:
                ret += 1
    return ret

def test(log):
    values = log.decode_values("""
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82

    """)

    log.test(calc(log, values, 1), '3')
    log.test(calc(log, values, 2), '6')

def run(log, values):
    log("Part 1")
    log(calc(log, values, 1))
    log("Part 2")
    log(calc(log, values, 2))

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
