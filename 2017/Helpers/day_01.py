#!/usr/bin/env python3

DAY_NUM = 1
DAY_DESC = 'Day 1: Inverse Captcha'


def calc(log, values):
    value = list(values[0])
    ret = 0
    ret2 = 0

    for i in range(len(value)):
        if value[i] == value[(i+1)%len(value)]:
            ret += int(value[i])
        if value[i] == value[(i+(len(value)//2))%len(value)]:
            ret2 += int(value[i])

    log("Half around: " + str(ret2))

    return ret


def test(log):
    values = [
        "91212129",
    ]

    if calc(log, values) == 9:
        return True
    else:
        return False


def run(log, values):
    log(calc(log, values))

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
