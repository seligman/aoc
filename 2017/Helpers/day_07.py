#!/usr/bin/env python3

import re
from collections import deque

DAY_NUM = 7
DAY_DESC = 'Day 7: Recursive Circus'

class Node:
    def __init__(self, value):
        m = re.search("(.*) \\(([0-9]+)\\)(| -> (.*))$", value)
        self.name = m.group(1)
        self.weight = int(m.group(2))
        self.children = []
        self.parent = None
        if m.group(4):
            self.children = m.group(4).split(", ")

    def get_weight(self, nodes):
        ret = self.weight
        for sub in self.children:
            ret += nodes[sub].get_weight(nodes)
        return ret

def calc(log, values, balance):
    nodes = {}
    for cur in values:
        temp = Node(cur)
        nodes[temp.name] = temp

    for key in nodes:
        for sub in nodes[key].children:
            nodes[sub].parent = key

    root_node = None

    for key in nodes:
        if nodes[key].parent is None:
            root_node = key

    if balance == 0:
        return root_node

    unbalanced = root_node
    change = None
    while True:
        if len(nodes[unbalanced].children) > 0:
            weights = {}
            seen = {}
            for cur in nodes[unbalanced].children:
                weights[cur] = nodes[cur].get_weight(nodes)
                if weights[cur] not in seen:
                    seen[weights[cur]] = 1
                else:
                    seen[weights[cur]] += 1
            if change is None:
                change = max(weights.values()) - min(weights.values())
            next_unbalanced = None
            for cur in weights:
                if seen[weights[cur]] == 1:
                    next_unbalanced = cur
            if next_unbalanced is None:
                return nodes[unbalanced].weight - change
            unbalanced = next_unbalanced
        else:
            break

    log(unbalanced)

    return None

def test(log):
    values = [
        "pbga (66)",
        "xhth (57)",
        "ebii (61)",
        "havc (66)",
        "ktlj (57)",
        "fwft (72) -> ktlj, cntj, xhth",
        "qoyq (66)",
        "padx (45) -> pbga, havc, qoyq",
        "tknk (41) -> ugml, padx, fwft",
        "jptl (61)",
        "ugml (68) -> gyxo, ebii, jptl",
        "gyxo (61)",
        "cntj (57)",
    ]

    if calc(log, values, 0) == "tknk":
        if calc(log, values, 1) == 60:
            return True
        else:
            return False
    else:
        return False

def run(log, values):
    log("Part 1: %s" % (calc(log, values, 0),))
    log("Part 2: %s" % (calc(log, values, 1),))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2017/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
