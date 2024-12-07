#!/usr/bin/env python3

DAY_NUM = 7
DAY_DESC = 'Day 7: Bridge Repair'

from collections import deque

def calc(log, values, mode):
    if mode == 1:
        possible = ["+", "*"]
    else:
        possible = ["+", "*", "||"]

    ret = 0
    for row in values:
        target, args = row.split(": ")
        target = int(target)
        args = [{"oper": 0, "val": int(x)} for x in args.split()]

        todo = deque()
        todo.append((args[0]['val'], 1))
        
        finish = len(args)
        while len(todo) > 0:
            val, pos = todo.pop()
            if pos == finish:
                if val == target:
                    ret += target
                    break
            else:
                next_val = args[pos]['val']
                for oper in possible:
                    if oper == "*":
                        temp = next_val * val
                    elif oper == "+":
                        temp = next_val + val
                    elif oper == "||":
                        temp = int(str(val) + str(next_val))
                    else:
                        raise Exception()
                    if temp <= target:
                        todo.append((temp, pos + 1))

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
