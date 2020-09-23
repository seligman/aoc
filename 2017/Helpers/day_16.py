#!/usr/bin/env python

from collections import deque

def get_desc():
    return 16, 'Day 16: Permutation Promenade'


def calc(log, values, dance):
    dance = list(dance)

    for cur in values[0].split(','):
        if cur[0] == "s":
            dance = deque(dance)
            dance.rotate(int(cur[1:]))
            dance = list(dance)
        elif cur[0] == "x":
            cur = [int(x) for x in cur[1:].split("/")]
            dance[cur[0]], dance[cur[1]] = dance[cur[1]], dance[cur[0]]
        elif cur[0] == "p":
            cur = [dance.index(x) for x in cur[1:].split("/")]
            dance[cur[0]], dance[cur[1]] = dance[cur[1]], dance[cur[0]]
        else:
            raise Exception()

    return "".join(dance)


def calc2(log, values, dance):
    seen = {}
    i = 0
    left = 1000000000
    while left > 0:
        seen[dance] = i
        dance = calc(log, values, dance)
        i += 1
        left -= 1
        if dance in seen:
            left -= (left // (i - seen[dance])) * (i - seen[dance])
            seen = {}
    return dance


def test(log):
    values = [
        "s1,x3/4,pe/b",
    ]

    if calc(log, values, "abcde") == "baedc":
        return True
    else:
        return False


def run(log, values):
    log.show(calc(log, values, 'abcdefghijklmnop'))
    log.show(calc2(log, values, 'abcdefghijklmnop'))
