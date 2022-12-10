#!/usr/bin/env python3

DAY_NUM = 23
DAY_DESC = 'Day 23: Category Six'


def calc(log, values, use_nat=False, log_traffic=False):
    from program import Program

    progs = []
    for x in range(50):
        prog = Program.from_values(values, log)
        prog.add_to_input(x)
        prog.tick_till_end()
        prog.id = x
        progs.append(prog)

    nat = None
    last_nat_y = None
    passes = 0

    if log_traffic:
        import os
        if os.path.isfile("traffic.txt"):
            os.unlink("traffic.txt")

    while True:
        passes += 1
        idle_count = 0

        for prog in progs:
            if len(prog.input) == 0:
                prog.add_to_input(-1)
            prog.tick_till_end(allowed_reads=1)

        for prog in progs:
            if len(prog.output) == 0 and len(prog.input) == 0:
                idle_count += 1
            while len(prog.output) >= 3:
                dest, x, y = prog.get_output(to_get=3)
                if log_traffic:
                    with open("traffic.txt", "a") as f:
                        f.write("%d,%d,%d,%d,%d\n" % (passes, prog.id, dest, x, y))
                if dest == 255:
                    nat = (x, y)
                    if not use_nat:
                        return y
                else:
                    progs[dest].add_to_input((x, y))

        if idle_count == 50:
            progs[0].add_to_input(nat)
            if log_traffic:
                with open("traffic.txt", "a") as f:
                    f.write("%d,%d,%d,%d,%d\n" % (passes, 255, 0, nat[0], nat[1]))
            if last_nat_y is not None and last_nat_y == nat[1]:
                return nat[1]
            else:
                last_nat_y = nat[1]
            nat = None


def other_log(describe, values):
    if describe:
        return "Log network traffic"
    from dummylog import DummyLog
    calc(DummyLog(), values, use_nat=True, log_traffic=True)
    print("Done")


def test(log):
    return True


def run(log, values):
    log("First output to 255: " + str(calc(log, values)))
    log("First repeated NAT value: " + str(calc(log, values, use_nat=True)))

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
