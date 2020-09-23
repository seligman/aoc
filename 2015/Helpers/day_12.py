#!/usr/bin/env python

import json

def get_desc():
    return 12, 'Day 12: JSAbacusFramework.io'


def summarize(data, red_pass):
    ret = 0
    if isinstance(data, dict):
        skip = False
        if red_pass:
            if "red" in data.values():
                skip = True
            elif "red" in data:
                skip = True
        if not skip:
            for value in data.values():
                ret += summarize(value, red_pass)
    elif isinstance(data, list):
        for key in data:
            ret += summarize(key, red_pass)
    elif isinstance(data, int):
        ret += data
    return ret


def calc(values, red_pass):
    data = values[0]
    data = json.loads(data)

    return summarize(data, red_pass)


def test(log):
    values = [
        '{"a":[-1,1]}',
    ]

    if calc(values, False) == 0:
        return True
    else:
        return False


def run(log, values):
    log.show(calc(values, False))
    log.show(calc(values, True))
