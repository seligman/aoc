#!/usr/bin/env python3

import codecs

def get_desc():
    return 8, 'Day 8: Matchsticks'


def calc(log, values):
    total_size = 0
    total_decoded = 0
    total_encoded = 0

    for cur in values:
        total_size += len(cur)
        total_decoded += len(codecs.escape_decode(cur[1:-1])[0])

        cur = cur.replace("\\", "\\\\")
        cur = cur.replace('"', '\\"')

        total_encoded += len(cur) + 2

    log.show("Increased: %d" % (total_encoded - total_size,))

    return total_size - total_decoded


def test(log):
    return True


def run(log, values):
    log.show(calc(log, values))
