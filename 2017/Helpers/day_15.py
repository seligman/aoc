#!/usr/bin/env python

def get_desc():
    return 15, 'Day 15: Dueling Generators'


def calc(log, values):
    a = int(values[0][24:])
    b = int(values[1][24:])

    ret = 0
    rounds = 40000000
    while rounds > 0:
        rounds -= 1
        a = (a * 16807) % 2147483647
        b = (b * 48271) % 2147483647
        if (a & 65535) == (b & 65535):
            ret += 1

    return ret


def calc2(log, values):
    a = int(values[0][24:])
    b = int(values[1][24:])

    ret = 0
    rounds = 5000000
    while rounds > 0:
        rounds -= 1
        while True:
            a = (a * 16807) % 2147483647
            if a % 4 == 0:
                break
        while True:
            b = (b * 48271) % 2147483647
            if b % 8 == 0:
                break
        if (a & 65535) == (b & 65535):
            ret += 1

    return ret


def test(log):
    values = [
        "Generator A starts with 65",
        "Generator B starts with 8921",
    ]

    if calc(log, values) == 588:
        log.show("Pass 1 worked")
        if calc2(log, values) == 309:
            log.show("Pass 2 worked")
            return True
        else:
            return False
    else:
        return False


def run(log, values):
    log.show(calc(log, values))
    log.show(calc2(log, values))
