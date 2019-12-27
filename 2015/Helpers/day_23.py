#!/usr/bin/env python

def get_desc():
    return 23, 'Day 23: Opening the Turing Lock'


def calc(values, reg_a):
    offset = 0
    regs = {"a": reg_a, "b": 0}

    while True:
        if offset >= len(values):
            return regs["b"]

        ins = values[offset]
        if ins.startswith("hlf "):
            regs[ins[4:]] /= 2
            offset += 1
        elif ins.startswith("tpl "):
            regs[ins[4:]] *= 3
            offset += 1
        elif ins.startswith("inc "):
            regs[ins[4:]] += 1
            offset += 1
        elif ins.startswith("jmp "):
            offset += int(ins[4:])
        elif ins.startswith("jie "):
            if regs[ins[4:5]] % 2 == 0:
                offset += int(ins[6:])
            else:
                offset += 1
        elif ins.startswith("jio "):
            if regs[ins[4:5]] == 1:
                offset += int(ins[6:])
            else:
                offset += 1
        else:
            return regs["b"]


def test(log):
    values = [
        "inc b",
        "jio b, +2",
        "tpl b",
        "inc b",
    ]

    if calc(values, 0) == 2:
        return True
    else:
        return False


def run(log, values):
    log.show(calc(values, 0))
    log.show(calc(values, 1))
