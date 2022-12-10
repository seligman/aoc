#!/usr/bin/env python3

import re

DAY_NUM = 19
DAY_DESC = 'Day 19: Go With The Flow'


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


def get_ops():
    return {
        "addr": op_addr, "addi": op_addi,
        "mulr": op_mulr, "muli": op_muli,
        "banr": op_banr, "bani": op_bani,
        "borr": op_borr, "bori": op_bori,
        "setr": op_setr, "seti": op_seti,
        "gtir": op_gtir, "gtri": op_gtri, "gtrr": op_gtrr,
        "eqir": op_eqir, "eqri": op_eqri, "eqrr": op_eqrr,
    }

def calc(values, start_r1, test):
    ops = get_ops()
    r = [start_r1, 0, 0, 0, 0, 0]
    ip_register = None
    ip = 0

    if values[0].startswith("#ip "):
        ip_register = int(values[0][4:])
    values = [x for x in values if x[0] != "#"]

    for i in range(len(values)):
        temp = values[i].split(' ')
        values[i] = (ops[temp[0]], int(temp[1]), int(temp[2]), int(temp[3]))

    max_ip = len(values)
    while True:
        if ip >= max_ip:
            break
        if ip_register is not None:
            r[ip_register] = ip

            if ip == 1 and not test:
                # Skip to the end, this is just calculating factors
                target = r[5]
                factors = set()
                for cur in range(1, int(target ** 0.5) + 1):
                    if target % cur == 0:
                        factors.add(cur)
                        factors.add(target // cur)
                r[0] = sum(factors)
                break

        cur = values[ip]
        cur[0](r, cur[1], cur[2], cur[3])

        if ip_register is not None:
            ip = r[ip_register]
        ip += 1

    return r[0]


def test(log):
    values = [
        "#ip 0",
        "seti 5 0 1",
        "seti 6 0 2",
        "addi 0 1 0",
        "addr 1 2 3",
        "setr 1 0 0",
        "seti 8 0 4",
        "seti 9 0 5",
    ]

    if calc(values, 0, True) == 6:
        return True
    else:
        return False


def run(log, values):
    log.show(calc(values, 0, False))
    log.show(calc(values, 1, False))


def get_op_to_str():
    return {
        "addr": "r[c] = r[a] + r[b]", 
        "addi": "r[c] = r[a] + b", 
        "mulr": "r[c] = r[a] * r[b]", 
        "muli": "r[c] = r[a] * b", 
        "banr": "r[c] = r[a] & r[b]", 
        "bani": "r[c] = r[a] & b", 
        "borr": "r[c] = r[a] | r[b]", 
        "bori": "r[c] = r[a] | b", 
        "setr": "r[c] = r[a]", 
        "seti": "r[c] = a", 
        "gtir": "r[c] = (a > r[b]) ? 1 : 0", 
        "gtri": "r[c] = (r[a] > b) ? 1 : 0", 
        "gtrr": "r[c] = (r[a] > r[b]) ? 1 : 0", 
        "eqir": "r[c] = (a == r[b]) ? 1 : 0", 
        "eqri": "r[c] = (r[a] == b) ? 1 : 0", 
        "eqrr": "r[c] = (r[a] == r[b]) ? 1 : 0", 
    }


def decompile(instruction_line, ip_register, line_no, total_lines):
    vals = instruction_line.split(' ')

    to_str = get_op_to_str()
    temp = to_str[vals[0]]
    temp = temp.replace("a", vals[1])
    temp = temp.replace("b", vals[2])
    temp = temp.replace("c", vals[3])
    if ip_register is not None:
        temp = temp.replace("r[" + str(ip_register) + "]", "IP")
    for test in ["r[1]", "r[2]", "r[3]", "r[4]", "r[5]", "r[6]"]:
        if temp == test + " = " + test + " + 1":
            temp = test + "++"
        if temp.startswith(test + " = " + test + " + "):
            temp = test + " += " + temp[len(test + " = " + test + " + "):]
        if temp.startswith("IP = "):
            test = temp[5:]
            test = test + " + 1"
            test = test.replace("IP", str(line_no))
            if re.search("^[0-9\\+\\*\\-\\/ ]+$", test):
                test = eval(test)
                if test >= total_lines:
                    temp = "exit"
                else:
                    temp = "goto " + str(test)
            else:
                temp = "goto " + test
    return "%3d: %-14s -- %s" % (line_no, instruction_line, temp)


def other_decompile(describe, values):
    if describe:
        return "Decompile the source input"

    ip_register = None
    line_no = 0
    total_lines = 0
    for cur in values:
        if cur[0] != "#":
            total_lines += 1

    for cur in values:
        if cur.startswith("#ip "):
            ip_register = cur[4:]

        if cur[0] == "#":
            print("%3s  %s" % ("", cur))
        else:
            print(decompile(cur, ip_register, line_no, total_lines))
            line_no += 1

def other_debug(describe, values):
    if describe:
        return "Debug the soruce code"

    ip_register = None
    code = []

    for cur in values:
        if cur.startswith("#ip "):
            ip_register = cur[4:]
        elif not cur.startswith("#"):
            code.append(cur)

    r = [0] * 6
    last_line = "<none>"
    ip = 0
    ops = get_ops()
    number_ran = 0

    def step_code(steps, ip):
        ran = 0
        last_code = "<halt>"
        for _ in xrange(steps):
            if ip >= len(code):
                break

            if ip_register is not None:
                r[int(ip_register)] = ip

            cur = code[ip]
            last_code = decompile(cur, ip_register, ip, len(code))
            cur = cur.split(' ')
            ops[cur[0]](r, int(cur[1]), int(cur[2]), int(cur[3]))
            ran += 1

            if ip_register is not None:
                ip = r[int(ip_register)]
            ip += 1
        return ip, ran, last_code

    while True:
        print("      Last: " + last_line)
        if ip >= len(code):
            print("      Next: <halt>")
        else:
            print("      Next: " + decompile(code[ip], ip_register, ip, len(code)))
        print(" Registers: " + "  ".join("<%d>%d" % (i, r[i]) for i in range(len(r))))
        print("     Steps: " + str(number_ran))

        cmd = raw_input("$ ")
        cmd = cmd.split(' ')
        if cmd[0] in {"x", "exit", "q", "quit"}:
            break
        elif cmd[0] in {"context"}:
            for i in range(max(0, ip - 5), min(len(code), ip + 6)):
                print("%s %s" % (">" if i == ip else " ", decompile(code[i], ip_register, i, len(code))))
        elif cmd[0] in {"dump"}:
            for i in range(len(code)):
                print("%s %s" % (">" if i == ip else " ", decompile(code[i], ip_register, i, len(code))))
        elif cmd[0] in {"s", "step"}:
            ip, ran, last_line = step_code(1, ip)
            number_ran += ran
        elif cmd[0] in {"steps"} and len(cmd) == 2:
            ip, ran, last_line = step_code(int(cmd[1]), ip)
            number_ran += ran
        elif cmd[0] in {"set"} and len(cmd) == 3:
            r[int(cmd[1])] = int(cmd[2])
        else:
            print("  exit, x, quit, q = Exit the debugger")
            print("  dump             = Dump all code")
            print("  context          = Show context around current line")
            print("  step, s          = Step through the next line of code")
            print("  steps <#>        = Step through a number of steps")
            print("  set <r> <#>      = Set register r to value")
