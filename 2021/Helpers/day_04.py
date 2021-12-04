#!/usr/bin/env python3

import re
from collections import defaultdict

def get_desc():
    return 4, 'Day 4: Giant Squid'

def lines():
    for x in range(5):
        yield range(x, 25, 5)
    for x in range(5):
        yield range(x * 5, x * 5 + 5)

def calc(log, values, mode):
    values = values[:]
    drawn = [int(x) for x in values.pop(0).split(",")]
    values.pop(0)

    grids = []
    numbers = defaultdict(list)
    for i in range(0, len(values), 6):
        temp = values[i:i+5]
        if len(temp) == 5:
            grids.append([])
            for row in temp:
                grids[-1] += [{'val': int(y), 'picked': False} for y in re.split(" +", row.strip())]
            for xy in range(25):
                numbers[grids[-1][xy]['val']].append((grids[-1], xy))

    ret = 0
    for pick in drawn:
        for grid, xy in numbers[pick]:
            grid[xy]['picked'] = True

        won = set()
        for i, grid in enumerate(grids):
            for line in lines():
                if sum(grid[xy]['picked'] for xy in line) == 5:
                    won.add(i)
                    ret = sum(x['val'] for x in grid if not x['picked']) * pick
                    if mode == 1:
                        return ret

        grids = [x for i, x in enumerate(grids) if i not in won]

    return ret


def test(log):
    values = log.decode_values("""
        7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

        22 13 17 11  0
         8  2 23  4 24
        21  9 14 16  7
         6 10  3 18  5
         1 12 20 15 19

         3 15  0  2 22
         9 18 13 17  5
        19  8  7 25 23
        20 11 10 24  4
        14 21 16 12  6

        14 21 17 24  4
        10 16 15  9 19
        18  8 23 26 20
        22 11 13  6  5
         2  0 12  3  7
    """)

    log.test(calc(log, values, 1), 4512)
    log.test(calc(log, values, 2), 1924)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))
