#!/usr/bin/env python3

def get_desc():
    return 23, 'Day 23: Crab Cups'

def calc(log, values, mode):
    if mode == 1:
        cups = [-1] * (len(values[0]))
    else:
        cups = [-1] * 1000000

    max_value = 0
    last = None

    for x in values[0]:
        x = int(x) - 1
        max_value = max(x, max_value)
        if last is not None:
            cups[last] = x
        last = x

    if mode == 2:
        while max_value < 1000000 - 1:
            max_value += 1
            cups[last] = max_value
            last = max_value

    cups[last] = int(values[0][0]) - 1
    cur = cups[last]
    cups_count = max_value + 1

    for round in range(100 if mode == 1 else 10000000):
        if round % 2500000 == 0:
            log(f"Working on round {round}")

        c1 = cups[cur]
        c2 = cups[c1]
        c3 = cups[c2]

        cups[cur] = cups[c3]

        target = (cur - 1) % cups_count
        if target == c1 or target == c2 or target == c3:
            target = (target - 1) % cups_count
            if target == c1 or target == c2 or target == c3:
                target = (target - 1) % cups_count
                if target == c1 or target == c2 or target == c3:
                    target = (target - 1) % cups_count

        cups[target], cups[c3] = c1, cups[target]
        cur = cups[cur]

    if mode == 1:
        temp = ""
        cur = cups[0]
        while cur != 0:
            temp += str(cur + 1)
            cur = cups[cur]
        return int(temp)
    else:
        return (cups[0] + 1) * (cups[cups[0]] + 1)

def test(log):
    values = log.decode_values("""
        389125467
    """)

    log.test(calc(log, values, 1), 67384529)
    log.test(calc(log, values, 2), 149245887792)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))
