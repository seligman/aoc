#!/usr/bin/env python3

DAY_NUM = 2
DAY_DESC = 'Day 2: I Was Told There Would Be No Math'

def calc(log, values):
    ret = 0
    ribbon = 0
    for cur in values:
        cur = [int(x) for x in cur.split("x")]
        a, b, c = cur[0] * cur[1] * 2, cur[1] * cur[2] * 2, cur[0] * cur[2] * 2
        ret += sum((a, b, c)) + min((a, b, c)) // 2
        ribbon += sum(sorted(cur)[0:2])*2 + cur[0] * cur[1] * cur[2]

    log("Part 2: %d" % (ribbon,))

    return ret

def test(log):
    values = [
        "2x3x4",
    ]

    if calc(log, values) == 58:
        return True
    else:
        return False

def run(log, values):
    log("Part 1: %d" % (calc(log, values),))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2015/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
