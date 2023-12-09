#!/usr/bin/env python3

DAY_NUM = 9
DAY_DESC = 'Day 9: Mirage Maintenance'

def calc(log, values, mode):
    ret = 0

    for row in values:
        row = [[int(x) for x in row.split(" ")]]
        while tuple(row[-1]) != tuple(0 for _ in row[-1]):
            last = row[-1]
            row.append([last[x+1] - last[x] for x in range(len(last)-1)])
        if mode == 1:
            row[-1].append(0)
            for i in range(len(row)-2, -1, -1):
                row[i].append(row[i+1][-1] + row[i][-1])
            ret += row[0][-1]
        else:
            row[-1].insert(0, 0)
            for i in range(len(row)-2, -1, -1):
                row[i].insert(0, row[i][0] - row[i+1][0])
            ret += row[0][0]

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
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
