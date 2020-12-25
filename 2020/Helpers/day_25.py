#!/usr/bin/env python3

def get_desc():
    return 25, 'Day 25: Combo Breaker'


def transform(loop, subject):
    value = 1
    for _ in range(loop):
        value = value * subject
        value = value % 20201227
    return value

def transform_bail(subject, bail):
    value = 1
    loop = 0
    while True:
        loop += 1
        value = value * subject
        value = value % 20201227
        if bail == value:
            return loop

def calc(log, values, mode):
    door = transform_bail(7, int(values[1]))
    return transform(door, int(values[0]))


def test(log):
    values = log.decode_values("""
        5764801
        17807724
    """)

    log.test(calc(log, values, 1), 14897079)

def run(log, values):
    log(calc(log, values, 1))
