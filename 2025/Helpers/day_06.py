#!/usr/bin/env python3

DAY_NUM = 6
DAY_DESC = 'Day 6: Trash Compactor'

def calc(log, values, mode):
    # TODO: Delete or use these
    # from parsers import get_ints, get_floats
    # from grid import Grid, Point
    # grid = Grid.from_text(values)
    # from program import Program
    # program = Program(values)

    import re
    from collections import defaultdict

    nums = defaultdict(list)
    ops = {}

    if mode == 1:
        for row in values:
            row = re.sub(" +", " ", row).split(' ')
            row = [x for x in row if len(x)]
            if len("".join(row)) == len(row):
                ops = {i: k for i, k in enumerate(row)}
            else:
                for i, k in enumerate(row):
                    nums[i].append(int(k))
    else:
        off = 0
        for i in range(len(values[0]) - 1, -1, -1):
            temp = [x[i] for x in values]
            if all(x == ' ' for x in temp):
                pass
            else:
                nums[off].append(int("".join(temp[:-1])))
                if temp[-1] != ' ':
                    ops[off] = temp[-1]
                    off += 1

    ret = 0
    for i in ops:
        temp = None
        for cur in nums[i]:
            if ops[i] == "+":
                if temp is None:
                    temp = cur
                else:
                    temp += cur
            elif ops[i] == "*":
                if temp is None:
                    temp = cur
                else:
                    temp *= cur
            else:
                raise Exception()
        ret += temp
    return ret

def test(log):
    values = log.decode_values("""
123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  
    """)

    log.test(calc(log, values, 1), '4277556')
    log.test(calc(log, values, 2), '3263827')

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
