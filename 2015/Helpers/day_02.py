#!/usr/bin/env python

def get_desc():
    return 2, 'Day 2: I Was Told There Would Be No Math'


def calc(log, values):
    ret = 0
    ribbon = 0
    for cur in values:
        cur = [int(x) for x in cur.split("x")]
        a, b, c = cur[0] * cur[1] * 2, cur[1] * cur[2] * 2, cur[0] * cur[2] * 2
        ret += sum((a, b, c)) + min((a, b, c)) // 2
        ribbon += sum(sorted(cur)[0:2])*2 + cur[0] * cur[1] * cur[2]

    log.show("%d feet of ribbon" % (ribbon,))

    return ret


def test(log):
    values = [
        "2x3x4",
    ]

    if calc(log, values) == 58:
        return True
    else:
        return False


def run(log, values):
    log.show(calc(log, values))
