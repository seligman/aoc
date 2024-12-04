#!/usr/bin/env python3

DAY_NUM = 3
DAY_DESC = 'Day 3: Spiral Memory'


def calc(log, values):
    value = int(values[0])
    cur = 1
    x, y = 0, 0
    change = 1

    wrote = {(0,0): 1}

    while True:
        for dx, dy, inc in ((1, 0, 0), (0, -1, 1), (-1, 0, 0), (0, 1, 1)):
            for _ in range(change):
                x += dx
                y += dy
                cur += 1

                if wrote is not None:
                    write = 0
                    for ox, oy in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)):
                        ox += x
                        oy += y
                        write += wrote.get((ox, oy), 0)
                    if write > value:
                        log("First greater: " + str(write))
                        wrote = None
                    if wrote is not None:
                        wrote[(x, y)] = write

                if cur == value:
                    return abs(x) + abs(y)
            change += inc


def test(log):
    values = [
        "1024",
    ]

    if calc(log, values) == 31:
        return True
    else:
        return False


def run(log, values):
    log(calc(log, values))

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
