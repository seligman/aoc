#!/usr/bin/env python3

DAY_NUM = 23
DAY_DESC = 'Day 23: Crab Cups'

def calc(log, values, mode):
    if mode == 1:
        cups = [-1] * (len(values[0]))
    else:
        cups = [-1] * 1000000

    max_value = 0
    last = None

    for x in values[0]:
        x = int(x) - 1
        max_value = max(x, max_value)
        if last is not None:
            cups[last] = x
        last = x

    if mode == 2:
        while max_value < 1000000 - 1:
            max_value += 1
            cups[last] = max_value
            last = max_value

    cups[last] = int(values[0][0]) - 1
    cur = cups[last]
    cups_count = max_value + 1

    for round in range(100 if mode == 1 else 10000000):
        if round % 2500000 == 0:
            log(f"Working on round {round}")

        c1 = cups[cur]
        c2 = cups[c1]
        c3 = cups[c2]

        cups[cur] = cups[c3]

        target = (cur - 1) % cups_count
        if target == c1 or target == c2 or target == c3:
            target = (target - 1) % cups_count
            if target == c1 or target == c2 or target == c3:
                target = (target - 1) % cups_count
                if target == c1 or target == c2 or target == c3:
                    target = (target - 1) % cups_count

        cups[target], cups[c3] = c1, cups[target]
        cur = cups[cur]

    if mode == 1:
        temp = ""
        cur = cups[0]
        while cur != 0:
            temp += str(cur + 1)
            cur = cups[cur]
        return int(temp)
    else:
        return (cups[0] + 1) * (cups[cups[0]] + 1)

def test(log):
    values = log.decode_values("""
        389125467
    """)

    log.test(calc(log, values, 1), 67384529)
    log.test(calc(log, values, 2), 149245887792)

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
