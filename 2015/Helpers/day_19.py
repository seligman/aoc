#!/usr/bin/env python3

from collections import deque

DAY_NUM = 19
DAY_DESC = 'Day 19: Medicine for Rudolph'

class Step:
    def __init__(self, chemical, level):
        self.level = level
        self.chemical = chemical[:]

def calc(log, values, mode):
    chemical = []
    for cur in values[-1]:
        if "A" <= cur <= "Z":
            chemical.append(cur)
        else:
            chemical[-1] += cur

    mutations = {}
    for cur in values[0:-2]:
        cur = cur.split(" => ")
        if cur[0] not in mutations:
            mutations[cur[0]] = []
        test = []
        for sub in cur[1]:
            if "A" <= sub <= "Z":
                test.append(sub)
            else:
                test[-1] += sub
        mutations[cur[0]].append(test)

    if mode == 0:
        seen = set()
        for i in range(len(chemical)):
            old = chemical[i]
            if old in mutations:
                for test in mutations[old]:
                    chemical[i] = "".join(test)
                    seen.add("".join(chemical))
                chemical[i] = old
        return len(seen)
    else:
        inverse = {}
        for key in mutations:
            value = mutations[key]
            for sub in value:
                sub = tuple(sub)
                if sub in inverse:
                    log(sub)
                    raise Exception()
                inverse[sub] = key

        to_check = deque()
        to_check.append(Step(chemical, 0))

        bail = 100000
        best_step = None
        while len(to_check) > 0:
            bail -= 1
            if bail == 0:
                break

            cur = to_check.pop()
            for i in range(len(cur.chemical)):
                for key in inverse:
                    value = inverse[key]
                    if key == tuple(cur.chemical[i: len(key) + i]):
                        test = cur.chemical[0:i] + [value] + cur.chemical[i+len(key):]
                        if len(test) == 1 and test[0] == "e":
                            if best_step is None or cur.level < best_step:
                                best_step = cur.level
                                log("Found answer: " + str(best_step + 1))
                        to_check.append(Step(test, cur.level + 1))

        return best_step + 1

def test(log):
    values = [
        "Ha => HaO",
        "Ha => OHa",
        "O => HaHa",
        "e => Ha",
        "",
        "HaOHaOHaO",
    ]

    if calc(log, values, 0) == 7:
        if calc(log, values, 1) == 6:
            return True
        else:
            return False
    else:
        return False

def run(log, values):
    log("Part 1: %d" % (calc(log, values, 0),))
    log("Part 2: %d" % (calc(log, values, 1),))

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
