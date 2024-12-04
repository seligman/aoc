#!/usr/bin/env python3

import itertools

DAY_NUM = 24
DAY_DESC = 'Day 24: It Hangs in the Balance'


def get_all(values, target, invalid):
    values = set(values)
    for cur in invalid:
        values.remove(cur)
    for i in range(len(values)):
        for test in itertools.combinations(values, i + 1):
            if sum(test) == target:
                yield test


def calc(values, include_trunk):
    values = [int(x) for x in values]
    total_weight = sum(values)
    group_weight = total_weight / (4 if include_trunk else 3)

    best_count = len(values)
    best_entangle = 0

    for group_1 in get_all(values, group_weight, []):
        if len(group_1) > best_count:
            break

        entangle = 1
        for cur in group_1:
            entangle *= cur
        if entangle < best_entangle:
            best_entangle = entangle

        skip = False
        if len(group_1) == best_count:
            if entangle >= best_entangle:
                skip = True

        if not skip:
            any_valid = False
            for group_2 in get_all(values, group_weight, group_1):
                for group_3 in get_all(values, group_weight, group_1 + group_2):
                    if include_trunk:
                        for _group_4 in get_all(values, group_weight, group_1 + group_2 + group_3):
                            any_valid = True
                            break
                        if any_valid:
                            break
                    else:
                        any_valid = True
                        break
                if any_valid:
                    break

            if any_valid:
                if len(group_1) < best_count:
                    best_count = len(group_1)
                    best_entangle = entangle
                elif len(group_1) == best_count:
                    best_entangle = entangle

    return best_entangle


def test(log):
    values = [
        "1",
        "2",
        "3",
        "4",
        "5",
        "7",
        "8",
        "9",
        "10",
        "11",
    ]

    log("With trunk: " + str(calc(values, True)))
    if calc(values, False) == 99:
        return True
    else:
        return False


def run(log, values):
    log("No trunk: " + str(calc(values, False)))
    log("With trunk: " + str(calc(values, True)))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2015/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
