#!/usr/bin/env python

from collections import deque

def get_desc():
    return 11, 'Day 11: Hex Ed'

def dist(tx, ty):
    tx = abs(tx)
    ty = abs(ty)

    if ty > tx:
        return ty + tx // 2
    else:
        return tx


def calc(log, values):
    longest = 0

    x, y = 0, 0
    left = 0
    for cur in values[0].split(","):
        left += 1

    for cur in values[0].split(","):
        left -= 1
        if x % 2 == 0:
            offs = {"nw": (-1, -1), "n": (0, -1), "ne": (1, -1), "sw": (-1, 0), "s": (0, 1), "se": (1, 0)}
        else:
            offs = {"nw": (-1, 0), "n": (0, -1), "ne": (1, 0), "sw": (-1, 1), "s": (0, 1), "se": (1, 1)}
        x, y = x + offs[cur][0], y + offs[cur][1]
        cur_dist = dist(x, y)
        if cur_dist > longest:
            longest = cur_dist

    log.show("Furthest away was: " + str(longest))

    return dist(x, y)


def test(log):
    values = [
        "se,sw,se,sw,sw",
    ]

    if calc(log, values) == 2:
        return True
    else:
        return False


def run(log, values):
    log.show(calc(log, values))
