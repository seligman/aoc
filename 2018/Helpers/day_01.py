#!/usr/bin/env python3

DAY_NUM = 1
DAY_DESC = 'Day 1: Chronal Calibration'


def calc(log, values, test_mode):
    ret = 0
    real_ret = None
    seen = {}
    first = True
    while first:
        for value in values:
            ret += value
            seen[ret] = seen.get(ret, 0) + 1
            if first:
                if seen[ret] == 2:
                    log("First twice is %d" % (ret,))
                    first = False
        if real_ret is None:
            real_ret = ret
        if test_mode:
            break
    return real_ret


def test(log):
    test = [
        ("+1, +1, +1",  3),
        ("+1, +1, -2",  0),
        ("-1, -2, -3", -6),
    ]
    for value, ret in test:
        values = [int(x.strip()) for x in value.split(', ')]
        test_val = calc(log, values, True)
        log("[%s] -> %d, %d" % (value, ret, test_val))
        if ret != test_val:
            return False

    return True


def run(log, values):
    values = [int(x) for x in values]
    log(calc(log, values, False))

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
