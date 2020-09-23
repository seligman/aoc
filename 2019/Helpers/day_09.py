#!/usr/bin/env python

def get_desc():
    return 9, 'Day 9: Sensor Boost'


def calc(log, values, first_input):
    from program import Program

    ticker = [int(x) for x in values[0].split(",")]

    prog = Program(ticker, log)
    prog.add_to_input(first_input)
    prog.tick_till_end()

    return ",".join([str(x) for x in list(prog.output)[::-1]])


def test(log):
    values = log.decode_values("""
        109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99
    """)

    ret, expected = calc(log, values, 0), values[0]
    log("Test returned\n  '%s'\nExpected\n  '%s'" % (str(ret), str(expected)))
    if ret != expected:
        return False

    return True


def run(log, values):
    log("BOOST keycode: " + str(calc(log, values, 1)))
    log("Coordinates of the distress signal: " + str(calc(log, values, 2)))
