#!/usr/bin/env python3

DAY_NUM = 11
DAY_DESC = 'Day 11: Plutonian Pebbles'

import functools

@functools.cache
def runner(x, dist):
    if dist == 0:
        return 1

    if x == 0:
        return runner(1, dist - 1)
    elif len(str(x)) % 2 == 0:
        x = str(x)
        return runner(int(x[:len(x)//2]), dist - 1) + runner(int(x[len(x)//2:]), dist - 1)
    else:
        return runner(x * 2024, dist - 1)


def calc(log, values, mode):
    row = [int(x) for x in values[0].split()]
    return sum(runner(x, 25 if mode == 1 else 75) for x in row)

def test(log):
    values = log.decode_values("""
        125 17
    """)

    log.test(calc(log, values, 1), '55312')
    # log.test(calc(log, values, 2), 'TODO')

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
