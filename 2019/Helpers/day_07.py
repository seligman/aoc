#!/usr/bin/env python

def get_desc():
    return 7, 'Day 7: Amplification Circuit'


def calc(log, values, feedback, debug=False):
    from program import Program
    import itertools

    ticker = [int(x) for x in values[0].split(",")]
    max_output = 0
    best_perm = None
    best_frames = None

    for cur in itertools.permutations([5, 6, 7, 8, 9] if feedback else [0, 1, 2, 3, 4]):
        progs = []
        first = True
        for x in cur:
            prog = Program(ticker, log)
            if first:
                first = False
                if debug:
                    prog.save_frames()
            prog.add_to_input(x)
            if len(progs) > 0:
                prog.hook_up_output(progs[-1])
            progs.append(prog)

        progs[0].hook_up_output(progs[-1])
        progs[0].add_to_input(0)

        while progs[4].flag_running:
            for prog in progs:
                prog.tick_till_end()

        if progs[4].last_output > max_output:
            max_output = progs[4].last_output
            best_perm = cur
            best_frames = progs[0].frames

    if debug:
        log(best_perm)
        states = {}
        for cur in best_frames:
            if cur[0] not in {"input", "output"}:
                for key in cur[1]:
                    if key not in states:
                        states[key] = set()

        for cur in best_frames:
            if cur[0] not in {"input", "output"}:
                for key in states:
                    states[key].add(cur[1].get(key, None))

        changes = []
        for cur in sorted(states):
            if len(states[cur]) > 1:
                changes.append(cur)

        class SaveLine:
            def __init__(self):
                self.last = ""
            def show(self, value):
                self.last = value

        s = SaveLine()
        for cur in best_frames:
            if cur[0] not in {"input", "output"}:
                row = []
                for x in changes:
                    row.append("%d:%d" % (x, cur[1].get(x, None)))
                Program.debug_line(s, ticker, cur[0])
                print("%-75s -- %s" % (s.last, ", ".join(row)))
            else:
                if cur[0] == "input":
                    print("%sProvided input of %d" % (" " * 31, cur[1]))
                else:
                    print("%sGot output of %d" % (" " * 31, cur[1]))

    return max_output


def test(log):
    values = log.decode_values("""
        3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0
    """)

    ret, expected = calc(log, values, False), 43210
    log("Test returned %s, expected %s" % (str(ret), str(expected)))
    if ret != expected:
        return False

    values = log.decode_values("""
        3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5
    """)

    ret, expected = calc(log, values, True), 139629729
    log("Test returned %s, expected %s" % (str(ret), str(expected)))
    if ret != expected:
        return False

    return True


def run(log, values):
    log("Highest signal: " + str(calc(log, values, False)))
    log("Highest signal, with feedback: " + str(calc(log, values, True)))


def other_debug(describe, values):
    if describe:
        return "Debug mode on the second part"

    from dummylog import DummyLog
    calc(DummyLog(), values, True, debug=True)
    