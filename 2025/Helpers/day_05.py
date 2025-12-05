#!/usr/bin/env python3

DAY_NUM = 5
DAY_DESC = 'Day 5: Cafeteria'

def calc(log, values, mode):
    ranges = []

    ret = 0
    for row in values:
        if "-" in row:
            a, b = row.split('-')
            ranges.append((int(a), int(b)))
        elif len(row):
            if mode == 1:
                x = int(row)
                for a, b in ranges:
                    if a <= x <= b:
                        ret += 1
                        break
            else:
                ranges.sort()
                final = [ranges.pop(0)]
                for a, b in ranges:
                    x, y = final[-1]
                    if a <= y:
                        final[-1] = (x, max(b, y))
                    else:
                        final.append((a, b))
                for a, b in final:
                    ret += (b - a) + 1
                break

    return ret

def test(log):
    values = log.decode_values("""
3-5
10-14
16-20
12-18

1
5
8
11
17
32

    """)

    log.test(calc(log, values, 1), '3')
    log.test(calc(log, values, 2), '14')

def run(log, values):
    log("Part 1")
    log(calc(log, values, 1))
    log("Part 2")
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
