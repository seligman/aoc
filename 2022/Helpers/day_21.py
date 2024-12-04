#!/usr/bin/env python3

DAY_NUM = 21
DAY_DESC = 'Day 21: Monkey Math'

def solver(equation, show_work=None):
    a, oper, b = equation
    if isinstance(b, int):
        a, b = b, a

    def to_str(val):
        if isinstance(val, int) or isinstance(val, str):
            return str(val)
        else:
            return f"({to_str(val[0])} {val[1]} {to_str(val[2])})"

    while isinstance(b, list):
        if show_work is not None: show_work(to_str([a, oper, b]))
            
        if b[1] == "+":
            if isinstance(b[0], int):
                a -= b[0]
                b = b[2]
            else:
                a -= b[2]
                b = b[0]
        elif b[1] == "-":
            if isinstance(b[0], int):
                a = -(a - b[0])
                b = b[2]
            else:
                a = (a + b[2])
                b = b[0]
        elif b[1] == "*":
            if isinstance(b[0], int):
                a = a // b[0]
                b = b[2]
            else:
                a = a // b[2]
                b = b[0]
        elif b[1] == "/":
            if isinstance(b[0], int):
                a = a * b[0]
                b = b[2]
            else:
                a = a * b[2]
                b = b[0]

    if show_work is not None: show_work(to_str([a, oper, b]))

    return a

def builder(a, oper, b):
    if isinstance(a, int) and isinstance(b, int):
        if oper == "+": return a + b
        if oper == "-": return a - b
        if oper == "*": return a * b
        if oper == "/": return a // b
    return [a, oper, b]

def calc(log, values, mode):
    todo = {}
    done = {}

    for row in values:
        row = row.split(" ")
        monkey = row[0][:-1]
        if len(row) == 2:
            done[monkey] = int(row[1])
        else:
            todo[monkey] = row[1:]
    
    if mode == 2:
        todo["root"][1] = "=="
        done["humn"] = "x"

    while "root" not in done:
        for monkey, (a, oper, b) in todo.items():
            if a in done and b in done:
                done[monkey] = builder(done[a], oper, done[b])
        todo = {x: y for x, y in todo.items() if x not in done}

    if isinstance(done["root"], int):
        return done["root"]
    else:
        return solver(done['root'])

def test(log):
    values = log.decode_values("""
        root: pppw + sjmn
        dbpl: 5
        cczh: sllz + lgvd
        zczc: 2
        ptdq: humn - dvpt
        dvpt: 3
        lfqf: 4
        humn: 5
        ljgn: 2
        sjmn: drzm * dbpl
        sllz: 4
        pppw: cczh / lfqf
        lgvd: ljgn * ptdq
        drzm: hmdt - zczc
        hmdt: 32
    """)

    log.test(calc(log, values, 1), '152')
    log.test(calc(log, values, 2), '301')

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2022/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
