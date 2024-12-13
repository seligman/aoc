#!/usr/bin/env python3

DAY_NUM = 13
DAY_DESC = 'Day 13: Claw Contraption'

def calc(log, values, mode):
    import re
    r = re.compile("X[\\+=](?P<x>[0-9]+), Y[\\+=](?P<y>[0-9]+)")
    ret = 0
    for i in range(0, len(values), 4):
        m = r.search(values[i])
        x_a, y_a = int(m["x"]), int(m["y"])
        m = r.search(values[i+1])
        x_b, y_b = int(m["x"]), int(m["y"])
        m = r.search(values[i+2])
        x_prize, y_prize = int(m["x"]), int(m["y"])

        if mode == 2:
            x_prize += 10000000000000
            y_prize += 10000000000000

        press_b = (x_prize * y_a - y_prize * x_a) // (x_b * y_a - y_b * x_a)
        press_a = (y_prize - y_b * press_b) // y_a
        if press_a * x_a + press_b * x_b == x_prize and press_a * y_a + press_b * y_b == y_prize:
            ret += 3 * press_a + press_b

    return ret

def test(log):
    values = log.decode_values("""
        Button A: X+94, Y+34
        Button B: X+22, Y+67
        Prize: X=8400, Y=5400

        Button A: X+26, Y+66
        Button B: X+67, Y+21
        Prize: X=12748, Y=12176

        Button A: X+17, Y+86
        Button B: X+84, Y+37
        Prize: X=7870, Y=6450

        Button A: X+69, Y+23
        Button B: X+27, Y+71
        Prize: X=18641, Y=10279
    """)

    log.test(calc(log, values, 1), '480')

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2024/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
