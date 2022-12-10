#!/usr/bin/env python3

DAY_NUM = 9
DAY_DESC = 'Day 9: Encoding Error'

def calc(log, values, mode, preamble):
    values = [int(x) for x in values]
    orig = values[:]
    temp = values[:preamble]
    values = values[preamble:]
    while True:
        found = False
        for i in range(preamble):
            if found:
                break
            for j in range(i, preamble):
                if temp[i] + temp[j] == values[0]:
                    found = True
                    temp = temp[1:] + values[0:1]
                    values = values[1:]
                    break
        if not found:
            if mode == 1:
                return values[0]
            else:
                for i in range(len(orig)):
                    for j in range(len(orig) - (i + 1)):
                        temp = sum(orig[i:j])
                        if temp == values[0]:
                            return min(orig[i:j]) + max(orig[i:j])
                        if temp > values[0]:
                            break

    return -1

def test(log):
    values = log.decode_values("""
        35
        20
        15
        25
        47
        40
        62
        55
        65
        95
        102
        117
        150
        182
        127
        219
        299
        277
        309
        576
    """)

    log.test(calc(log, values, 1, 5), 127)
    log.test(calc(log, values, 2, 5), 62)

def run(log, values):
    log(calc(log, values, 1, 25))
    log(calc(log, values, 2, 25))

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
