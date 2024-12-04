#!/usr/bin/env python3

DAY_NUM = 5
DAY_DESC = 'Day 5: Sunny with a Chance of Asteroids'


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
