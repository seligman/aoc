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
