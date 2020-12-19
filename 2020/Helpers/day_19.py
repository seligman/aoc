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
        rules["8"] = "( 42 | 42 8 )"
        rules["11"] = "( 42 31 | 42 11 31 )"

    compiled = []
    for key in rules if mode == 1 else ["0"]:
        def decode(temp, used):
            ret = []
            for x in temp:
                if x in tail:
                    ret.append(tail[x])
                elif x in rules and used[x] < 5:
                    used2 = used.copy()
                    used2[x] += 1
                    ret += decode(rules[x].split(' '), used2)
                else:
                    ret.append(x)
            return ret

        rule = "".join(decode(rules[key].split(' '), defaultdict(int)))
        rule = rule.replace(' ', '')
        compiled.append(re.compile("^" + rule.replace(" ", "") + "$"))

    count = 0
    for cur in [x for x in values if ":" not in x and len(x) > 0]:
        if len([x for x in [x.match(cur) for x in compiled] if x is not None]) > 0:
            count += 1

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
