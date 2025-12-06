#!/usr/bin/env python3

DAY_NUM = 6
DAY_DESC = 'Day 6: Trash Compactor'

from collections import defaultdict

def calc(log, values, mode):
    nums = defaultdict(list)
    ops = {}
    off = 0

    values = [[x[i] for x in values] for i in range(len(values[0]))]

    for row in values:
        if all(x == ' ' for x in row):
            off += 1
        else:
            if mode == 1:
                if len(nums[off]) == 0:
                    nums[off] = [''] * (len(row) - 1)
                for i, x in enumerate(row[:-1]):
                    nums[off][i] += x
                if row[-1] != ' ':
                    ops[off] = row[-1]
            else:
                nums[off].append(int("".join(row[:-1])))
                if row[-1] != ' ':
                    ops[off] = row[-1]

    for i in range(len(nums)):
        nums[i] = [int(x) for x in nums[i]]

    ret = 0
    for i in ops:
        row = nums[i][0]
        for cur in nums[i][1:]:
            if ops[i] == "+":
                row += cur
            elif ops[i] == "*":
                row *= cur
            else:
                raise Exception()
        ret += row
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
