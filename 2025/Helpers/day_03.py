#!/usr/bin/env python3

DAY_NUM = 3
DAY_DESC = 'Day 3: Lobby'

def get_best(battery, left):
    seen = {}
    for i, a in enumerate(battery):
        if a not in seen:
            seen[a] = i
    for a, i in [(a, seen[a]) for a in sorted(seen, key=int, reverse=True)]:
        if left == 1:
            return a
        else:
            next_val = get_best(battery[i+1:], left-1)
            if next_val is not None:
                return a + next_val
    return None

def calc(log, values, mode):
    ret = 0

    for battery in values:
        val = get_best(battery, 2 if mode == 1 else 12)
        ret += int(val)

    return ret

def test(log):
    values = log.decode_values("""
987654321111111
811111111111119
234234234234278
818181911112111
    """)

    log.test(calc(log, values, 1), '357')
    log.test(calc(log, values, 2), '3121910778619')

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
