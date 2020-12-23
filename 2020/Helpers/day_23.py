#!/usr/bin/env python3

def get_desc():
    return 23, 'Day 23: Crab Cups'

class Cup():
    __slots__ = ('val', 'left', 'right')
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def calc(log, values, mode):
    cups = list(values[0])
    last = None
    first = None
    cups = {}

    max_value = 0

    for x in values[0]:
        x = int(x)
        max_value = max(x, max_value)
        cup = Cup(x)
        cups[x] = cup
        if first is None:
            first = cup
        if last is not None:
            last.right = cup
            cup.left = last
        last = cup

    if mode == 2:
        while len(cups) < 1000000:
            max_value += 1
            cup = Cup(max_value)
            cups[max_value] = cup
            last.right = cup
            cup.left = last
            last = cup

    last.right = first
    first.left = last

    cur = first
    for round in range(100 if mode == 1 else 10000000):
        if round % 2500000 == 0:
            log(f"Working on round {round}")

        c1 = cur.right
        c2 = c1.right
        c3 = c2.right

        cur.right = c3.right
        cur.right.left = cur

        target = cur.val
        in_hand_vals = {c1.val, c2.val, c3.val}
        while True:
            target -= 1
            if target < 1:
                target = max_value
            if target not in in_hand_vals and target in cups:
                target = cups[target]
                break
        c3.right = target.right
        c3.right.left = c3
        target.right = c1
        c1.left = target

        cur = cur.right

    if mode == 1:
        temp = ""
        cur = cups[1].right
        while cur != cups[1]:
            temp += str(cur.val)
            cur = cur.right

        return temp
    else:
        return cups[1].right.val * cups[1].right.right.val

def test(log):
    values = log.decode_values("""
        389125467
    """)

    log.test(calc(log, values, 1), '67384529')
    log.test(calc(log, values, 2), 149245887792)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))
