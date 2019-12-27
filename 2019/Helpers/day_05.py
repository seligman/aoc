#!/usr/bin/env python

def get_desc():
    return 5, 'Day 5: Sunny with a Chance of Asteroids'


def calc(log, values, replace_1=None, replace_2=None):
    from program import Program
    ret = []
    for val in [1, 5]:
        ticker = [int(x) for x in values[0].split(",")]
        prog = Program(ticker, log)
        prog.add_to_input(val)
        while prog.tick():
            pass
        ret.append(prog.last_output)
    return tuple(ret)


def test(log):
    values = log.decode_values("""
        1002,4,3,4,33
    """)

    ret, expected = calc(log, values), (None, None)
    log.show("Test returned %s, expected %s" % (str(ret), str(expected)))
    if ret != expected:
        return False
    
    return True


def run(log, values):
    log.show(calc(log, values))
