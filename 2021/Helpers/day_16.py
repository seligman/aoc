#!/usr/bin/env python3

import math

def get_desc():
    return 16, 'Day 16: Packet Decoder'

def calc(log, values, mode, print_formula=False):
    from program import Program
    program = Program(values, print_formula=print_formula)
    program.run()

    if print_formula:
        log("".join(program.formula))

    if mode == 1:
        return program.version_sum
    else:
        return program.result

def other_show_formula(describe, values):
    if describe:
        return "Show the formula used"
    from dummylog import DummyLog
    calc(DummyLog(), values, 2, print_formula=True)

def test(log):
    log.test(calc(log, ["620080001611562C8802118E34"], 1), 12)
    log.test(calc(log, ["C200B40A82"], 2), 3)
    log.test(calc(log, ["04005AC33890"], 2), 54)
    log.test(calc(log, ["880086C3E88112"], 2), 7)
    log.test(calc(log, ["CE00C43D881120"], 2), 9)
    log.test(calc(log, ["D8005AC2A8F0"], 2), 1)
    log.test(calc(log, ["F600BC2D8F"], 2), 0)
    log.test(calc(log, ["9C005AC2F8F0"], 2), 0)
    log.test(calc(log, ["9C0141080250320F1802104A08"], 2), 1)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))
