#!/usr/bin/env python3

DAY_NUM = 21
DAY_DESC = 'Day 21: Monkey Math'

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
        done["humn"] = "XX"

        while "root" not in done:
            to_del = set()
            for monkey, exp in todo.items():
                if exp[0] in done and exp[2] in done:
                    if exp[1] == "+":
                        done[monkey] = f"({done[exp[0]]} + {done[exp[2]]})"
                    elif exp[1] == "-":
                        done[monkey] = f"({done[exp[0]]} - {done[exp[2]]})"
                    elif exp[1] == "/":
                        done[monkey] = f"({done[exp[0]]} // {done[exp[2]]})"
                    elif exp[1] == "*":
                        done[monkey] = f"({done[exp[0]]} * {done[exp[2]]})"
                    elif exp[1] == "==":
                        done[monkey] = f"{done[exp[0]]} == {done[exp[2]]}"
                    else:
                        raise Exception
                    to_del.add(monkey)
            todo = {x: y for x, y in todo.items() if x not in to_del}
        
        check = 0
        inc = 1 << 30
        a, b = done["root"].split("==")
        if "XX" in a:
            a, b = b, a
        a = eval(a)
        while True:
            temp = eval(b.replace("XX", str(check)))
            if temp == a:
                while eval(b.replace("XX", str(check-1))) == a:
                    check -= 1
                return check
            elif temp > a:
                check += inc
            else:
                check -= inc
                inc //= 2
    else:
        while "root" not in done:
            to_del = set()
            for monkey, exp in todo.items():
                if exp[0] in done and exp[2] in done:
                    if exp[1] == "+":
                        done[monkey] = done[exp[0]] + done[exp[2]]
                    elif exp[1] == "-":
                        done[monkey] = done[exp[0]] - done[exp[2]]
                    elif exp[1] == "/":
                        done[monkey] = done[exp[0]] // done[exp[2]]
                    elif exp[1] == "*":
                        done[monkey] = done[exp[0]] * done[exp[2]]
                    else:
                        raise Exception
                    to_del.add(monkey)
            todo = {x: y for x, y in todo.items() if x not in to_del}
    
        return done["root"]
        
    # TODO: Delete or use these
    # from parsers import get_ints, get_floats
    # from grid import Grid, Point
    # from program import Program
    # grid = Grid.from_text(values)
    # program = Program(values)

    # TODO
    return 0

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
    # log.test(calc(log, values, 2), '301')

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
