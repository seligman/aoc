#!/usr/bin/env python3

from collections import deque

def get_desc():
    return 12, 'Day 12: Digital Plumber'


def calc(log, values):
    progs = {}
    remaining = set()
    for cur in values:
        cur = cur.split(" <-> ")
        remaining.add(cur[0])
        progs[cur[0]] = cur[1].split(", ")

    groups = []

    while len(remaining) > 0:
        cur = list(remaining)[0]
        seen = set()
        seen.add(cur)
        todo = deque()
        todo.append(cur)
        remaining.remove(cur)
        while len(todo) > 0:
            cur = todo.popleft()
            for sub in progs[cur]:
                if sub not in seen:
                    remaining.remove(sub)
                    seen.add(sub)
                    todo.append(sub)
        groups.append(seen)

    log.show("There are " + str(len(groups)) + " groups")

    for group in groups:
        if "0" in group:
            return len(group)

    return None


def test(log):
    values = [
        "0 <-> 2",
        "1 <-> 1",
        "2 <-> 0, 3, 4",
        "3 <-> 2, 4",
        "4 <-> 2, 3, 6",
        "5 <-> 6",
        "6 <-> 4, 5",
    ]

    if calc(log, values) == 6:
        return True
    else:
        return False


def run(log, values):
    log.show(calc(log, values))
