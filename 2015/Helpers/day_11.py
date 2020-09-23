#!/usr/bin/env python

import re

def get_desc():
    return 11, 'Day 11: Corporate Policy'


def is_valid(r, value):
    if "i" in value or "o" in value or "l" in value:
        return False
    if r.search(value) is None:
        return False
    expected = "-"
    run = 1
    for cur in value:
        if cur == expected:
            run += 1
            if run == 3:
                return True
        else:
            run = 1
        expected = chr(ord(cur) + 1)
    return False


def calc(values):
    r = re.compile("(.)\\1.*?(.)\\2")
    value = list(values[0])

    while True:
        dig = len(value) - 1
        while True:
            if value[dig] == "z":
                value[dig] = "a"
                dig -= 1
            else:
                value[dig] = chr(ord(value[dig]) + 1)
                break
        if is_valid(r, "".join(value)):
            return "".join(value)


def test(log):
    values = [
        "ghijklmn",
    ]

    if calc(values) == 'ghjaabcc':
        return True
    else:
        return False


def run(log, values):
    ret = calc(values)
    log.show(ret)
    ret = calc([ret])
    log.show(ret)
