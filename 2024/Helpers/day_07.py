#!/usr/bin/env python3

DAY_NUM = 7
DAY_DESC = 'Day 7: Bridge Repair'

from collections import deque

def calc(log, values, mode):
    possible = []
    if mode in {1, 2}:
        possible.append(lambda x, y: x + y)
        possible.append(lambda x, y: x * y)
    if mode == 2:
        possible.append(lambda x, y: int(str(x) + str(y)))

    ret = 0
    for row in values:
        target, args = row.split(": ")
        target = int(target)
        args = [int(x) for x in args.split()]
        if mode == 2:
            mul = [10 ** len(str(x)) for x in args]

        todo = deque()
        todo.append((args[0], 1))
        finish = len(args)
        
        while len(todo) > 0:
            val, pos = todo.pop()
            if val <= target:
                if pos == finish:
                    if val == target:
                        ret += target
                        break
                else:
                    x = args[pos]
                    todo.append((val + x, pos + 1))
                    todo.append((val * x, pos + 1))
                    if mode == 2:
                        todo.append((val * mul[pos] + x, pos + 1))

    return ret

def test(log):
    values = log.decode_values("""
        190: 10 19
        3267: 81 40 27
        83: 17 5
        156: 15 6
        7290: 6 8 6 15
        161011: 16 10 13
        192: 17 8 14
        21037: 9 7 18 13
        292: 11 6 16 20
    """)

    log.test(calc(log, values, 1), '3749')
    log.test(calc(log, values, 2), '11387')

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
