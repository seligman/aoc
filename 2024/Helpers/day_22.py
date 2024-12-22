#!/usr/bin/env python3

DAY_NUM = 22
DAY_DESC = 'Day 22: Monkey Market'

def calc(log, values, mode):
    ret = 0
    if mode == 1:
        for row in values:
            x = int(row)
            for _ in range(2000):
                x = ((x * 64) ^ x) % 16777216
                x = ((x // 32) ^ x) % 16777216
                x = ((x * 2048) ^ x) % 16777216
            ret += x
    else:
        total = {}
        for row in values:
            x = int(row)
            last = x % 10
            pattern = []
            for _ in range(2000):
                x = ((x * 64) ^ x) % 16777216
                x = ((x // 32) ^ x) % 16777216
                x = ((x * 2048) ^ x) % 16777216
                temp = x % 10
                pattern.append((temp - last, temp))
                last = temp
            seen = set()
            for i in range(len(pattern)-4):
                pat = tuple(x[0] for x in pattern[i:i+4])
                val = pattern[i+3][1]
                if pat not in seen:
                    seen.add(pat)
                    if pat not in total:
                        total[pat] = val
                    else:
                        total[pat] += val
        ret = max(total.values())

    return ret

def test(log):
    values = log.decode_values("""
        1
        10
        100
        2024
    """)

    log.test(calc(log, values, 1), '37327623')

    values = log.decode_values("""
        1
        2
        3
        2024
    """)
    log.test(calc(log, values, 2), '23')

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2024/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
