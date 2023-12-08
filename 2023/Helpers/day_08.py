#!/usr/bin/env python3

DAY_NUM = 8
DAY_DESC = 'Day 8: Haunted Wasteland'

def calc(log, values, mode):
    import re
    dirs = values[0]
    map = {}
    for row in values[2:]:
        m = re.search("([A-Z0-9]+) = \\(([A-Z0-9]+), ([A-Z0-9]+)\\)", row)
        name, l, r = m.group(1), m.group(2), m.group(3)
        map[name] = (l, r)
    
    if mode == 1:
        pos = ["AAA"]
    else:
        pos = [x for x in map if x.endswith("A")]

    ret = []
    for pos in pos:
        steps = 0
        while True:
            pos = map[pos][0 if dirs[steps % len(dirs)] == "L" else 1]

            if mode == 1:
                if pos == "ZZZ":
                    break
            else:
                if pos.endswith("Z"):
                    break
            steps += 1
        ret.append(steps + 1)


    if mode == 1:
        return ret[0]
    else:
        import math
        return math.lcm(*ret)

def test(log):
    values = log.decode_values("""
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
    """)

    log.test(calc(log, values, 1), '6')

    values = log.decode_values("""
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
    """)

    log.test(calc(log, values, 2), '6')

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
