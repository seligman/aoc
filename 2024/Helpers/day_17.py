#!/usr/bin/env python3

DAY_NUM = 17
DAY_DESC = 'Day 17: Chronospatial Computer'

def calc(log, values, mode):
    a = int(values[0].split(": ")[1])
    b = int(values[1].split(": ")[1])
    c = int(values[2].split(": ")[1])
    prog = [int(x) for x in values[4].split(": ")[1].split(",")]

    def decode(a, b, c, val):
        if val <= 3: return val
        elif val == 4: return a
        elif val == 5: return b
        elif val == 6: return c
        else: raise Exception()

    def run_program(a, b, c, prog):
        ret = []
        i = 0
        while i < len(prog):
            next_i = i + 2
            opcode = prog[i]
            operand = prog[i+1]

            if opcode == 0:
                a = int(a / (2 ** decode(a, b, c, operand)))
            elif opcode == 1:
                b = b ^ operand
            elif opcode == 2:
                b = decode(a, b, c, operand) % 8
            elif opcode == 3:
                if a != 0:
                    next_i = operand
            elif opcode == 4:
                b = b ^ c
            elif opcode == 5:
                ret.append(decode(a, b, c, operand) % 8)
            elif opcode == 6:
                b = int(a / (2 ** decode(a, b, c, operand)))
            elif opcode == 7:
                c = int(a / (2 ** decode(a, b, c, operand)))
            i = next_i
        return ret

    if mode == 1:
        ret = run_program(a, b, c, prog)
        return ",".join(str(x) for x in ret)
    else:
        todo = [(prog, len(prog) - 1, 0)]
        while len(todo) > 0:
            prog, off, val = todo.pop(0)
            for cur in range(8):
                next_val = (val << 3) + cur
                if run_program(next_val, 0, 0, prog) == prog[off:]:
                    if off == 0:
                        return next_val
                    todo.append((prog, off - 1, next_val))

    return None

def test(log):
    values = log.decode_values("""
        Register A: 729
        Register B: 0
        Register C: 0

        Program: 0,1,5,4,3,0
    """)

    log.test(calc(log, values, 1), '4,6,3,5,6,3,5,2,1,0')

    values = log.decode_values("""
        Register A: 2024
        Register B: 0
        Register C: 0

        Program: 0,3,5,4,3,0
    """)

    log.test(calc(log, values, 2), '117440')

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2024/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
