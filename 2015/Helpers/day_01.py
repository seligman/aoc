#!/usr/bin/env python3

DAY_NUM = 1
DAY_DESC = 'Day 1: Not Quite Lisp'


def calc(log, values):
    ret = 0
    pos = 0
    shown = False
    for cur in values:
        for sub in cur:
            if sub == "(":
                ret += 1
                pos += 1
            elif sub == ")":
                ret -= 1
                pos += 1
            if not shown:
                if ret < 0:
                    log("Entered basement on %d" % (pos,))
                    shown = True

    return ret


def test(log):
    values = [
        ")())())",
    ]

    if calc(log, values) == -3:
        return True
    else:
        return False


def run(log, values):
    log(calc(log, values))

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
