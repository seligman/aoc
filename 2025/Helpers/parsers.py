#!/usr/bin/env python3

def get_ints(line):
    ret = [""]
    for x in line:
        if len(ret[-1]) == 0 and x == "-":
            ret[-1] = "-"
        elif "0" <= x <= "9":
            ret[-1] += x
        else:
            if len(ret[-1]) > 0:
                ret.append("")
    if len(ret[-1]) == 0:
        ret.pop(-1)
    return list(map(int, ret))

def get_floats(line):
    ret = [""]
    for x in line:
        if x == "-" and len(ret[-1]) == 0:
            ret[-1] = "-"
        elif "0" <= x <= "9":
            ret[-1] += x
        elif x == "." and "." not in ret[-1]:
            ret[-1] += x
        else:
            if len(ret[-1]) > 0:
                ret.append("")
    if len(ret[-1]) == 0:
        ret.pop(-1)
    return list(map(float, ret))
