#!/usr/bin/env python3

DAY_NUM = 21
DAY_DESC = 'Day 21: Monkey Math'

def oper_func(oper, a, b):
    if oper == "+":
        def helper(x): return (a(x) if callable(a) else a) + (b(x) if callable(b) else b)
        return helper
    elif oper == "*":
        def helper(x): return (a(x) if callable(a) else a) * (b(x) if callable(b) else b)
        return helper
    elif oper == "/":
        def helper(x): return (a(x) if callable(a) else a) // (b(x) if callable(b) else b)
        return helper
    elif oper == "-":
        def helper(x): return (a(x) if callable(a) else a) - (b(x) if callable(b) else b)
        return helper
    else:
        raise Exception()

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
        done["humn"] = lambda x: x

    while "root" not in done:
        for monkey, (a, oper, b) in todo.items():
            if a in done and b in done:
                if oper == "==":
                    done[monkey] = [done[a], done[b]]
                else:
                    if callable(done[a]) or callable(done[b]):
                        done[monkey] = oper_func(oper, done[a], done[b])
                    else:
                        done[monkey] = oper_func(oper, done[a], done[b])(0)
        todo = {x: y for x, y in todo.items() if x not in done}

    if mode == 2:
        check = 0
        inc = 1
        grow_mode = True
        a, b = done["root"]
        if callable(a): a, b = b, a

        too_low = b(0) < a
        while True:
            temp = b(check)
            if temp == a:
                while b(check-1) == a: check -= 1
                return check
            elif (too_low and temp < a) or (not too_low and temp > a):
                if grow_mode:
                    inc *= 2
                check += inc
            else:
                grow_mode = False
                check -= inc
                inc //= 2
    else:
        return done["root"]

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
            for dn in [[], ["Puzzles"], ["..", "Puzzles"]]:
                cur = os.path.join(*(dn + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!"); exit(1)
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
