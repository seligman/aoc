#!/usr/bin/env python

def get_desc():
    return 5, 'Day 5: Binary Boarding'

def calc(log, values, mode):
    final = []

    ret = 0
    for value in values:
        row, row_part = 127, 64
        seat, seat_part = 7, 4
        for cur in value:
            if cur == "F":
                row -= row_part
                row_part //= 2
            elif cur == "B":
                row += row_part
                row_part //= 2
            elif cur == "L":
                seat -= seat_part
                seat_part //= 2
            elif cur == "R":
                seat += seat_part
                seat_part //= 2

        row //= 2
        seat //= 2

        seat_id = row * 8 + seat
        final.append(seat_id)
        ret = max(ret, seat_id)

    if mode == 1:
        return ret
    else:
        final.sort()
        for i in range(len(final)-1):
            if final[i] + 2 == final[i+1]:
                return final[i] + 1

def test(log):
    values = log.decode_values("""
        FBFBBFFRLR
    """)

    log.test(calc(log, values, 1), 357)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))
