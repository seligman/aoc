#!/usr/bin/env python3

DAY_NUM = 9
DAY_DESC = 'Day 9: Mirage Maintenance'

def calc(log, values, mode):
    ret = 0

    if mode == 1: next_value = lambda a, b: a + b
    else: next_value = lambda a, b: b - a

    for row in values:
        row = [[int(x) for x in row.split(" ")]]
        while any(row[-1]):
            last = row[-1]
            row.append([last[x+1] - last[x] for x in range(len(last)-1)])

        if mode == 2:
            row = [x[::-1] for x in row]

        row[-1].append(0)
        for i in range(len(row)-2, -1, -1):
            row[i].append(next_value(row[i+1][-1], row[i][-1]))
        ret += row[0][-1]

    return ret

def test(log):
    values = log.decode_values("""
        0 3 6 9 12 15
        1 3 6 10 15 21
        10 13 16 21 30 45
    """)

    log.test(calc(log, values, 1), '114')
    log.test(calc(log, values, 2), '2')

def run(log, values):
    log(f"Part 1: {calc(log, values, 1)}")
    log(f"Part 2: {calc(log, values, 2)}")

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2023/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
