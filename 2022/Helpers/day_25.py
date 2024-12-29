#!/usr/bin/env python3

DAY_NUM = 25
DAY_DESC = 'Day 25: Full of Hot Air'

def calc(log, values, mode):
    def decode(val):
        val = 0
        dig = 1
        for _ in row[:-1]:
            dig *= 5
        for x in row:
            if x == "-":
                val -= dig
            elif x == "=":
                val -= dig * 2
            else:
                val += dig * int(x)
            dig //= 5
        return val

    ret = 0
    for row in values:
        ret += decode(row)

    temp = ""
    dig = 1
    while dig < ret:
        dig *= 5
    
    dig //= 5
    temp = ""

    while True:
        x = ret/dig
        if x < 0:
            x = -int(abs(x) + 0.5)
        else:
            x = int(x + 0.5)
        ret -= x * dig
        if x == -1:
            temp += "-"
        elif x == -2:
            temp += "="
        else:
            temp += str(x)
        if dig == 1:
            break
        dig //= 5

    return temp

def test(log):
    values = log.decode_values("""
        1=-0-2
        12111
        2=0=
        21
        2=01
        111
        20012
        112
        1=-1=
        1-12
        12
        1=
        122
    """)

    log.test(calc(log, values, 1), '2=-1=0')

def run(log, values):
    log(f"Part 1: {calc(log, values, 1)}")

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2022/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
