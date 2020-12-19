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
        rules["8"] = "(?P<r8> 42 + )"
        rules["11"] = "(?P<r11> 42 + 31 + )"

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

    if mode == 2:
        r42 = "".join(decode(rules["42"].split(' ')))
        r31 = "".join(decode(rules["31"].split(' ')))
        r42 = re.compile("^" + r42.replace(" ", ""))
        r31 = re.compile(r31.replace(" ", "") + "$")

    count = 0
    for cur in [x for x in values if ":" not in x and len(x) > 0]:
        for rule in compiled:
            m = rule.search(cur)
            if m is not None:
                if mode == 1:
                    count += 1
                else:
                    temp = m.group("r8") + m.group("r11")
                    c42 = 0
                    c31 = 0
                    while r42.search(temp):
                        c42 += 1
                        temp = r42.sub("", temp)
                    while r31.search(temp):
                        c31 += 1
                        temp = r31.sub("", temp)
                    if c31 < c42:
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
