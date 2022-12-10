#!/usr/bin/env python3

import re
from collections import defaultdict

DAY_NUM = 19
DAY_DESC = 'Day 19: Monster Messages'

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
        rules["11"] = "( 42 + 31 + )"

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

    def count_matches(rule, value):
        ret = 0
        while rule.search(value):
            ret += 1
            value = rule.sub("", value)
        return ret

    count = 0
    for cur in [x for x in values if ":" not in x and len(x) > 0]:
        for rule in compiled:
            m = rule.search(cur)
            if m is not None:
                if mode == 1:
                    count += 1
                else:
                    if count_matches(r31, cur) < count_matches(r42, cur):
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
