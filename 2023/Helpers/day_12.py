#!/usr/bin/env python3

DAY_NUM = 12
DAY_DESC = 'Day 12: Hot Springs'

from functools import cache

@cache
def calc_clue(clue, vals, current_run):
    ret = 0

    if clue == ".":
        if len(vals) == 0 and current_run == 0:
            ret += 1
    else:
        if clue[0] == "?":
            if current_run == 0 or len(vals) > 0 and vals[0] == current_run:
                ret += calc_clue("." + clue[1:], vals, current_run)
            if len(vals) > 0:
                ret += calc_clue("#" + clue[1:], vals, current_run)
        elif clue[0] == "#":
            if len(vals) > 0:
                if vals[0] == current_run + 1:
                    if clue[1] == ".":
                        ret += calc_clue(clue[1:], vals[1:], 0)
                    elif clue[1] == "?":
                        ret += calc_clue("." + clue[2:], vals[1:], 0)
                elif current_run < vals[0]:
                    if clue[1] == "#":
                        ret += calc_clue(clue[1:], vals, current_run + 1)
                    elif clue[1] == "?":
                        ret += calc_clue("#" + clue[2:], vals, current_run + 1)
        elif clue[0] == "." and current_run == 0:
            ret += calc_clue(clue[1:], vals, 0)
    
    return ret

def calc(log, values, mode):
    ret = 0

    for row in values:
        clue, vals = row.split(" ")
        if mode == 2:
            clue = "?".join([clue] * 5)
            vals = ",".join([vals] * 5)
        vals = tuple(int(x) for x in vals.split(","))
        clue += "."
        ret += calc_clue(clue, vals, 0)

    return ret

def test(log):
    values = log.decode_values("""
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
    """)

    log.test(calc(log, values, 1), '21')
    log.test(calc(log, values, 2), '525152')

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
