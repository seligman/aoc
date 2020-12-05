#!/usr/bin/env python

def get_desc():
    return 5, 'Day 5: Binary Boarding'

def calc(log, values, mode):
    final = []

    ret = 0
    for value in values:
        rows = list(range(128))
        seats = list(range(8))
        for cur in value:
            if cur == "F":
                rows = rows[:len(rows)//2]
            elif cur == "B":
                rows = rows[len(rows)//2:]
            elif cur == "R":
                seats = seats[len(seats)//2:]
            elif cur == "L":
                seats = seats[:len(seats)//2]

        final.append(rows[0] * 8 + seats[0])
        ret = max(ret, rows[0] * 8 + seats[0])

    if mode == 1:
        return ret
    else:
        final.sort()
        for i in range(len(final)-1):
            if final[i] + 2 == final[i+1]:
                print(final[i] + 1)

def test(log):
    values = log.decode_values("""
        FBFBBFFRLR
    """)

    log.test(calc(log, values, 1), 357)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))
