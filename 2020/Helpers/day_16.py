#!/usr/bin/env python3

import re
from collections import defaultdict

def get_desc():
    return 16, 'Day 16: Ticket Translation'

def calc(log, values, mode):
    rules = []
    names = []
    valid_values = []
    invalid = 0

    for cur in values:
        m = re.search(r"^([a-z ]+): ([\d]+)-([\d]+) or ([\d]+)-([\d]+)", cur)
        if m is not None:
            rules.append([int(x) for x in m.groups()[1:]])
            names.append(m.groups()[0])

        m = re.search(r"^[\d,]+$", cur)
        if m is not None:
            cur = [int(x) for x in cur.split(",")]
            all_valid = True
            for x in cur:
                valid = False
                for rule in rules:
                    if x >= rule[0] and x <= rule[1]:
                        valid = True
                    if x >= rule[2] and x <= rule[3]:
                        valid = True
                if not valid:
                    invalid += x
                    all_valid = False

            if all_valid:
                valid_values.append(cur)

    if mode == 1:
        return invalid

    if mode == 2:
        possibles = {}
        for i in range(len(valid_values[0])):
            for j in range(len(rules)):
                name = names[j]
                rule = rules[j]
                all_valid = True
                for x in [z[i] for z in valid_values]:
                    valid = False
                    if x >= rule[0] and x <= rule[1]:
                        valid = True
                    if x >= rule[2] and x <= rule[3]:
                        valid = True
                    if not valid:
                        all_valid = False
                        break
                if all_valid:
                    if name not in possibles:
                        possibles[name] = set()
                    possibles[name].add(i)

        final = {}
        ticket = valid_values[0]

        while True:
            temp = {}
            for name, targets in possibles.items():
                for x in targets:
                    temp[x] = temp.get(x, []) + [name]

            if sum([len(x) for x in temp.values()]) == 0:
                break

            for val, targets in temp.items():
                if len(targets) == 1:
                    final[val] = targets[0]
                    possibles[targets[0]] = set()
    
        ret = 1
        for i in range(len(ticket)):
            if final[i].startswith("departure"):
                ret *= ticket[i]
        return ret

def test(log):
    values = log.decode_values("""
        class: 1-3 or 5-7
        row: 6-11 or 33-44
        seat: 13-40 or 45-50

        your ticket:
        7,1,14

        nearby tickets:
        7,3,47
        40,4,50
        55,2,20
        38,6,12
    """)

    log.test(calc(log, values, 1), 71)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))
