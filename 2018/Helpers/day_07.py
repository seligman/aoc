#!/usr/bin/env python3

import re

DAY_NUM = 7
DAY_DESC = 'Day 7: The Sum of Its Parts'


def get_requires(order):
    requires = {}
    for a, b in order:
        for cur in (a, b):
            if cur not in requires:
                requires[cur] = set()
        requires[b].add(a)

    return requires


def calc(log, values, workers, time_pad):
    r = re.compile("Step (.) must be finished before step (.) can begin.")
    order = []
    for cur in values:
        m = r.search(cur)
        if m:
            order.append(m.groups())

    requires = get_requires(order)
    ret = ""
    while len(requires) > 0:
        for cur in sorted(requires):
            if len(requires[cur]) == 0:
                ret += cur
                del requires[cur]
                for value in requires.values():
                    if cur in value:
                        value.remove(cur)
                break

    requires = get_requires(order)

    procs = []
    for _ in range(workers):
        procs.append({
            "working": None,
            "left": 0,
        })

    tick = -1
    in_progress = set()
    while len(requires) > 0:
        tick += 1
        for proc in procs:
            if proc["working"] is not None:
                proc["left"] -= 1
                if proc["left"] == 0:
                    cur = proc["working"]
                    proc["working"] = None
                    del requires[cur]
                    for value in requires.values():
                        if cur in value:
                            value.remove(cur)

        for proc in procs:
            if proc["working"] is None:
                for cur in sorted(requires):
                    if (cur not in in_progress) and (len(requires[cur]) == 0):
                        proc["working"] = cur
                        in_progress.add(cur)
                        proc["left"] = (ord(cur) - ord("A") + 1) + time_pad
                        break

    log("It took %d seconds for the workers to finish" % (tick,))

    return ret


def test(log):
    values = [
        "Step C must be finished before step A can begin.",
        "Step C must be finished before step F can begin.",
        "Step A must be finished before step B can begin.",
        "Step A must be finished before step D can begin.",
        "Step B must be finished before step E can begin.",
        "Step D must be finished before step E can begin.",
        "Step F must be finished before step E can begin.",
    ]

    if calc(log, values, 2, 0) == "CABDFE":
        return True
    else:
        return False


def run(log, values):
    log(calc(log, values, 5, 60))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in [[], ["Puzzles"], ["..", "Puzzles"]]:
                cur = os.path.join(*(dn + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!"); exit(1)
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
