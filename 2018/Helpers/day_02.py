#!/usr/bin/env python3

DAY_NUM = 2
DAY_DESC = 'Day 2: Inventory Management System'


def calc(log, values):
    hits = {}
    valid = []
    for cur_value in values:
        counts = {}
        for cur in cur_value:
            counts[cur] = counts.get(cur, 0) + 1
        seen = set()
        for value in counts.values():
            if value > 1 and value not in seen:
                hits[value] = hits.get(value, 0) + 1
                seen.add(value)
        if (2 in seen) or (3 in seen):
            valid.append(cur_value)

    found = None
    for i in range(len(valid)):
        if found is not None:
            break
        for j in range(i + 1, len(valid)):
            if found is not None:
                break
            matches = ""
            for x in range(len(valid[i])):
                if valid[i][x] == valid[j][x]:
                    matches += valid[i][x]
            if len(matches) == len(valid[i]) - 1:
                log(matches)
                found = matches

    ret = 1
    for value in hits.values():
        ret *= value

    return ret


def test(log):
    test = [
        "abcdef",
        "bababc",
        "abbcde",
        "abcccd",
        "aabcdd",
        "abcdee",
        "ababab",
    ]

    if calc(log, test) != 12:
        return False

    return True


def run(log, values):
    log(calc(log, values))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2018/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
