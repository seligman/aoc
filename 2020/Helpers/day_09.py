#!/usr/bin/env python3

DAY_NUM = 9
DAY_DESC = 'Day 9: Encoding Error'

def calc(log, values, mode, preamble):
    values = [int(x) for x in values]

    ret = -1    
    
    for off in range(preamble, len(values)):
        found = False
        for i in range(off - preamble, off):
            if found:
                break
            for j in range(i+1, off):
                if values[i] + values[j] == values[off]:
                    found = True
                    break
        if not found:
            ret = values[off]
            break

    if mode == 1:
        return ret

    temp = []
    for x in values:
        temp.append(x)
        if sum(temp) == ret:
            return  min(temp) + max(temp)
        while len(temp) > 1 and sum(temp) > ret:
            temp.pop(0)
            if sum(temp) == ret:
                return min(temp) + max(temp)


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
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2020/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
