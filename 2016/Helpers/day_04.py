#!/usr/bin/env python3

import re
from collections import defaultdict

DAY_NUM = 4
DAY_DESC = 'Day 4: Security Through Obscurity'


def calc(log, values):
    r = re.compile("([a-z-]+)-([0-9]+)\\[([a-z]+)\\]")
    ret = 0

    for cur in values:
        m = r.search(cur).groups()
        counts = defaultdict(int)
        for sub in m[0]:
            if sub != '-':
                counts[sub] += 1
        letters = list(counts)
        letters.sort(key=lambda x:(-counts[x], x))
        letters = "".join(letters[0:5])

        if letters == m[2]:
            temp = ""
            for sub in m[0]:
                if sub == "-":
                    temp += " "
                else:
                    temp += chr((((ord(sub) - ord('a')) + int(m[1])) % 26) + ord('a'))
            if "north" in temp and "pole" in temp:
                log.show("%s - %s" % (temp, m[1]))
            ret += int(m[1])

    return ret


def test(log):
    values = [
        "aaaaa-bbb-z-y-x-123[abxyz]",
        "a-b-c-d-e-f-g-h-987[abcde]",
        "not-a-real-room-404[oarel]",
        "totally-real-room-200[decoy]",
    ]

    if calc(log, values) == 1514:
        return True
    else:
        return False


def run(log, values):
    log.show(calc(log, values))
