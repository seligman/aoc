#!/usr/bin/env python3

DAY_NUM = 1
DAY_DESC = 'Day 1: Trebuchet?!'

import re

def calc(log, values, mode):
    ret = 0

    digits = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }

    test = "1|2|3|4|5|6|7|8|9"
    if mode == 2:
        test += "|" + "|".join(digits)

    for cur in values:
        m = re.search("(" + test + ")", cur)
        val = digits.get(m.group(1), m.group(1))
        m = re.search(".*(" + test + ")", cur)
        val += digits.get(m.group(1), m.group(1))
        ret += int(val)

    return ret

def test(log):
    values = log.decode_values("""
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
    """)

    log.test(calc(log, values, 1), '142')

    values = log.decode_values("""
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
        """)

    log.test(calc(log, values, 2), '281')

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))

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
