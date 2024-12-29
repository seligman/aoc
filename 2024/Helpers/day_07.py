#!/usr/bin/env python3

DAY_NUM = 7
DAY_DESC = 'Day 7: Bridge Repair'

from collections import deque, namedtuple
import math

def calc(log, values, mode):
    ret = 0
    test = namedtuple('test', ['val', 'pos'])
    for row in values:
        row = list(map(int, row.replace(":", "").split()))
        todo = deque()
        todo.append(test(row[0], len(row) - 1))
        while len(todo) > 0:
            cur = todo.pop()
            if cur.pos == 1:
                if cur.val == row[1]:
                    ret += row[0]
                    break
            else:
                if cur.val % row[cur.pos] == 0:
                    todo.append(test(cur.val // row[cur.pos], cur.pos - 1))
                if cur.val > row[cur.pos]:
                    todo.append(test(cur.val - row[cur.pos], cur.pos - 1))
                if mode == 2:
                    mul = 10 ** int(math.log10(row[cur.pos])+1)
                    if cur.val % mul == row[cur.pos]:
                        todo.append(test(cur.val // mul, cur.pos - 1))

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

    # log.test(calc(log, values, 1), '3749')
    # log.test(calc(log, values, 2), '11387')

    values = log.decode_values("""
        20: 2 3 4
        2012: 2 3 4 12
    """)

    log.test(calc(log, values, 1), '20')
    log.test(calc(log, values, 2), '2032')


def run(log, values):
    log(f"Part 1: {calc(log, values, 1)}")
    log(f"Part 2: {calc(log, values, 2)}")

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
