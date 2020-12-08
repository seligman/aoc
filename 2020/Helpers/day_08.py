#!/usr/bin/env python

def get_desc():
    return 8, 'Day 8: Handheld Halting'

def calc(log, values, mode, debug=False):
    from program import Program
    if mode == 1:
        prog = Program(values, log if debug else None)
        while not prog.seen_pc():
            prog.step()
        return prog.acc
    else:
        prog = Program(values)
        swap = {"jmp": "nop", "nop": "jmp"}
        to_test = []
        for i in range(len(values)):
            if prog.instructions[i].op in swap:
                to_test.append(i)
        
        for i in to_test:
            prog = Program(values)
            prog.instructions[i].op = swap[prog.instructions[i].op]
            hit_end = True
            while prog.step():
                if prog.seen_pc():
                    hit_end = False
                    break
            if hit_end:
                return prog.acc

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

    log.test(calc(log, values, 1, True), 5)
    log.test(calc(log, values, 2), 8)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))
