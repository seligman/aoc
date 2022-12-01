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
    log(calc(log, values, 1))
    log(calc(log, values, 2))

if __name__ == "__main__":
    import sys, os
    cur = None
    for cur in sys.argv[1:] + ["input.txt", "day_##_input.txt", "Puzzles/day_##_input.txt", "../Puzzles/day_##_input.txt"]:
        cur = os.path.join(*cur.split("/")).replace("##", f"{DAY_NUM:02d}")
        if os.path.isfile(cur): fn = cur; break
    if cur is None: print("Unable to find input file!"); exit(1)
    with open(fn) as f: values = f.readlines()
    print(f"Running day {DAY_DESC}:")
    run(print, values)
