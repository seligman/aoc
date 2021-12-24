#!/usr/bin/env python3

import re, string

def get_desc():
    return 24, 'Day 24: Arithmetic Logic Unit'

def calc(log, values, mode):
    if False:
        pos = [0]
        def handle_inp(g):
            print(f"{g[0]} = val[{pos[0]}]")
            pos[0] += 1
        def handle_add(g):
            print(f"{g[0]} += {g[1]}")
        def handle_mul(g):
            print(f"{g[0]} *= {g[1]}")
        def handle_div(g):
            print(f"{g[0]} //= {g[1]}")
        def handle_mod(g):
            print(f"{g[0]} = {g[0]} % {g[1]}")
        def handle_eql(g):
            print(f"{g[0]} = 1 if {g[0]} == {g[1]} else 0")

        for cur in values:
            m = re.search("^([a-z]+) ([a-z]+)$", cur)
            if m is not None:
                handle_inp(m.groups()[1:])
            else:
                m = re.search("^([a-z]+) ([a-z]+) ([a-z0-9-]+)$", cur)
                x, g = m.group(1), m.groups()[1:]
                if x == "add": handle_add(g)
                elif x == "div": handle_div(g)
                elif x == "mul": handle_mul(g)
                elif x == "mod": handle_mod(g)
                elif x == "eql": handle_eql(g)
                else:
                    raise Exception()
        # return(sn, var["z"])
        return 0

    stuffs = []
    for i in range(14):
        chunk = list(map(lambda s: "".join(list(filter(lambda c: c in string.digits + "-1", s))), values[:18]))
        stuff = {
            'div': int(chunk[4]),
            'n1': int(chunk[5]),
            'n2': int(chunk[15])
        }
        stuffs.append(stuff)
        values = values[18:]
    if mode == 2:
        rng = range(9999999)
    else:
        rng = range(9999999, -1, -1)

    for input in rng:
        z = 0
        ans = ""
        dindex = 0
        for index in range(14):
            stuff = stuffs[index]
            if stuff['div'] == 1:
                digit = str(input).zfill(7)[dindex]
                z = section(w=int(digit), z=z, **stuffs[index])
                ans += digit
                dindex += 1
            else:
                fixed = z % 26 + stuff['n1']
                if fixed > 9 or fixed < 0:
                    z = "wrong"
                    break
                z = section(w=fixed, z=z, **stuffs[index])
                ans += str(fixed)
        if z == 0 and "0" not in ans:
            return ans

    return 0

def section(w, div, n1, n2, z):
    x = 1 if ((z % 26) + n1) != w else 0
    y1 = 25 * x + 1
    y2 = (w + n2) * x
    return (z // div) * y1 + y2

def test(log):
    log("No test")

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))
