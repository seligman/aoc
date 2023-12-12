#!/usr/bin/env python3

DAY_NUM = 12
DAY_DESC = 'Day 12: Hot Springs'

from functools import cache

clue, vals = None, None

@cache
def calc_clue(clue_off, dig, val_off, current_run):
    if dig == "E":
        if len(vals) == val_off and current_run == 0:
            return 1
    else:
        if dig == "?":
            return (
                calc_clue(clue_off, ".", val_off, current_run) + 
                calc_clue(clue_off, "#", val_off, current_run)
            )
        elif dig == ".":
            if current_run == 0:
                return calc_clue(clue_off + 1, clue[clue_off + 1], val_off, 0)
            elif current_run == vals[val_off]:
                return calc_clue(clue_off + 1, clue[clue_off + 1], val_off + 1, 0)
        else:
            if val_off < len(vals) and current_run < vals[val_off]:
                return calc_clue(clue_off + 1, clue[clue_off + 1], val_off, current_run + 1)
    
    return 0

def calc(log, values, mode):
    ret = 0
    global clue, vals

    for row in values:
        clue, vals = row.split(" ")
        if mode == 2:
            clue = "?".join([clue] * 5)
            vals = ",".join([vals] * 5)
        vals = tuple(int(x) for x in vals.split(","))
        clue += ".E"
        calc_clue.cache_clear()
        ret += calc_clue(0, clue[0], 0, 0)

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
