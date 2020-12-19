#!/usr/bin/env python3

import re

def get_desc():
    return 19, 'Day 19: Monster Messages'

def calc(log, values, mode):
    rules = {}
    tail = set()

    for cur in values:
        if ":" in cur:
            cur = cur.split(":")
            rules[cur[0]] = "( " + cur[1].replace('"', '').strip() + " )"
            if '"' in cur[1]:
                tail.add(cur[0])

    if mode == 2:
        rules["8"] = "( 42 | 42 8 )"
        rules["11"] = "( 42 31 | 42 11 31 )"

    compiled = []
    for key in rules if mode == 1 else ["0"]:
        temp = rules[key]
        temp = temp.split(' ')

        def decode(temp, used):
            ret = []
            for x in temp:
                if x in rules and (used.get(x, 0) < 10 not in used or x in tail):
                    used2 = used.copy()
                    used2[x] = used2.get(x, 0) + 1
                    ret += decode(rules[x].split(' '), used2)
                else:
                    if x in rules:
                        ret.append(rules[x])
                    else:
                        ret.append(x)
            return ret

        rule = "".join(decode(temp, {}))
        rule = rule.replace(' ', '')
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
