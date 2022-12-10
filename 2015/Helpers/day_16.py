#!/usr/bin/env python3

import re

DAY_NUM = 16
DAY_DESC = 'Day 16: Aunt Sue'


def calc(values, mode):
    target = {
        "children": 3,
        "cats": 7,
        "samoyeds": 2,
        "pomeranians": 3,
        "akitas": 0,
        "vizslas": 0,
        "goldfish": 5,
        "trees": 3,
        "cars": 2,
        "perfumes": 1,
    }

    sues = {}
    r = re.compile("Sue ([0-9]+): (.*)")

    for cur in values:
        m = r.search(cur)
        vals = {}
        for cur in m.group(2).split(", "):
            cur = cur.split(": ")
            vals[cur[0]] = int(cur[1])
        sues[int(m.group(1))] = vals

    for sue in sues:
        good = True
        for key in target:
            value = target[key]
            if key in sues[sue]:
                if mode == 0:
                    if value != sues[sue][key]:
                        good = False
                else:
                    if key in {'cats', 'trees'}:
                        if value >= sues[sue][key]:
                            good = False
                    elif key in {'pomeranians', 'goldfish'}:
                        if value <= sues[sue][key]:
                            good = False
                    else:
                        if value != sues[sue][key]:
                            good = False
        if good:
            return sue

    return -1


def test(log):
    return True


def run(log, values):
    log.show(calc(values, 0))
    log.show(calc(values, 1))
