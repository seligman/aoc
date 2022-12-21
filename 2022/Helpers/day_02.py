#!/usr/bin/env python3

DAY_NUM = 2
DAY_DESC = 'Day 2: Rock Paper Scissors'

def calc(log, values, mode):
    score = 0

    for a, _, b in values:
        a = {"A": "R", "B": "P", "C": "S"}[a]
        if mode == 1:
            b = {"X": "R", "Y": "P", "Z": "S"}[b]
        else:
            if b == "Y":
                b = a
            elif b == "X":
                # Force a win
                b = {"R": "S", "S": "P", "P": "R"}[a]
            else:
                # Force a loss
                b = {"R": "P", "P": "S", "S": "R"}[a]

        if a == b:
            score += 3
        elif (b == "R" and a == "S") or (b == "S" and a == "P") or (b == "P" and a == "R"):
            score += 6

        score += {"R": 1, "P": 2, "S": 3}[b]

    return score

def test(log):
    values = log.decode_values("""
        A Y
        B X
        C Z
    """)

    log.test(calc(log, values, 1), 15)
    log.test(calc(log, values, 2), 12)

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
