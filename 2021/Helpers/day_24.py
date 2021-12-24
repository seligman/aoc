#!/usr/bin/env python3

import re, string

def get_desc():
    return 24, 'Day 24: Arithmetic Logic Unit'

def other_compile(describe, values, log=print):
    if describe:
        return "Compile the input to a python function"
    pos = [0]
    ret = []
    var = [""]
    def handle_inp(g):
        ret.append(None)
        ret.append([f"{g[0]}", f"val[{pos[0]}]"])
        pos[0] += 1
        var[0] = g[0]
    def handle_add(g):
        if var[0] == g[0]:
            if ret[-1][1] == "":
                ret[-1][1] = g[1]
            else:
                ret[-1][1] = f"({ret[-1][1]} + {g[1]})"
        else:
            ret.append([f"{g[0]}", f"({g[0]} + {g[1]})"])
            var[0] = g[0]
    def handle_mul(g):
        if g[1] == "0":
            ret.append([g[0], ""])
            var[0] = g[0]
        else:
            if var[0] == g[0]:
                ret[-1][1] = f"({ret[-1][1]} * {g[1]})"
            else:
                ret.append([f"{g[0]}", f"({g[0]} * {g[1]})"])
                var[0] = g[0]
    def handle_div(g):
        if g[1] != "1":
            if var[0] == g[0]:
                ret[-1][1] = f"({ret[-1][1]} // {g[1]})"
            else:
                ret.append([f"{g[0]}", f"({g[0]} // {g[1]})"])
                var[0] = g[0]
    def handle_mod(g):
            if var[0] == g[0]:
                ret[-1][1] = f"({ret[-1][1]} % {g[1]})"
            else:
                ret.append([f"{g[0]}", f"({g[0]} % {g[1]})"])
                var[0] = g[0]
    def handle_eql(g):
        if g[1] == "0" and g[0] == ret[-1][0] and "==" in ret[-1][1]:
            ret[-1][1] = ret[-1][1][-1] + ret[-1][1][1:-1] + ret[-1][1][0]
            pass
        else:
            ret.append([f"{g[0]}", f"1 if {g[0]} == {g[1]} else 0"])

    log("def compiled(use, val):")
    log("    x = 0")
    log("    w = 0")
    log("    y = 0")
    log("    z = 0")

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

    use = 0
    for cur in ret:
        if cur is None:
            log("")
            log(f"    if use is None or {use} in use:")
            use += 1
        else:
            x, y = cur
            if y.startswith("("):
                y = y[1:-1]
            y = y.replace("+ -", "- ")
            log("        " + x + " = " + y)

    log("")
    log("    return z")

    return 0

"""
This next function is a placeholder to make autocomplete happy.  It's really compilied 
at runtime using the helper above to something like this:

def compiled(use, val):
    x = 0
    w = 0
    y = 0
    z = 0

    if use is None or 0 in use:
        w = val[0]
        x = (z % 26) + 10
        x = 0 if x == w else 1
        y = (25 * x) + 1
        z = z * y
        y = (w + 12) * x
        z = z + y

    # ... removed most digits ...

    if use is None or 13 in use:
        w = val[13]
        x = z % 26
        z = z // 26
        x = x - 14
        x = 0 if x == w else 1
        y = (25 * x) + 1
        z = z * y
        y = (w + 13) * x
        z = z + y

    return z
"""
def compiled(*args):
    raise Exception("Place holder function, replaced at runtime")

def calc(log, values, mode):
    data = []
    def helper_log(x):
        data.append(x)
    other_compile(False, values, log=helper_log)
    exec("\n".join(data), globals())

    def tryout(use1, use2, val, skip, possible):
        for a in range(1, 10):
            for b in range(1, 10):
                val[use1] = a
                val[use2] = b
                if compiled(skip | {use1, use2}, val) == 0:
                    possible.append((a, b, use1, use2))
        val[use1] = 1
        val[use2] = 1

    def level(depth, apply, states, val, skip):
        if apply is not None:
            a, b, use1, use2 = apply
            states[use1] = False
            states[use2] = False
            skip.add(use1)
            skip.add(use2)
            val[use1] = a
            val[use2] = b
            if sum(states) == 0:
                return val
        use1 = states.index(True)
        use2 = 13 - states[::-1].index(True)
        possible = []
        tryout(use1, use2, val, skip, possible)
        if len(possible) == 0:
            use1 = states.index(True)
            use2 = states[use1+1:].index(True) + use1 + 1
            tryout(use1, use2, val, skip, possible)
        possible.sort(reverse=mode==1)
        for x in possible:
            ret = level(depth + 1, x, states[:], val[:], set(skip))
            if ret is not None:
                return ret
        return None
    
    val = [1 for _ in range(14)]
    states = [True] * 14
    skip = set()
    val = level(0, None, states[:], val[:], set(skip))
    return "".join(str(x) for x in val)

def test(log):
    log("No test")

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))
