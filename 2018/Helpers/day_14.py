#!/usr/bin/env python3

DAY_NUM = 14
DAY_DESC = 'Day 14: Chocolate Charts'


def calc(log, values, test_mode):
    scores = "37"
    elv_0 = 0
    elv_1 = 1

    test = 1000
    test_start = 0

    while True:
        if test_mode:
            if len(scores) >= values + 10:
                break
        scores += str(int(scores[elv_0]) + int(scores[elv_1]))
        elv_0 = (elv_0 + int(scores[elv_0]) + 1) % len(scores)
        elv_1 = (elv_1 + int(scores[elv_1]) + 1) % len(scores)
        test -= 1
        if test == 0:
            loc = scores.find("920831", test_start)
            if loc >= 0:
                log("Found index at %d" % (scores.index("920831"),))
                break
            else:
                log(len(scores))
            test_start = len(scores) - 50
            test = 10000000

    return scores[values:values+10]


def test(log):
    if calc(log, 2018, True) == "5941429882":
        return True
    else:
        return False


def run(log, values):
    log(calc(log, 920831, False))

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
