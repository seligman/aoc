#!/usr/bin/env python3

DAY_NUM = 2
DAY_DESC = 'Day 2: 1202 Program Alarm'


def calc(log, values, replace_1=None, replace_2=None):
    ticker = [int(x) for x in values[0].split(",")]
    if replace_1:
        ticker[1] = replace_1
        ticker[2] = replace_2
    off = 0
    while True:
        op = ticker[off]
        if op == 1:
            ticker[ticker[off+3]] = ticker[ticker[off+1]] + ticker[ticker[off+2]]
        elif op == 2:
            ticker[ticker[off+3]] = ticker[ticker[off+1]] * ticker[ticker[off+2]]
        elif op == 99:
            break
        else:
            raise Exception()
        off += 4

    return ticker[0]


def test(log):
    if calc(log, ["1,9,10,3,2,3,11,0,99,30,40,50"]) != 3500:
        return False
    if calc(log, ["1,0,0,0,99"]) != 2:
        return False
    if calc(log, ["2,4,4,5,99,0"]) != 2:
        return False
    if calc(log, ["1,1,1,4,99,5,6,0,99"]) != 30:
        return False

    return True


def run(log, values):
    log("Position 0: " + str(calc(log, values, replace_1=12, replace_2=2)))
    found = False
    for a in range(100):
        if found:
            break
        for b in range(200):
            try:
                if calc(log, values, replace_1=a, replace_2=b) == 19690720:
                    log("Noun * Verb: " + str(100 * a + b))
                    found = True
                    break
            except:
                pass

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
