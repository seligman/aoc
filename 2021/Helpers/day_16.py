#!/usr/bin/env python3

DAY_NUM = 16
DAY_DESC = 'Day 16: Packet Decoder'

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

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in [[], ["Puzzles"], ["..", "Puzzles"]]:
                cur = os.path.join(*(dn + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!"); exit(1)
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
