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
    cur = None
    for cur in sys.argv[1:] + ["input.txt", "day_##_input.txt", "Puzzles/day_##_input.txt", "../Puzzles/day_##_input.txt"]:
        cur = os.path.join(*cur.split("/")).replace("##", f"{DAY_NUM:02d}")
        if os.path.isfile(cur): fn = cur; break
    if cur is None: print("Unable to find input file!"); exit(1)
    with open(fn) as f: values = f.readlines()
    print(f"Running day {DAY_DESC}:")
    run(print, values)
