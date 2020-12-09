#!/usr/bin/env python3

def get_desc():
    return 1, 'Day 1: Inverse Captcha'


def calc(log, values):
    value = list(values[0])
    ret = 0
    ret2 = 0

    for i in range(len(value)):
        if value[i] == value[(i+1)%len(value)]:
            ret += int(value[i])
        if value[i] == value[(i+(len(value)//2))%len(value)]:
            ret2 += int(value[i])

    log.show("Half around: " + str(ret2))

    return ret


def test(log):
    values = [
        "91212129",
    ]

    if calc(log, values) == 9:
        return True
    else:
        return False


def run(log, values):
    log.show(calc(log, values))
