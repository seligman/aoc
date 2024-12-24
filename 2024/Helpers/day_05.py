#!/usr/bin/env python3

DAY_NUM = 5
DAY_DESC = 'Day 5: Print Queue'

def calc(log, values, mode):
    rules = []
    ret = 0
    for row in values:
        if "|" in row:
            rules.append(list(map(int, row.split("|"))))
        elif "," in row:
            row = {x: i for i, x in enumerate(map(int, row.split(",")))}
            first = True
            while True:
                problems = []
                for a, b in rules:
                    if a in row and b in row:
                        if row[a] > row[b]:
                            problems.append((a, b))
                            break
                
                if mode == 1 or (mode == 2 and not first and len(problems) == 0):
                    if len(problems) == 0:
                        ret += sum(k for k, v in row.items() if v == (len(row) - 1) // 2)
                    break
                else:
                    if first and len(problems) == 0:
                        break
                    first = False
                    a, b = problems[0]
                    row[a], row[b] = row[b], row[a]

    return ret

def test(log):
    values = log.decode_values("""
        47|53
        97|13
        97|61
        97|47
        75|29
        61|13
        75|53
        29|13
        97|29
        53|29
        61|53
        97|53
        61|29
        47|13
        75|47
        97|75
        47|61
        75|61
        47|29
        75|13
        53|13

        75,47,61,53,29
        97,61,53,29,13
        75,29,13
        75,97,47,61,53
        61,13,29
        97,13,75,29,47
    """)

    log.test(calc(log, values, 1), '143')
    log.test(calc(log, values, 2), '123')

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
