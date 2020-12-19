#!/usr/bin/env python3

import re

def get_desc():
    return 19, 'Day 19: Monster Messages'

def calc(log, values, mode):
    rules = {}

    for cur in values:
        if ":" in cur:
            cur = cur.split(":")
            rules[cur[0]] = "( " + cur[1].replace('"', '').strip() + " )"

    if mode == 2:
        rules["8"] = "( 42 | 42 8 )"
        rules["11"] = "( 42 31 | 42 11 31 )"

    compiled = []
    for key in rules if mode == 1 else ["0"]:
        temp = rules[key]
        rule = temp.split(' ')
        bail = 0
        while True:
            found = False
            temp = rule
            rule = []
            for cur in temp:
                if cur in rules:
                    rule += rules[cur].split(' ')
                    found = True
                else:
                    rule.append(cur)
            bail += 1
            if mode == 1:
                if not found:
                    break
            else:
                if bail >= 30:
                    break
        rule = "".join(rule)
        rule = re.compile("^" + rule.replace(" ", "") + "$")
        compiled.append(rule)

    valid = set()
    for cur in values:
        if len(cur) > 0 and ":" not in cur:
            for rule in compiled:
                if rule.match(cur):
                    valid.add(cur)

    return len(valid)

def test(log):
    values = log.decode_values("""
        0: 4 1 5
        1: 2 3 | 3 2
        2: 4 4 | 5 5
        3: 4 5 | 5 4
        4: "a"
        5: "b"

        ababbb
        bababa
        abbbab
        aaabbb
        aaaabbb
    """)

    log.test(calc(log, values, 1), 2)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))
