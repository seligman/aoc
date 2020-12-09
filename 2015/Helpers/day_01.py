#!/usr/bin/env python3

def get_desc():
    return 1, 'Day 1: Not Quite Lisp'


def calc(log, values):
    ret = 0
    pos = 0
    shown = False
    for cur in values:
        for sub in cur:
            if sub == "(":
                ret += 1
                pos += 1
            elif sub == ")":
                ret -= 1
                pos += 1
            if not shown:
                if ret < 0:
                    log.show("Entered basement on %d" % (pos,))
                    shown = True

    return ret


def test(log):
    values = [
        ")())())",
    ]

    if calc(log, values) == -3:
        return True
    else:
        return False


def run(log, values):
    log.show(calc(log, values))
