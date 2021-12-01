#!/usr/bin/env python3

def get_desc():
    return 1, 'Day 1: Sonar Sweep'

def calc(log, values, mode):
    last = None
    ret = 0
    stack = []
    mode = {1: 1, 2: 3}[mode]
    for cur in values:
        stack.append(int(cur))
        stack = stack[-mode:]
        if len(stack) == mode:
            cur = sum(stack)
            if last and cur > last:
                ret += 1
            last = cur
    return ret

def test(log):
    values = log.decode_values("""
        199
        200
        208
        210
        200
        207
        240
        269
        260
        263    
    """)

    log.test(calc(log, values, 1), 7)
    log.test(calc(log, values, 2), 5)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))
