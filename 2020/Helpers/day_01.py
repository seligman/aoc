#!/usr/bin/env python3

DAY_NUM = 1
DAY_DESC = 'Day 1: Report Repair'

def calc(log, values, mode):
    values = [int(x) for x in values]

    if mode == 1:
        for x in range(len(values)):
            for y in range(x + 1, len(values)):
                if values[x] + values[y] == 2020:
                    return values[x] * values[y]
    else:
        for x in range(len(values)):
            for y in range(x + 1, len(values)):
                for z in range(y + 1, len(values)):
                    if values[x] + values[y] + values[z] == 2020:
                        return values[x] * values[y] * values[z]

    return 10

def test(log):
    values = log.decode_values("""
        1721
        979
        366
        299
        675
        1456
    """)

    log.test(calc(log, values, 1), 514579)
    log.test(calc(log, values, 2), 241861950)

def run(log, values):
    log(f"Part 1: {calc(log, values, 1)}")
    log(f"Part 2: {calc(log, values, 2)}")

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2020/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
