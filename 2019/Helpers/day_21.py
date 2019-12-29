#!/usr/bin/env python

def get_desc():
    return 21, 'Day 21: Springdroid Adventure'


def calc(log, values, walk):
    from program import Program
    prog = Program.from_values(values, log)

    def sb(value, use=True):
        if use:
            for cur in value + "\n":
                prog.add_to_input(ord(cur))

    sb("NOT A J")
    sb("NOT B T")
    sb("AND H T", not walk)
    sb("OR T J")
    sb("NOT C T")
    sb("AND H T", not walk)
    sb("OR T J")
    sb("AND D J")

    sb("WALK" if walk else "RUN")

    prog.tick_till_end()

    output = [""]
    while len(prog.output) > 0:
        value = prog.get_output()
        if value > 128:
            return value
        else:
            if value == 10:
                output.append("")
            else:
                output[-1] += chr(value)

    for cur in output:
        log(cur)

    return "ERROR"


def test(log):
    return True


def run(log, values):
    log("Walk: " + str(calc(log, values, True)))
    log("Run: " + str(calc(log, values, False)))
