#!/usr/bin/env python3

DAY_NUM = 5
DAY_DESC = 'Day 5: A Maze of Twisty Trampolines, All Alike'


def calc(log, values, mode):
    ip = 0
    steps = 0
    values = [int(x) for x in values]

    if mode == 0:
        while ip < len(values):
            next_ip = values[ip] + ip
            values[ip] += 1
            ip = next_ip
            steps += 1
    else:
        while ip < len(values):
            next_ip = values[ip] + ip
            if values[ip] >= 3:
                values[ip] -= 1
            else:
                values[ip] += 1
            ip = next_ip
            steps += 1

    return steps


def test(log):
    values = [
        "0",
        "3",
        "0",
        "1",
        "-3",
    ]

    if calc(log, values, 0) == 5:
        if calc(log, values, 1) == 10:
            return True
        else:
            return False
    else:
        return False


def run(log, values):
    log.show(calc(log, values, 0))
    log.show(calc(log, values, 1))
