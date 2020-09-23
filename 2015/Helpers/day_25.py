#!/usr/bin/env python

def get_desc():
    return 25, 'Day 25: Let It Snow'


def calc(target_x, target_y):
    x, y = 1, 1
    value = 20151125

    while x != target_x or y != target_y:
        x += 1
        y -= 1
        if y == 0:
            x, y = 1, x
        value = (value * 252533) % 33554393

    return value


def test(log):
    if calc(4, 5) == 6899651:
        return True
    else:
        return False


def run(log, values):
    log.show(calc(3029, 2947))
