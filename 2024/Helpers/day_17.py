#!/usr/bin/env python3

DAY_NUM = 17
DAY_DESC = 'Day 17: Chronospatial Computer'

from collections import deque

def other_draw(describe, values):
    if describe:
        return "Draw this"
    from dummylog import DummyLog
    import animate
    animate.prep()
    calc(DummyLog(), values, 2, draw=True)
    animate.create_mp4(DAY_NUM, rate=15, final_secs=5)

def calc(log, values, mode, draw=False):
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

    def run_program(a, b, c, prog, history=None):
        ret = []
        i = 0
        step = 0
        while i < len(prog):
            step += 1
            next_i = i + 2
            opcode = prog[i]
            operand = prog[i+1]

            if history is not None:
                op_name = ["adv", "bxl", "bst", "jnz", "bxc", "out", "bdv", "cdv"]
                history.append(f"#{step:03d} IP={i:04d}, Op={opcode} {op_name[opcode]}, Operand={operand}, A={a:15d}, B={b:15d}, C={c:15d}")

            if opcode == 0: # adv
                a = a // (1 << decode(a, b, c, operand))
            elif opcode == 1: # bxl
                b = b ^ operand
            elif opcode == 2: # bst
                b = decode(a, b, c, operand) % 8
            elif opcode == 3: # jnz
                if a != 0:
                    next_i = operand
            elif opcode == 4: # bxc
                b = b ^ c
            elif opcode == 5: # out
                ret.append(decode(a, b, c, operand) % 8)
            elif opcode == 6: # bdv
                b = a // (1 << decode(a, b, c, operand))
            elif opcode == 7: # cdv
                c = a // (1 << decode(a, b, c, operand))
            i = next_i
        return ret

    if draw:
        from grid import Grid
        grid = Grid()
        grid[0, 0] = "."
        grid[100, 0] = "."
        def dump_grid(rows):
            if len(rows) > 30:
                rows = rows[:25] + [" . . . . ."] + rows[-4:]
            grid.save_frame(rows)

    if mode == 1:
        ret = run_program(a, b, c, prog)
        return ",".join(str(x) for x in ret)
    else:
        todo = deque([(prog, len(prog) - 1, 0, True, [])])
        while len(todo) > 0:
            prog, off, val, calc, added = todo.popleft()
            if calc:
                for cur in range(8):
                    next_val = (val << 3) + cur
                    if draw:
                        history = ["Program: " + ", ".join(str(x) for x in prog)]
                        temp = '.'.join(f"{x}" for x in (added + [cur])[::-1])
                        history.append(f"Initial A = {temp}  <- or ->  {next_val}")
                    else:
                        history = None
                    result = run_program(next_val, 0, 0, prog, history=history)
                    if draw:
                        temp = [str(x) for x in result]
                        while len(temp) < len(prog):
                            temp.insert(0, " ")
                        history.append(" Result: " + ", ".join(temp))
                    if result == prog[off:]:
                        if draw:
                            history.append("Found quine!" if off == 0 else "Partial match of quine!")
                            dump_grid(history)
                        if off == 0:
                            if draw:
                                grid.ease_frames(rate=15, secs=30)
                                grid.draw_frames(show_lines=False)
                            return next_val
                        todo.append((prog, off - 1, next_val, True, added + [cur]))
                    else:
                        if draw:
                            history.append("ERROR: Mismatch")
                            dump_grid(history)
                        todo.append((prog, off - 1, next_val, False, added + [cur]))

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
