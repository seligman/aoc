#!/usr/bin/env python3

DAY_NUM = 5
DAY_DESC = 'Day 5: Supply Stacks'

def calc(log, values, mode):
    stacks = []
    values = [x.lstrip(".") for x in values]
    while True:
        row = values.pop(0)
        if row.strip().startswith("1"):
            break
        for i, val in enumerate(row):
            if 'A' <= val <= 'Z':
                i = int((i - 1) / 4)
                while len(stacks) <= i:
                    stacks.append([])
                stacks[i].append(val)

    for i in range(len(stacks)):
        stacks[i] = stacks[i][::-1]
        
    import re
    for row in values:
        m = re.search("move ([0-9]+) from ([0-9]+) to ([0-9]+)", row)
        if m is not None:
            steps = list(map(int, m.groups()))
            if mode == 1:
                for _ in range(steps[0]):
                    stacks[steps[2]-1].append(stacks[steps[1]-1].pop())
            else:
                temp = []
                for _ in range(steps[0]):
                    temp.append(stacks[steps[1]-1].pop())
                stacks[steps[2]-1] += temp[::-1]

    ret = ""
    for cur in stacks:
        ret += cur[-1]
    return ret

def test(log):
    values = log.decode_values("""
        .    [D]    
        .[N] [C]    
        .[Z] [M] [P]
        . 1   2   3 
        .
        .move 1 from 2 to 1
        .move 3 from 1 to 3
        .move 2 from 2 to 1
        .move 1 from 1 to 2
    """)

    log.test(calc(log, values, 1), 'CMZ')
    log.test(calc(log, values, 2), 'MCD')

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
    if fn is None: print("Unable to find input file!"); exit(1)
    with open(fn) as f: values = [x.strip() for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
