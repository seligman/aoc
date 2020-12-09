#!/usr/bin/env python3

def get_desc():
    return 1, 'Day 1: Report Repair'

def calc(log, values, mode):
    values = [int(x) for x in values]

    if mode == 1:
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

    log.test(calc(log, values, 1), 514579)
    log.test(calc(log, values, 2), 241861950)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))
