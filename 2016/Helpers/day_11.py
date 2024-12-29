#!/usr/bin/env python3

import re
import itertools

DAY_NUM = 11
DAY_DESC = 'Day 11: Radioisotope Thermoelectric Generators'

def correct(floor):
    if len(floor) == 0:
        return True
    temp = set(x for x in floor if -x not in floor)
    if len(temp) == 0:
        return True
    if min(temp) < 0 and max(temp) > 0:
        return False
    return True    

def copy(val):
    return [x.copy() for x in val]

def as_key(val, cost, floor):
    ret = [floor]
    for cur in val:
        ret.append(12345)
        ret += list(sorted(cur))
    return tuple(ret)

def calc(values, extra=None):
    r = re.compile("The (.*) floor contains (.*)\\.")

    floors = []
    ids = {}
    
    for cur in values:
        floors.append([])
        m = r.search(cur)
        cur = m.group(2)
        cur = cur.replace(", and", ",")
        cur = cur.replace(" and", ",")
        if cur == "nothing relevant":
            cur = ""
        cur = cur.split(",")
        if len(floors) == 1 and extra is not None:
            cur += extra
        for sub in cur:
            sub = sub.strip()
            if len(sub) > 0:
                negate = 1
                if "-compatible microchip" in sub:
                    negate = -1
                sub = sub.replace("-compatible microchip", "")
                sub = sub.replace(" generator", "")
                if sub not in ids:
                    ids[sub] = len(ids) + 1
                floors[-1].append(ids[sub] * negate)

    start_cost = 0
    for i in range(len(floors)):
        temp = floors[i]
        before = len(temp)
        temp = [x for x in temp if -x not in temp]
        if i == 0 and len(temp) == 0:
            temp = [floors[i][0], -floors[i][0]]
        after = len(temp)
        start_cost += ((before - after) // 2) * {0: 12, 1: 8, 2: 4, 3: 0}[i]
        floors[i] = set(temp)

    todo = [{"cost": start_cost, "floor": 0, "floors": copy(floors)}]
    seen = set()
    while len(todo) > 0:
        todo.sort(key=lambda x: (x['cost']))
        cur = todo.pop(0)
        key = as_key(cur["floors"], cur["cost"], cur["floor"])
        if key not in seen:
            seen.add(key)
            if cur["floor"] == 3:
                if len(cur["floors"][1]) == 0 and len(cur["floors"][2]) == 0 and len(cur["floors"][0]) == 0:
                    return cur["cost"]
            for key in list(itertools.combinations(cur["floors"][cur["floor"]], 1)) + list(itertools.combinations(cur["floors"][cur["floor"]], 2)):
                floors = copy(cur["floors"])
                floors[cur["floor"]] -= set(key)
                if correct(floors[cur["floor"]]):
                    for other in [cur["floor"] - 1, cur["floor"] + 1]:
                        if other >= 0 and other < len(floors):
                            floors = copy(cur["floors"])
                            floors[cur["floor"]] -= set(key)
                            floors[other] |= set(key)
                            if correct(floors[other]):
                                todo.append({"cost": cur["cost"] + 1, "floor": other, "floors": floors})

def test(log):
    values = [
        "The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.",
        "The second floor contains a hydrogen generator.",
        "The third floor contains a lithium generator.",
        "The fourth floor contains nothing relevant.",
    ]

    log(calc(values))
    if calc(values) == 11:
        return True
    else:
        return False

def run(log, values):
    log("Part 1: %d" % (calc(values),))
    extra = [
        "an elerium generator",
        "an elerium-compatible microchip",
        "a dilithium generator",
        "a dilithium-compatible microchip",
    ]
    log("Part 2: %d" % (calc(values, extra),))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2016/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
