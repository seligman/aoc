#!/usr/bin/env python3

DAY_NUM = 21
DAY_DESC = 'Day 21: Springdroid Adventure'

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
    log("Part 1: " + str(calc(log, values, True)))
    log("Part 2: " + str(calc(log, values, False)))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2019/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
