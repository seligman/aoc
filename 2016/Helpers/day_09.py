#!/usr/bin/env python3

DAY_NUM = 9
DAY_DESC = 'Day 9: Explosives in Cyberspace'

def calc(value, ver):
    ret = 0
    in_paren = None

    buffer = ""
    buffer_left = 0
    buffer_rep = 0

    for cur in value:
        if in_paren is None:
            if buffer_left > 0:
                buffer += cur
                buffer_left -= 1
                if buffer_left == 0:
                    if ver == 1:
                        ret += len(buffer) * buffer_rep
                    else:
                        ret += calc(buffer, 2) * buffer_rep
            elif cur == "(":
                in_paren = ""
            else:
                ret += 1
        else:
            if cur == ")":
                buffer_left, buffer_rep = [int(x) for x in in_paren.split("x")]
                buffer = ""
                in_paren = None
            else:
                in_paren += cur

    return ret

def test(log):
    values = [
        "X(8x2)(3x3)ABCY",
    ]

    if calc(values[0], 1) == 18:
        return True
    else:
        return False

def run(log, values):
    log("Part 1: %d" % (calc(values[0], 1),))
    log("Part 2: %d" % (calc(values[0], 2),))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2016/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
