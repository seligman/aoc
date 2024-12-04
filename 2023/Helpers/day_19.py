#!/usr/bin/env python3

DAY_NUM = 19
DAY_DESC = 'Day 19: Aplenty'

import re

def is_accepted(rules, val):
    step = "in"
    while True:
        if step == "A":
            return True
        elif step == "R":
            return False
        else:
            for rule in rules[step]:
                m = re.search("([a-z]+)([<>])([0-9]+):([a-z0-9A-Z]+)", rule)
                if m is not None:
                    var, op, target, dest = m.groups()
                    if op == ">":
                        if val[var] > int(target):
                            step = dest
                            break
                    elif op == "<":
                        if val[var] < int(target):
                            step = dest
                            break
                    else:
                        raise Exception()
                else:
                    step = rule
                    break

def calc(log, values, mode):
    import re

    rules = {}
    vals = []

    for row in values:
        if len(row) > 0:
            if row.startswith("{"):
                row = row.strip("{}")
                row = row.split(",")
                row = {x.split("=")[0]: int(x.split("=")[1]) for x in row}
                vals.append(row)
            else:
                row = row.split("{")
                rules[row[0]] = row[1].strip("}").split(",")

    ret = 0
    if mode == 1:
        for val in vals:
            if is_accepted(rules, val):
                ret += sum(val.values())
    else:
        step = "in"
        todo = [("in", [])]
        accepts = []
        while len(todo) > 0:
            step, limits = todo.pop(0)
            if step == "A":
                accepts.append(limits)
            elif step == "R":
                pass
            else:
                for rule in rules[step]:
                    m = re.search("([a-z]+)([<>])([0-9]+):([a-z0-9A-Z]+)", rule)
                    if m is not None:
                        var, op, target, dest = m.groups()
                        if op == ">":
                            todo.append((dest, limits[:] + [(var, ">", int(target))]))
                            limits += [(var, "<", int(target)+1)]
                        elif op == "<":
                            todo.append((dest, limits[:] + [(var, "<", int(target))]))
                            limits += [(var, ">", int(target)-1)]
                        else:
                            raise Exception()
                    else:
                        todo.append((rule, limits[:]))
        
        for accept in accepts:
            vals = {key: list(range(1, 4001)) for key in "xmas"}
            for var, op, val in accept:
                if op == ">":
                    vals[var] = [x for x in vals[var] if x > val]
                elif op == "<":
                    vals[var] = [x for x in vals[var] if x < val]
                else:
                    raise Exception()
        
            temp = 1
            for val in vals.values():
                temp *= len(val)
            ret += temp
        # ret *= len(vals)

    return ret

def test(log):
    values = log.decode_values("""
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
    """)

    log.test(calc(log, values, 1), '19114')
    log.test(calc(log, values, 2), '167409079868000')

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2023/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
