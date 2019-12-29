#!/usr/bin/env python

def get_desc():
    return 5, 'Day 5: Sunny with a Chance of Asteroids'


def calc(log, values, input_val):
    from program import Program

    prog = Program.from_values(values, log)
    prog.add_to_input(input_val)
    prog.tick_till_end()
    return prog.last_output


def test(log):
    values = log.decode_values("""
        1002,4,3,4,33
    """)

    ret, expected = calc(log, values, 1), None
    log("Test returned %s, expected %s" % (str(ret), str(expected)))
    if ret != expected:
        return False
    
    return True


def run(log, values):
    log("Diagnostic for 1: " + str(calc(log, values, 1)))
    log("Diagnostic for 5: " + str(calc(log, values, 5)))
