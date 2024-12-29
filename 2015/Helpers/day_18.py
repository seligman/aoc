#!/usr/bin/env python3

DAY_NUM = 18
DAY_DESC = 'Day 18: Like a GIF For Your Yard'

def calc(log, values, steps, mode):
    values = ["." * len(values[0])] + values + ["." * len(values[0])]
    values = [list("." + x + ".") for x in values]

    temp = [[x for x in y] for y in values]

    if mode == 1:
        for x in range(2):
            for y in range(2):
                values[y * (len(values) - 3) + 1][x * (len(values[0]) - 3) + 1] = "#"

    states = {"#": 1, ".": 0}
    wrap = []
    for x in range(-1, 2):
        for y in range(-1, 2):
            if x != 0 or y != 0:
                wrap.append((x, y))

    for _ in range(steps):
        for x in range(1, len(values[0])-1):
            for y in range(1, len(values)-1):
                on = 0
                for off in wrap:
                    on += states[values[y+off[1]][x+off[0]]]
                if values[y][x] == "#":
                    temp[y][x] = "#" if 2 <= on <= 3 else "."
                else:
                    temp[y][x] = "#" if on == 3 else "."

        values, temp = temp, values
        if mode == 1:
            for x in range(2):
                for y in range(2):
                    values[y * (len(values) - 3) + 1][x * (len(values[0]) - 3) + 1] = "#"

        if False:
            log("")
            log("\n".join(["".join(x) for x in values]))

    return sum([sum([states[x] for x in y]) for y in values])

def test(log):
    values = [
        ".#.#.#",
        "...##.",
        "#....#",
        "..#...",
        "#.#..#",
        "####..",
    ]

    if calc(log, values, 4, 0) == 4:
        return True
    else:
        return False

def run(log, values):
    log("Part 1: %d" % (calc(log, values, 100, 0),))
    log("Part 2: %d" % (calc(log, values, 100, 1),))

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
