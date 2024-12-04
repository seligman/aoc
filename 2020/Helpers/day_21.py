#!/usr/bin/env python3

import re
from collections import defaultdict

DAY_NUM = 21
DAY_DESC = 'Day 21: Allergen Assessment'

def calc(log, values, mode):
    r = re.compile(r"^(?P<ingred>[^(]+)(| \(contains (?P<aller>.*)\))$")

    allers = {}
    ingreds = defaultdict(int)

    for row in values:
        m = r.search(row)
        ingred = m.group("ingred").split(" ")
        aller = set(m.group("aller").split(", "))
        for x in ingred:
            ingreds[x] += 1
        for cur in aller:
            allers[cur] = allers.get(cur, set(ingred)) & set(ingred)

    all_allers = set().union(*allers.values())
    if mode == 1:
        return sum([ingreds[x] for x in set(ingreds).difference(all_allers)])

    while max([len(x) for x in allers.values()]) > 1:
        for key in [x for x in allers if len(allers[x]) == 1]:
            for other in [x for x in allers if x != key]:
                allers[other] -= allers[key]

    allers = sorted([(x, list(y)[0]) for x, y in allers.items()])
    return ",".join([x[1] for x in allers])

def test(log):
    values = log.decode_values("""
        mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
        trh fvjkl sbzzf mxmxvkd (contains dairy)
        sqjhc fvjkl (contains soy)
        sqjhc mxmxvkd sbzzf (contains fish)
    """)

    log.test(calc(log, values, 1), 5)
    log.test(calc(log, values, 2), 'mxmxvkd,sqjhc,fvjkl')

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2020/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
