#!/usr/bin/env python3

DAY_NUM = 6
DAY_DESC = 'Day 6: Memory Reallocation'


def calc(log, values, redo):
    banks = [int(x) for x in values[0].replace("\t", " ").split(" ")]

    seen = set()
    while True:
        key = tuple(banks)
        if key in seen:
            if redo == 0:
                break
            else:
                seen = set()
                redo -= 1
        seen.add(key)
        i = banks.index(max(banks))
        val = banks[i]
        banks[i] = 0
        for x in range(val):
            banks[(i + 1 + x) % len(banks)] += 1

    return len(seen)


def test(log):
    values = [
        "0 2 7 0",
    ]

    if calc(log, values, 0) == 5:
        if calc(log, values, 1) == 4:
            return True
        else:
            return False
    else:
        return False


def run(log, values):
    log(calc(log, values, 0))
    log(calc(log, values, 1))

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
