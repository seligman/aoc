#!/usr/bin/env python3

DAY_NUM = 25
DAY_DESC = 'Day 25: Let It Snow'


def calc(target_x, target_y):
    x, y = 1, 1
    value = 20151125

    while x != target_x or y != target_y:
        x += 1
        y -= 1
        if y == 0:
            x, y = 1, x
        value = (value * 252533) % 33554393

    return value


def test(log):
    if calc(4, 5) == 6899651:
        return True
    else:
        return False


def run(log, values):
    log(calc(3029, 2947))

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
