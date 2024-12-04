#!/usr/bin/env python3

import re

DAY_NUM = 18
DAY_DESC = 'Day 18: Operation Order'

def eval_ops(val1, op, val2):
    bail["last_eval"] = val1 + " " + op + " " + val2
    ret = ""
    if op == "+":
        ret = str(int(val1) + int(val2))
    elif op == "*":
        ret = str(int(val1) * int(val2))
    elif op == "tree":
        ret = str((int(val1) + int(val2)) // 2)
    else:
        raise Exception()
    bail["last_eval_result"] = ret
    return ret

precedence = None
bail = {
    "bail_after_ops": None,
    "in_paren": False,
    "last_eval": "",
    "last_eval_result": "",
    "last_eval_offset": 0,
}

def paren(value):
    if isinstance(value, list):
        value = " ".join(value)
    if bail["in_paren"] and (" " in value):
        return "(" + value + ")"
    else:
        return value

def eval_expr(value):
    off = 0
    if isinstance(value, type(re.match("",""))):
        off = value.span()[0] + 1
        value = value.group("expr")

    if bail["bail_after_ops"] is not None:
        if bail["bail_after_ops"] == 0:
            return paren(value)

    ops = []
    offs = []
    for m in re.finditer(r"([\d]+|\+|\*|tree)", value):
        ops.append(m.group(1))
        offs.append(off + m.span()[0])

    if precedence == 1:
        passes = [{"tree"}, {"+", "*"}]
    else:
        passes = [{"tree"}, {"+"}, {"*"}]

    for operators in passes:
        found = True
        while found:
            found = False
            for i in range(len(ops) - 1):
                if ops[i] in operators:
                    found = True

                    bail["last_eval_offset"] = offs[i - 1]
                    ops = ops[:i-1] + [eval_ops(ops[i - 1], ops[i], ops[i + 1])] + ops[i + 2:]
                    if bail["bail_after_ops"] is not None:
                        bail["bail_after_ops"] -= 1
                        if bail["bail_after_ops"] == 0:
                            return paren(ops)
                    break

    return ops[0]

def calc(log, values, mode, target=None, pad=0):
    global precedence
    precedence = mode

    ret = 0
    for cur in values:
        if target is not None:
            for x in range(len(cur)):
                target.append([x, cur[x], (0, 0, 0)])
            target.append(None)
            while True:
                old_len = len(cur)
                old_value = cur
                bail["bail_after_ops"] = 1
                while True:
                    before = cur
                    bail["in_paren"] = True
                    cur = re.sub(r"\((?P<expr>[^\(\)]+)\)", eval_expr, before)
                    bail["in_paren"] = False
                    if cur == before:
                        break
                cur = eval_expr(cur)
                if bail["bail_after_ops"] == 1:
                    break

                for x in range(len(bail["last_eval"])):
                    target.append([x + bail["last_eval_offset"], old_value[x + bail["last_eval_offset"]], (128, 128, 0)])
                target.append(None)
                for x in range(old_len):
                    target.append([x, ' ', (0, 0, 0)])
                final = False
                if " " not in cur:
                    final = True
                for x in range(len(cur)):
                    target.append([x, cur[x], (0, 0, 0)])
                target.append(None)
                if final:
                    if len(cur) < pad:
                        for x in range(pad):
                            target.append([x, cur[x] if x < len(cur) else ' ', (128, 128, 0)])
                        target.append(None)
                        cur = " " * pad + cur
                        cur = cur[-pad:]
                        for x in range(pad):
                            target.append([x, cur[x], (0, 0, 0)])
                        target.append(None)
                    return cur
        else:
            while True:
                before = cur
                bail["in_paren"] = True
                cur = re.sub(r"\((?P<expr>[^\(\)]+)\)", eval_expr, before)
                if cur == before:
                    break
        cur = eval_expr(cur)
        ret += int(cur)
    return ret

def other_draw(describe, values):
    if describe:
        return "Animate this"

    from dummylog import DummyLog
    targets = []
    rows = []
    for cur in values[:50]:
        rows.append(calc(DummyLog(), [cur], 2, target=[], pad=0))
    total = sum([int(x.strip()) for x in rows])
    pad = len(str(total))
    rows = []

    for cur in values[:50]:
        targets.append([])
        rows.append(calc(DummyLog(), [cur], 2, target=targets[-1], pad=pad))

    from grid import Grid
    disp = Grid(default = ' ')

    while True:
        updates = 0
        y = 0
        for target in targets:
            while len(target) > 0:
                updates += 1
                cur = target.pop(0)
                if cur is None:
                    break
                disp[cur[0], y] = [cur[1], cur[2]]
            y += 1
        if updates == 0:
            break
        disp.draw_grid(show_lines=False, default_color=(0,0,0), font_size=13, cell_size=(11,19), color_map={})

    while len(rows) >= 2:
        for x in range(pad):
            disp[x, 0][1] = (128, 128, 0)
            disp[x, 1][1] = (128, 128, 0)
        disp.draw_grid(show_lines=False, default_color=(0,0,0), font_size=13, cell_size=(11,19), color_map={})
        for x in range(pad):
            disp[x, 0][1] = (0, 0, 0)
            disp[x, 1][1] = (0, 0, 0)
        for x in range(pad):
            for y in disp.y_range():
                disp[x, y] = [' ', (0, 0, 0)]
        temp = str(int(rows[0].strip()) + int(rows[1].strip()))
        temp = " " * pad + temp
        temp = temp[-pad:]
        rows = [temp] + rows[2:]
        for y in range(len(rows)):
            for x in range(len(rows[y])):
                disp[x, y] = [rows[y][x], (0, 0, 0)]
        disp.draw_grid(show_lines=False, default_color=(0,0,0), font_size=13, cell_size=(11,19), color_map={})

    import subprocess
    import os
    cmd = [
        "ffmpeg", "-y",
        "-hide_banner",
        "-f", "image2",
        "-framerate", "10", 
        "-i", "frame_%05d.png", 
        "-c:v", "libx264", 
        "-profile:v", "main", 
        "-pix_fmt", "yuv420p", 
        "-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2",
        "-an", 
        "-movflags", "+faststart",
        os.path.join("animations", "animation_%02d.mp4" % (get_desc()[0],)),
    ]
    print("$ " + " ".join(cmd))
    subprocess.check_call(cmd)


def test(log):
    log.test(calc(log, ["1 + (2 * 3) + (4 * (5 + 6))"], 1), 51)
    log.test(calc(log, ["2 * 3 + (4 * 5)"], 1), 26)
    log.test(calc(log, ["5 + (8 * 3 + 9 + 3 * 4 * 3)"], 1), 437)
    log.test(calc(log, ["5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"], 1), 12240)
    log.test(calc(log, ["((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"], 1), 13632)

    log.test(calc(log, ["1 + (2 * 3) + (4 * (5 + 6))"], 2), 51)
    log.test(calc(log, ["2 * 3 + (4 * 5)"], 2), 46)
    log.test(calc(log, ["5 + (8 * 3 + 9 + 3 * 4 * 3)"], 2), 1445)
    log.test(calc(log, ["5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"], 2), 669060)
    log.test(calc(log, ["((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"], 2), 23340)

    log.test(calc(log, ["4 tree 8"], 2), 6)
    log.test(calc(log, ["4 tree 9"], 2), 6)
    log.test(calc(log, ["5 + 1 tree 3"], 2), 7)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2020/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
