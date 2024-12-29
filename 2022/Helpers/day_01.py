#!/usr/bin/env python3

DAY_NUM = 1
DAY_DESC = 'Day 1: Calorie Counting'

def calc(log, values, mode):
    batches = [[]]
    for cur in values:
        if len(cur) == 0:
            batches.append([])
        else:
            batches[-1].append(int(cur))
    
    batches = [sum(x) for x in batches]
    
    if mode == 1:
        return str(max(batches))
    else:
        batches.sort(reverse=True)
        return str(sum(batches[0:3]))

def test(log):
    values = log.decode_values("""
        1000
        2000
        3000

        4000

        5000
        6000

        7000
        8000
        9000

        10000
    """)

    log.test(calc(log, values, 1), '24000')
    log.test(calc(log, values, 2), '45000')

def run(log, values):
    log(f"Part 1: {calc(log, values, 1)}")
    log(f"Part 2: {calc(log, values, 2)}")

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2022/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
