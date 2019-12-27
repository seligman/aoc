#!/usr/bin/env python

import re
from collections import deque

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


def get_desc():
    return 7, 'Day 7: Recursive Circus'


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

    log.show(unbalanced)

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
    log.show(calc(log, values, 0))
    log.show(calc(log, values, 1))
