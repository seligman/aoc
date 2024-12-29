#!/usr/bin/env python3

DAY_NUM = 6
DAY_DESC = 'Day 6: Wait For It'

import math

def calc(log, values, mode):
    if mode == 1:
        times = [int(x) for x in values[0].split(":")[1].split(" ") if len(x)]
        distances = [int(x) for x in values[1].split(":")[1].split(" ") if len(x)]
    else:
        times = [int(values[0].split(":")[1].replace(" ", ""))]
        distances = [int(values[1].split(":")[1].replace(" ", ""))]

    ret = 1

    for time, distance in zip(times, distances):
        # Solving "i * (time - i) > distance" for i
        start = (1/2) * (time - math.sqrt((time * time) - (4 * distance)))
        end = (1/2) * (math.sqrt((time ** 2) - 4 * distance) + time)
        # Clamp possible "i" for real numbers
        start = (int(start) + 1) if (start == int(start)) else int(math.ceil(start))
        end = (int(end) - 1) if (end == int(end)) else int(math.floor(end))
        wins = max(end - start + 1, 0)
        ret *= wins

    return ret

def test(log):
    values = log.decode_values("""
        Time:      7  15   30
        Distance:  9  40  200
    """)

    log.test(calc(log, values, 1), '288')
    log.test(calc(log, values, 2), '71503')

def run(log, values):
    log(f"Part 1: {calc(log, values, 1)}")
    log(f"Part 2: {calc(log, values, 2)}")

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2023/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
