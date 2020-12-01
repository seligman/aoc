#!/usr/bin/env python

def get_desc():
    return 1, 'Day 1: Report Repair'


def calc(log, values, step):
    values = [int(x) for x in values]

    if step == 1:
        for x in range(len(values)):
            for y in range(x + 1, len(values)):
                if values[x] + values[y] == 2020:
                    return values[x] * values[y]
    else:
        for x in range(len(values)):
            for y in range(x + 1, len(values)):
                for z in range(y + 1, len(values)):
                    if values[x] + values[y] + values[z] == 2020:
                        return values[x] * values[y] * values[z]

    return 10


def test(log):
    values = log.decode_values("""
        1721
        979
        366
        299
        675
        1456
    """)

    ret, expected = calc(log, values, 1), 514579
    log("Test returned %s, expected %s" % (str(ret), str(expected)))
    if ret != expected:
        return False

    ret, expected = calc(log, values, 2), 241861950
    log("Test returned %s, expected %s" % (str(ret), str(expected)))
    if ret != expected:
        return False

    return True


def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))
