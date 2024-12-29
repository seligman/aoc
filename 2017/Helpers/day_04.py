#!/usr/bin/env python3

DAY_NUM = 4
DAY_DESC = 'Day 4: High-Entropy Passphrases'

def calc(log, values):
    ret = 0
    ret2 = 0
    for cur in values:
        cur = cur.split(' ')
        if len(set(cur)) == len(cur):
            ret += 1
        cur = ["".join(sorted(x)) for x in cur]
        if len(set(cur)) == len(cur):
            ret2 += 1

    log("Part 2: " + str(ret2))

    return ret

def test(log):
    return True

def run(log, values):
    log("Part 1: %d" % (calc(log, values),))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2017/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
