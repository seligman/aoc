#!/usr/bin/env python3

DAY_NUM = 20
DAY_DESC = 'Day 20: Grove Positioning System'

def calc(log, values, mode):
    key = 811589153

    values = [(int(x), i) for i, x in enumerate(values)]

    if mode == 1:
        passes = 1
    elif mode == 2:
        passes = 10
        values = [(x * key, i) for x, i in values]

    todo = values[:]

    for _ in range(passes):
        for x in todo:
            cur_pos, next_pos = "-", "-"
            if x != 0 or True:
                cur_pos = values.index(x)
                next_pos = (cur_pos + x[0]) % (len(values)-1)
                values.pop(cur_pos)
                values.insert(len(values) if next_pos == 0 else next_pos, x)

    at = min(i for i, (x, _) in enumerate(values) if x == 0)

    ret = 0
    for i in range(1, 4):
        ret += values[(i * 1000 + at) % len(values)][0]

    return ret

def test(log):
    values = log.decode_values("""
        1
        2
        -3
        3
        -2
        0
        4
    """)

    log.test(calc(log, values, 1), '3')
    log.test(calc(log, values, 2), '1623178306')

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
