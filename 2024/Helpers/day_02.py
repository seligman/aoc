#!/usr/bin/env python3

DAY_NUM = 2
DAY_DESC = 'Day 2: Red-Nosed Reports'

def calc(log, values, mode):
    values = [list(map(int, x.split())) for x in values]

    ret = 0

    for row in values:
        last = row[0]
        is_neg = None
        fail = 0
        temp = row
        for i in range(-1, 0 if mode == 1 else len(temp)):
            if i == -1:
                row = temp
            else:
                row = temp[:]
                row.pop(i)
            fail = 0
            is_neg = None
            last = row[0]
            for x in row[1:]:
                diff = x - last
                if diff < 0:
                    diff = -diff
                    if is_neg is None:
                        is_neg = True
                    else:
                        if not is_neg:
                            fail += 1
                else:
                    if is_neg is None:
                        is_neg = False
                    else:
                        if is_neg:
                            fail += 1
                if diff not in {1, 2, 3}:
                    fail += 1
                last = x
            if fail == 0:
                break
        if fail <= 0:
            ret += 1

    return ret

def test(log):
    values = log.decode_values("""
        7 6 4 2 1
        1 2 7 8 9
        9 7 6 2 1
        1 3 2 4 5
        8 6 4 4 1
        1 3 6 7 9
    """)

    log.test(calc(log, values, 1), '2')
    log.test(calc(log, values, 2), '4')

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
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
