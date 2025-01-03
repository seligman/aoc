#!/usr/bin/env python3

DAY_NUM = 7
DAY_DESC = 'Day 7: The Treachery of Whales'

def calc(log, values, mode):
    values = [int(x) for x in values[0].split(",")]
    best = None
    cost = {}

    for target in range(min(values), max(values)+1):
        temp = 0
        for cur in values:
            if mode == 1:
                temp += abs(cur - target)
            else:
                x = abs(cur - target)
                if x not in cost:
                    cost[x] = sum(range(x + 1))
                temp += cost[x]
            if best is not None and temp > best:
                break
        if best is None:
            best = temp
        else:
            best = min(best, temp)
    
    return best

def test(log):
    values = log.decode_values("""
        16,1,2,0,4,2,7,1,2,14
    """)

    log.test(calc(log, values, 1), 37)
    log.test(calc(log, values, 2), 168)

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
