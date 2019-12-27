#!/usr/bin/env python

from collections import deque

def get_desc():
    return 19, 'Day 19: An Elephant Named Joseph'


def calc2(values):
    elves = int(values[0])
    left = deque()
    right = deque()
    for i in range(1, elves + 1):
        if i < (elves / 2) + 1:
            left.append(i)
        else:
            right.appendleft(i)

    while len(left) > 0 and len(right) > 0:
        if len(left) > len(right):
            left.pop()
        else:
            right.pop()

        right.appendleft(left.popleft())
        left.append(right.pop())

    if len(left) > 0:
        return left.pop()
    else:
        return right.pop()


def calc(values):
    elves = int(values[0])
    has_presents = deque(range(1, elves + 1))

    while len(has_presents) > 1:
        has_presents.rotate(-1)
        has_presents.popleft()

    return has_presents.pop()


def test(log):
    values = [
        "5",
    ]

    if calc(values) == 3:
        if calc2(values) == 2:
            return True
        else:
            return False
    else:
        return False


def run(log, values):
    log.show("To the left: " + str(calc(values)))
    log.show("Across the circle: " + str(calc2(values)))
