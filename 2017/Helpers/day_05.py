#!/usr/bin/env python3

DAY_NUM = 5
DAY_DESC = 'Day 5: A Maze of Twisty Trampolines, All Alike'

def calc(log, values, mode):
    ip = 0
    steps = 0
    values = [int(x) for x in values]

    if mode == 0:
        while ip < len(values):
            next_ip = values[ip] + ip
            values[ip] += 1
            ip = next_ip
            steps += 1
    else:
        while ip < len(values):
            next_ip = values[ip] + ip
            if values[ip] >= 3:
                values[ip] -= 1
            else:
                values[ip] += 1
            ip = next_ip
            steps += 1

    return steps

def test(log):
    values = [
        "0",
        "3",
        "0",
        "1",
        "-3",
    ]

    if calc(log, values, 0) == 5:
        if calc(log, values, 1) == 10:
            return True
        else:
            return False
    else:
        return False

def run(log, values):
    log("Part 1: %d" % (calc(log, values, 0),))
    log("Part 2: %d" % (calc(log, values, 1),))

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
