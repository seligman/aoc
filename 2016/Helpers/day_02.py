#!/usr/bin/env python3

DAY_NUM = 2
DAY_DESC = 'Day 2: Bathroom Security'


def calc(values, mode):
    steps = {}

    if mode == 0:
        keypad = [
            "     ",
            " 123 ",
            " 456 ",
            " 789 ",
            "     ",
        ]
    else:
        keypad = [
            "       ",
            "   1   ",
            "  234  ",
            " 56789 ",
            "  ABC  ",
            "   D   ",
            "       ",
        ]

    keypad = [list(x) for x in keypad]
    for y in range(0, len(keypad)):
        for x in range(0, len(keypad[0])):
            if keypad[y][x] != ' ':
                steps[keypad[y][x]] = {
                    'U': keypad[y][x] if keypad[y-1][x] == " " else keypad[y-1][x],
                    'D': keypad[y][x] if keypad[y+1][x] == " " else keypad[y+1][x],
                    'L': keypad[y][x] if keypad[y][x-1] == " " else keypad[y][x-1],
                    'R': keypad[y][x] if keypad[y][x+1] == " " else keypad[y][x+1],
                }


    ret = ""

    digit = '5'
    for line in values:
        for cur in line:
            digit = steps[digit][cur]
        ret += digit

    return ret


def test(log):
    values = [
        "ULL",
        "RRDDD",
        "LURDL",
        "UUUUD",
    ]

    if calc(values, 0) == "1985":
        return True
    else:
        return False


def run(log, values):
    log(calc(values, 0))
    log(calc(values, 1))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in [[], ["Puzzles"], ["..", "Puzzles"]]:
                cur = os.path.join(*(dn + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
