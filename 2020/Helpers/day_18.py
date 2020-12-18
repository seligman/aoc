#!/usr/bin/env python3

import re

def get_desc():
    return 18, 'Day 18: Operation Order'

def eval_ops(val1, op, val2):
    if op == "+":
        return str(int(val1) + int(val2))
    if op == "*":
        return str(int(val1) * int(val2))
    raise Exception()

precedence = None
def eval_expr(value):
    if isinstance(value, re.Match):
        value = value.group("expr")

    ops = []
    for m in re.finditer(r"([\d]+|\+|\*)", value):
        ops.append(m.group(1))

    if precedence == 1:
        passes = [{"+", "*"}]
    else:
        passes = [{"+"}, {"*"}]

    for operators in passes:
        found = True
        while found:
            found = False
            for i in range(len(ops) - 1):
                if ops[i] in operators:
                    found = True
                    ops = ops[:i-1] + [eval_ops(ops[i - 1], ops[i], ops[i + 1])] + ops[i + 2:]
                    break

    return ops[0]

def calc(log, values, mode):
    global precedence
    precedence = mode

    ret = 0
    for cur in values:
        while True:
            before = cur
            cur = re.sub(r"\((?P<expr>[^\(\)]+)\)", eval_expr, before)
            if cur == before:
                break
        cur = eval_expr(cur)
        ret += int(cur)
    return ret

def test(log):
    log.test(calc(log, ["1 + (2 * 3) + (4 * (5 + 6))"], 1), 51)
    log.test(calc(log, ["2 * 3 + (4 * 5)"], 1), 26)
    log.test(calc(log, ["5 + (8 * 3 + 9 + 3 * 4 * 3)"], 1), 437)
    log.test(calc(log, ["5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"], 1), 12240)
    log.test(calc(log, ["((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"], 1), 13632)

    log.test(calc(log, ["1 + (2 * 3) + (4 * (5 + 6))"], 2), 51)
    log.test(calc(log, ["2 * 3 + (4 * 5)"], 2), 46)
    log.test(calc(log, ["5 + (8 * 3 + 9 + 3 * 4 * 3)"], 2), 1445)
    log.test(calc(log, ["5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"], 2), 669060)
    log.test(calc(log, ["((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"], 2), 23340)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))
