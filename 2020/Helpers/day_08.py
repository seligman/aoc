#!/usr/bin/env python

import re

def get_desc():
    return 8, 'Day 8: Handheld Halting'

def calc(log, values, mode):
    r = re.compile("^(?P<op>[a-z]{3}) (?P<val>[\\+\\-][0-9]+)$")

    for i in range(len(values)):
        temp = values[:]
        if mode == 2:
            if temp[i].startswith("nop"):
                temp[i] = "jmp" + temp[i][3:]
            elif temp[i].startswith("jmp"):
                temp[i] = "nop" + temp[i][3:]

        visited = set()
        pc = 0
        acc = 0

        while True:
            if pc in visited:
                if mode == 1:
                    return acc
                break
            if pc >= len(values):
                return acc
            cur = temp[pc]
            visited.add(pc)

            m = r.search(cur)
            op, val = m.group("op"), int(m.group("val"))
            if op == "nop":
                pass
            elif op == "acc":
                acc += val
            elif op == "jmp":
                pc += val - 1
            
            pc += 1

    return 0

def test(log):
    values = log.decode_values("""
        nop +0
        acc +1
        jmp +4
        acc +3
        jmp -3
        acc -99
        acc +1
        jmp -4
        acc +6
    """)

    log.test(calc(log, values, 1), 5)
    log.test(calc(log, values, 2), 8)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))
