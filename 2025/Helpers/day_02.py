#!/usr/bin/env python3

import math

DAY_NUM = 2
DAY_DESC = 'Day 2: Gift Shop'

_mult_1 = {}
def is_valid_1(a):
    digits = int(math.log10(a) + 1)
    if digits not in _mult_1:
        _mult_1[digits] = []
        if digits % 2 == 0:
            temp = 1 + 10 ** (digits // 2)
            _mult_1[digits].append((temp, 10 ** (digits // 2)))

    for test, part in _mult_1[digits]:
        if test * (a % part) == a:
            return True

    return False

_mult_2 = {}
def is_valid_2(a):
    digits = int(math.log10(a) + 1)
    if digits not in _mult_2:
        _mult_2[digits] = []
        for digits_i in range(1, digits):
            if digits % digits_i == 0:
                temp = 0
                for _ in range(digits // digits_i):
                    temp *= 10 ** digits_i
                    temp += 1
                _mult_2[digits].append((temp, 10 ** digits_i))

    for test, part in _mult_2[digits]:
        if test * (a % part) == a:
            return True

    return False

def calc(log, values, mode):
    ret = 0
    ab, ac = 999999999999, 0
    for cur in values[0].split(","):
        a, b = cur.split('-')
        for i in range(int(a), int(b) + 1):
            if (mode == 1 and is_valid_1(i)) or (mode == 2 and is_valid_2(i)):
                ret += i
    return ret

def test(log):
    values = log.decode_values("""
11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124
    """)

    log.test(calc(log, values, 1), '1227775554')
    log.test(calc(log, values, 2), '4174379265')

def run(log, values):
    log("Part 1")
    log(calc(log, values, 1))
    log("Part 2")
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
