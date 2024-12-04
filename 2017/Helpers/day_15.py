#!/usr/bin/env python3

DAY_NUM = 15
DAY_DESC = 'Day 15: Dueling Generators'


def calc(log, values):
    a = int(values[0][24:])
    b = int(values[1][24:])

    ret = 0
    rounds = 40000000
    while rounds > 0:
        rounds -= 1
        a = (a * 16807) % 2147483647
        b = (b * 48271) % 2147483647
        if (a & 65535) == (b & 65535):
            ret += 1

    return ret


def calc2(log, values):
    a = int(values[0][24:])
    b = int(values[1][24:])

    ret = 0
    rounds = 5000000
    while rounds > 0:
        rounds -= 1
        while True:
            a = (a * 16807) % 2147483647
            if a % 4 == 0:
                break
        while True:
            b = (b * 48271) % 2147483647
            if b % 8 == 0:
                break
        if (a & 65535) == (b & 65535):
            ret += 1

    return ret


def test(log):
    values = [
        "Generator A starts with 65",
        "Generator B starts with 8921",
    ]

    if calc(log, values) == 588:
        log("Pass 1 worked")
        if calc2(log, values) == 309:
            log("Pass 2 worked")
            return True
        else:
            return False
    else:
        return False


def run(log, values):
    log(calc(log, values))
    log(calc2(log, values))

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
