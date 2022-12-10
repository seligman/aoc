#!/usr/bin/env python3

DAY_NUM = 1
DAY_DESC = 'Day 1: The Tyranny of the Rocket Equation'


def calc(log, values, mode):
    ret = 0
    for cur in values:
        if mode == 1:
            ret += (int(cur) // 3) - 2
        else:
            first = True
            while True:
                temp = (int(cur) // 3) - 2
                if temp > 0 or first:
                    ret += temp
                first = False
                if temp > 0:
                    cur = temp
                else:
                    break

    return ret


def test(log):
    values = log.decode_values("""
        100756
    """)

    ret, expected = calc(log, values, 1), 33583 
    log("Test returned %s, expected %s" % (str(ret), str(expected)))
    if ret != expected:
        return False
    ret, expected = calc(log, values, 2), 50346 
    log("Test returned %s, expected %s" % (str(ret), str(expected)))
    if ret != expected:
        return False

    return True


def run(log, values):
    log("Fuel requirements: " + str(calc(log, values, 1)))
    log("Including mass: " + str(calc(log, values, 2)))
