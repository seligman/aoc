#!/usr/bin/env python3

import re
import json

DAY_NUM = 7
DAY_DESC = 'Day 7: Some Assembly Required'


def calc(target, values, initial):
    final = {}
    rules = {}

    for cur in values:
        cur = cur.split(' -> ')
        if cur[1] in rules:
            raise Exception()
        rules[cur[1]] = cur[0]

    if initial is not None:
        for key in initial:
            value = initial[key]
            final[key] = value
            if key in rules:
                del rules[key]

    re_rule = re.compile("([0-9]+|[a-z]+) (AND|OR|LSHIFT|RSHIFT) ([0-9]+|[a-z]+)")
    re_rule_not = re.compile("(NOT) ([0-9]+|[a-z]+)")
    re_num = re.compile("^[0-9]+$")

    def decode(value):
        temp = re_num.search(value)
        if temp:
            return int(value)
        else:
            return final.get(value, None)

    bail = 1000

    while target not in final:
        bail -= 1
        if bail == 0:
            break
        for rule_dest in list(rules):
            found = False
            rule = rules[rule_dest]
            if not found:
                m = re_rule.search(rule)
                if m:
                    found = True
                    a = decode(m.group(1))
                    b = decode(m.group(3))
                    if a is not None and b is not None:
                        if m.group(2) == "AND":
                            final[rule_dest] = a & b
                        elif m.group(2) == "OR":
                            final[rule_dest] = a | b
                        elif m.group(2) == "LSHIFT":
                            final[rule_dest] = (a << b) & 65535
                        elif m.group(2) == "RSHIFT":
                            final[rule_dest] = a >> b
                        else:
                            raise Exception()
                        del rules[rule_dest]
            if not found:
                m = re_rule_not.search(rule)
                if m:
                    found = True
                    a = decode(m.group(2))
                    if a is not None:
                        final[rule_dest] = a ^ 65535
                        del rules[rule_dest]

            if not found:
                a = decode(rule)
                if a is not None:
                    found = True
                    final[rule_dest] = a
                    del rules[rule_dest]

    return final[target]


def test(log):
    values = [
        "123 -> x",
        "456 -> y",
        "x AND y -> d",
        "x OR y -> e",
        "x LSHIFT 2 -> f",
        "y RSHIFT 2 -> g",
        "NOT x -> h",
        "NOT y -> i",
    ]

    if calc("d", values, None) == 72:
        return True
    else:
        return False


def run(log, values):
    log(calc("a", values, None))
    log(calc("a", values, {"b": 3176}))

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
