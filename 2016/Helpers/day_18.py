#!/usr/bin/env python3

DAY_NUM = 18
DAY_DESC = 'Day 18: Like a Rogue'


def calc(values, rows):
    ret = 0
    row = [0 if x == "^" else 1 for x in values[0]]
    its_a_trap = {(0, 0, 1), (1, 0, 0), (0, 1, 1), (1, 1, 0)}

    while rows > 0:
        rows -= 1
        ret += sum(row)
        row = [1] + row + [1]
        row = [0 if tuple(row[x-1:x+2]) in its_a_trap else 1 for x in range(1, len(row) - 1)]

    return ret


def test(log):
    values = [
        ".^^.^.^^^^",
    ]

    if calc(values, 10) == 38:
        return True
    else:
        return False


def run(log, values):
    for rows in [40, 400000]:
        log("There are %d safe tiles in %d rows." % (calc(values, rows), rows))

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
