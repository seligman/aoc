#!/usr/bin/env python3

DAY_NUM = 25
DAY_DESC = 'Day 25: Combo Breaker'

def transform(loop, subject):
    value = 1
    for _ in range(loop):
        value = value * subject
        value = value % 20201227
    return value

def transform_bail(subject, bail):
    value = 1
    loop = 0
    while True:
        loop += 1
        value = value * subject
        value = value % 20201227
        if bail == value:
            return loop

def calc(log, values, mode):
    door = transform_bail(7, int(values[1]))
    return transform(door, int(values[0]))


def test(log):
    values = log.decode_values("""
        5764801
        17807724
    """)

    log.test(calc(log, values, 1), 14897079)

def run(log, values):
    log(calc(log, values, 1))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in [[], ["Puzzles"], ["..", "Puzzles"]]:
                cur = os.path.join(*(dn + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!"); exit(1)
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
