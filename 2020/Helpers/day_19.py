#!/usr/bin/env python3

import re
from collections import defaultdict

def get_desc():
    return 19, 'Day 19: Monster Messages'

def calc(log, values, mode):
    rules = {}
    tail = {}

    for cur in values:
        if ":" in cur:
            cur = cur.split(":")
            if '"' in cur[1]:
                tail[cur[0]] = cur[1].replace('"', '').strip()
            else:
                rules[cur[0]] = "( " + cur[1].strip() + " )"

    if mode == 2:
        rules["8"] = "( 42 + )"
        temp = []
        for i in range(1, 10):
            temp.append(f"42 {{{i}}} 31 {{{i}}}")
        rules["11"] = "( " + " | ".join(temp) + " )"

    compiled = []
    for key in rules if mode == 1 else ["0"]:
        def decode(temp):
            ret = []
            for x in temp:
                if x in tail:
                    ret.append(tail[x])
                elif x in rules:
                    ret += decode(rules[x].split(' '))
                else:
                    ret.append(x)
            return ret

        rule = "".join(decode(rules[key].split(' ')))
        compiled.append(re.compile("^" + rule.replace(" ", "") + "$"))

    count = 0
    for cur in [x for x in values if ":" not in x and len(x) > 0]:
        for rule in compiled:
            if rule.search(cur) is not None:
                count += 1
                break
    return count

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
