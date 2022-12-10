#!/usr/bin/env python3

DAY_NUM = 1
DAY_DESC = 'Day 1: Sonar Sweep'

def calc(log, values, mode):
    values = [int(x) for x in values]
    window_size = {1: 1, 2: 3}[mode]
    last = sum(values[0:window_size])
    ret = 0
    for i in range(len(values) - window_size + 1):
        cur = sum(values[i:i+window_size])
        if cur > last: ret += 1
        last = cur
    return ret

def test(log):
    values = log.decode_values("""
        199
        200
        208
        210
        200
        207
        240
        269
        260
        263    
    """)

    log.test(calc(log, values, 1), 7)
    log.test(calc(log, values, 2), 5)

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
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
