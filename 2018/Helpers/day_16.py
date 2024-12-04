#!/usr/bin/env python3

DAY_NUM = 16
DAY_DESC = 'Day 16: Chronal Classification'


def make_op(op):
    def make_op_internal(r, a, b, c):
        r[c] = op(r, a, b)
    return make_op_internal


op_addr = make_op(lambda r, a, b: r[a] + r[b])
op_addi = make_op(lambda r, a, b: r[a] + b)
op_mulr = make_op(lambda r, a, b: r[a] * r[b])
op_muli = make_op(lambda r, a, b: r[a] * b)
op_banr = make_op(lambda r, a, b: r[a] & r[b])
op_bani = make_op(lambda r, a, b: r[a] & b)
op_borr = make_op(lambda r, a, b: r[a] | r[b])
op_bori = make_op(lambda r, a, b: r[a] | b)
op_setr = make_op(lambda r, a, b: r[a])
op_seti = make_op(lambda r, a, b: a)
op_gtir = make_op(lambda r, a, b: 1 if (a > r[b]) else 0)
op_gtri = make_op(lambda r, a, b: 1 if (r[a] > b) else 0)
op_gtrr = make_op(lambda r, a, b: 1 if (r[a] > r[b]) else 0)
op_eqir = make_op(lambda r, a, b: 1 if (a == r[b]) else 0)
op_eqri = make_op(lambda r, a, b: 1 if (r[a] == b) else 0)
op_eqrr = make_op(lambda r, a, b: 1 if (r[a] == r[b]) else 0)


def calc(log, values):
    ops = [
        [op_addr], [op_addi],
        [op_mulr], [op_muli],
        [op_banr], [op_bani],
        [op_borr], [op_bori],
        [op_setr], [op_seti],
        [op_gtir], [op_gtri], [op_gtrr],
        [op_eqir], [op_eqri], [op_eqrr],
    ]

    for op in ops:
        op.append(set())

    matches = 0

    for i in range(len(values)):
        if values[i][0:9] == "Before: [":
            before = [int(x) for x in values[i][9:-1].split(",")]
            after = [int(x) for x in values[i + 2][9:-1].split(",")]
            vals = [int(x) for x in values[i + 1].split(" ")]
            is_like = 0
            for op in ops:
                r = [x for x in before]
                op[0](r, vals[1], vals[2], vals[3])
                if r == after:
                    is_like += 1
                    op[1].add(vals[0])

            if is_like >= 3:
                matches += 1

    while True:
        removed = False
        for op in ops:
            if removed:
                break
            if len(op[1]) == 1:
                to_remove = list(op[1])[0]
                for op_other in ops:
                    if op_other[0] != op[0]:
                        if to_remove in op_other[1]:
                            op_other[1].remove(to_remove)
                            removed = True
        if not removed:
            break

    lookup = {}
    for op in ops:
        lookup[list(op[1])[0]] = op[0]


    blanks = 0
    r = [0, 0, 0, 0]
    for i in range(len(values)):
        if len(values[i]) == 0:
            blanks += 1
        else:
            if blanks > 2:
                vals = [int(x) for x in values[i].split(" ")]
                lookup[vals[0]](r, vals[1], vals[2], vals[3])
            else:
                blanks = 0

    log("Final registers: " + ", ".join([str(x) for x in r]))

    return matches


def test(log):
    return True


def run(log, values):
    log(calc(log, values))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2018/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
