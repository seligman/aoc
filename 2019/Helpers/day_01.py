#!/usr/bin/env python3

DAY_NUM = 1
DAY_DESC = 'Day 1: The Tyranny of the Rocket Equation'


def calc(log, values, mode):
    ret = 0
    for cur in values:
        if mode == 1:
            ret += (int(cur) // 3) - 2
        else:
            first = True
            while True:
                temp = (int(cur) // 3) - 2
                if temp > 0 or first:
                    ret += temp
                first = False
                if temp > 0:
                    cur = temp
                else:
                    break

    return ret


def test(log):
    values = log.decode_values("""
        100756
    """)

    ret, expected = calc(log, values, 1), 33583 
    log("Test returned %s, expected %s" % (str(ret), str(expected)))
    if ret != expected:
        return False
    ret, expected = calc(log, values, 2), 50346 
    log("Test returned %s, expected %s" % (str(ret), str(expected)))
    if ret != expected:
        return False

    return True


def run(log, values):
    log("Fuel requirements: " + str(calc(log, values, 1)))
    log("Including mass: " + str(calc(log, values, 2)))

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
