#!/usr/bin/env python3

DAY_NUM = 11
DAY_DESC = 'Day 11: Chronal Charge'

def calc(log, values):
    powers = {}
    for x in range(1, 301):
        for y in range(1, 301):
            rack_id = x + 10
            power = (rack_id * y + values) * rack_id
            power = ((power // 100) % 10) - 5
            powers[(x,y)] = power

    # cs[(x, y)] is the cumulative sum of d[(i, j)] for all i <= x and j <= y
    cumulative = {}
    for x in range(1, 301):
        for y in range(1, 301):
            cumulative[(x, y)] = powers[(x, y)] + cumulative.get((x - 1, y), 0) + cumulative.get((x, y - 1), 0) - cumulative.get((x - 1, y - 1), 0)

    best = None
    best_at = None
    for x in range(1, 301 - 3):
        for y in range(1, 301 - 3):
            size = 3
            power = cumulative[(x + size, y + size)] + cumulative[(x, y)] - cumulative[(x + size, y)] - cumulative[(x, y + size)]
            # k = d[(i, j)]
            if best is None or power > best:
                best = power
                best_at = "Part 1: %d,%d" % (x + 1, y + 1)
    log(best_at)

    best = None
    best_at = None
    for x in range(1, 301):
        for y in range(1, 301):
            for size in range(1, 301 - max(x, y)):
            # I figured out after submitting that these indices should all be one
            # smaller since the bounds of the square are
            # i <= x < i + s, j <= y < j + s
                power = cumulative[(x + size, y + size)] + cumulative[(x, y)] - cumulative[(x + size, y)] - cumulative[(x, y + size)]
                if best is None or power > best:
                    best = power
                    best_at = "Part 2: %d,%d,%d" % (x + 1, y + 1, size)

    log(best_at)

    return ""

def test(log):
    if calc(log, 18) == 29:
        return True
    else:
        return False

def run(log, values):
    calc(log, int(values[0]))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2018/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
