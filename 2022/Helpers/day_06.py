#!/usr/bin/env python3

DAY_NUM = 6
DAY_DESC = 'Day 6: Tuning Trouble'

def calc(log, values, mode):
    last = []
    target_len = 4 if mode == 1 else 14
    for i in range(len(values[0])):
        if len(set(values[0][i:target_len+i])) == target_len:
            return i + target_len

def test(log):
    values = log.decode_values("""
        mjqjpqmgbljsphdztnvjfqwrcgsmlb
    """)

    log.test(calc(log, values, 1), 7)
    log.test(calc(log, values, 2), 19)

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
