#!/usr/bin/env python3

def get_desc():
    return 1, 'Day 1: Chronal Calibration'


def calc(log, values, test_mode):
    ret = 0
    real_ret = None
    seen = {}
    first = True
    while first:
        for value in values:
            ret += value
            seen[ret] = seen.get(ret, 0) + 1
            if first:
                if seen[ret] == 2:
                    log.show("First twice is %d" % (ret,))
                    first = False
        if real_ret is None:
            real_ret = ret
        if test_mode:
            break
    return real_ret


def test(log):
    test = [
        ("+1, +1, +1",  3),
        ("+1, +1, -2",  0),
        ("-1, -2, -3", -6),
    ]
    for value, ret in test:
        values = [int(x.strip()) for x in value.split(', ')]
        test_val = calc(log, values, True)
        log.show("[%s] -> %d, %d" % (value, ret, test_val))
        if ret != test_val:
            return False

    return True


def run(log, values):
    values = [int(x) for x in values]
    log.show(calc(log, values, False))
