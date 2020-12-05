#!/usr/bin/env python

from collections import defaultdict

def get_desc():
    return 5, 'Day 5: Binary Boarding'

def calc(log, values, mode):
    neighbors = defaultdict(int)
    seats = set()
    for value in values:
        row, row_part = 127, 64
        seat, seat_part = 7, 4
        for cur in value:
            if cur in {"F", "B"}:
                row += row_part * {"F": -1, "B": 1}[cur]
                row_part //= 2
            elif cur in {"L", "R"}:
                seat += seat_part * {"L": -1, "R": 1}[cur]
                seat_part //= 2
        seat_id = (row // 2) * 8 + (seat // 2)

        seats.add(seat_id)
        neighbors[seat_id - 1] += 1
        neighbors[seat_id + 1] += 1

    if mode == 1:
        return max(seats)
    else:
        return [x for x in neighbors if neighbors[x] == 2 and x not in seats][0]

def test(log):
    values = log.decode_values("""
        FBFBBFFRLR
    """)
    log.test(calc(log, values, 1), 357)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))
