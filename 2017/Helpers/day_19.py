#!/usr/bin/env python3

DAY_NUM = 19
DAY_DESC = 'Day 19: A Series of Tubes'


def calc(log, values):
    y = 0
    for x in range(len(values[0])):
        if values[0][x] == "|":
            break

    dx, dy = 0, 1
    ret = ""
    steps = 0

    while True:
        x, y = x + dx, y + dy
        steps += 1

        if values[y][x] == "+":
            for ox, oy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                if (ox, oy) != (-dx, -dy) and values[y + oy][x + ox] != ' ':
                    dx, dy = ox, oy
                    break
        elif values[y][x] == " ":
            break
        elif values[y][x] not in {"-", "|"}:
            ret += values[y][x]

    log("Steps: " + str(steps))

    return ret


def test(log):
    values = [
        "     |          ",
        "     |  +--+    ",
        "     A  |  C    ",
        " F---|----E|--+ ",
        "     |  |  |  D ",
        "     +B-+  +--+ ",
        "                ",
    ]

    if calc(log, values) == "ABCDEF":
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
