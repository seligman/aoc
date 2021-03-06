#!/usr/bin/env python3

from collections import defaultdict, deque


def get_desc():
    return 23, 'Day 23: Coprocessor Conflagration'


def deref(r, value):
    if len(value) == 1 and value >= 'a' and value <= 'z':
        return r[value]
    else:
        return int(value)


def calc(log, values, show_heat, mode):
    values = [x.split(' ') for x in values]
    heat = [0] * len(values)
    ret = 0
    r = defaultdict(int)
    ip = 0

    if mode == 1:
        r["a"] = 1

    while ip < len(values):
        cur = values[ip]
        new_ip = ip + 1
        if not cur[0].startswith("#"):
            heat[ip] += 1
            if cur[0] == "set":
                r[cur[1]] = deref(r, cur[2])
            elif cur[0] == "sub":
                r[cur[1]] -= deref(r, cur[2])
            elif cur[0] == "mul":
                ret += 1
                r[cur[1]] *= deref(r, cur[2])
            elif cur[0] == "jnz":
                if deref(r, cur[1]) != 0:
                    new_ip = ip + deref(r, cur[2])
            else:
                raise Exception()
        ip = new_ip

    if show_heat:
        for i in range(len(values)):
            raw = " ".join(values[i])
            if values[i][0].startswith("#"):
                easy = "comment"
            elif values[i][0] == "set":
                easy = "%s = %s" % (values[i][1], values[i][2])
            elif values[i][0] == "sub":
                easy = "%s -= %s" % (values[i][1], values[i][2])
            elif values[i][0] == "mul":
                easy = "%s *= %s" % (values[i][1], values[i][2])
            elif values[i][0] == "jnz":
                easy = "if %s != 0 then skip(%s)" % (values[i][1], values[i][2])
            else:
                raise Exception()
            log.show("%3d: %5d: %-20s %s" % (i, heat[i], raw, easy))

    if mode == 0:
        return ret
    else:
        return r["h"]


def test(log):
    return True


def run(log, values):
    log.show(calc(log, values, False, 0))

    h = 0
    # The initial value of c
    for x in range(107900, 107900 + 17000 + 1, 17):
        for i in range(2,x):
            if x % i == 0:
                h += 1
                break
    log.show("Final value of H is %d" % (h,))


class DummyLog:
    def __init__(self):
        pass

    def show(self, value):
        print(value)


def other_heat(describe, values):
    if describe:
        return "Show heat map of program"

    calc(DummyLog(), values, True, 0)
