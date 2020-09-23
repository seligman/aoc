#!/usr/bin/env python

def get_desc():
    return 16, 'Day 16: Dragon Checksum'


def calc(values, target_len):
    value = values[0]

    while len(value) < target_len:
        value = value + "0" + "".join(["1" if x == "0" else "0" for x in reversed(value)])

    value = value[0:target_len]

    code = {
        "00": "1",
        "11": "1",
        "01": "0",
        "10": "0",
    }

    while len(value) % 2 != 1:
        value = "".join([code[value[x:x+2]] for x in range(0, len(value), 2)])

    return value


def test(log):
    values = [
        "10000",
    ]

    if calc(values, 20) == "01100":
        return True
    else:
        return False


def run(log, values):
    log.show(calc(values, 272))
    log.show(calc(values, 35651584))
