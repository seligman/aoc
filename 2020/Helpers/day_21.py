#!/usr/bin/env python3

import re
from collections import defaultdict

def get_desc():
    return 21, 'Day 21: Allergen Assessment'

def calc(log, values, mode):
    r = re.compile(r"^(?P<ingred>.*) \(contains (?P<aller>.*)\)$")

    allers = {}
    ingreds = defaultdict(int)

    for row in values:
        m = r.search(row)
        if m is not None:
            aller = set(m.group("aller").split(", "))
            ingred = m.group("ingred").split(" ")
            for x in ingred:
                ingreds[x] += 1
            for cur in aller:
                if cur in allers:
                    allers[cur] &= set(ingred)
                else:
                    allers[cur] = set(ingred)
        else:
            for x in row.split(" "):
                ingreds[x] += 1
    

    all_allers = set().union(*allers.values())
    if mode == 1:
        return sum([ingreds[x] for x in set(ingreds).difference(all_allers)])

    while max([len(x) for x in allers.values()]) > 1:
        for key, value in allers.items():
            if len(value) == 1:
                for other, _value2 in allers.items():
                    if key != other:
                        allers[other] -= value

    allers = [(x, list(y)[0]) for x, y in allers.items()]
    allers.sort()
    allers = [x[1] for x in allers]

    return ",".join(allers)

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
