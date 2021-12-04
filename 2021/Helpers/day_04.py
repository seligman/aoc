#!/usr/bin/env python3

import re

def get_desc():
    return 4, 'Day 4: Giant Squid'

def calc(log, values, mode):
    values = values[:]
    drawn = [int(x) for x in values.pop(0).split(",")]
    values.pop(0)

    grids = []
    numbers = {}
    for i in range(0, len(values), 6):
        temp = values[i:i+5]
        if len(temp) == 5:
            grids.append([])
            for row in temp:
                grids[-1] += [[int(y), False] for y in re.split(" +", row.strip())]
            for xy in range(25):
                numbers[grids[-1][xy][0]] = numbers.get(grids[-1][xy][0], []) + [[grids[-1], xy]]

    ret = 0
    for pick in drawn:
        for cur in numbers[pick]:
            cur[0][cur[1]][1] = True

        while True:
            won_i, won = None, None
            for i, grid in enumerate(grids):
                if won is None:
                    for x in range(5):
                        if sum(grid[xy][1] for xy in range(x, 25, 5)) == 5:
                            won_i, won = i, grid
                            break
                
                if won is None:
                    for y in range(5):
                        if sum(grid[xy][1] for xy in range(y * 5, y * 5 + 5)) == 5:
                            won_i, won = i, grid
                            break

            if won is None:
                break

            if won is not None:
                if mode == 2:
                    grids.pop(won_i)

                ret = sum(z[0] for z in won if not z[1]) * pick
                if mode == 1:
                    return ret

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
