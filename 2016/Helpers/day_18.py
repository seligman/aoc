#!/usr/bin/env python

def get_desc():
    return 18, 'Day 18: Like a Rogue'


def calc(values, rows):
    ret = 0
    row = [0 if x == "^" else 1 for x in values[0]]
    its_a_trap = {(0, 0, 1), (1, 0, 0), (0, 1, 1), (1, 1, 0)}

    while rows > 0:
        rows -= 1
        ret += sum(row)
        row = [1] + row + [1]
        row = [0 if tuple(row[x-1:x+2]) in its_a_trap else 1 for x in range(1, len(row) - 1)]

    return ret


def test(log):
    values = [
        ".^^.^.^^^^",
    ]

    if calc(values, 10) == 38:
        return True
    else:
        return False


def run(log, values):
    for rows in [40, 400000]:
        log.show("There are %d safe tiles in %d rows." % (calc(values, rows), rows))
