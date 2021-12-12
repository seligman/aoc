#!/usr/bin/env python3

from collections import deque

def get_desc():
    return 12, 'Day 12: Passage Pathing'

def calc(log, values, mode):
    paths = {}

    for cur in values:
        if len(cur.strip()) > 0:
            cur = cur.split("-")
            for x,y in ((cur[0], cur[1]), (cur[1], cur[0])):
                if x not in paths:
                    paths[x] = set()
                paths[x].add(y)

    trails = 0
    todo = deque([(set(["start"]), None, "start")])
    while len(todo) > 0:
        trail, dupe, cur = todo.pop()
        for x in paths[cur]:
            if x != "start":
                if x == "end":
                    trails += 1
                elif x.lower() == x:
                    if mode == 1:
                        if x not in trail:
                            todo.append((trail | set([x]), dupe, x))
                    else:
                        if x not in trail:
                            todo.append((trail | set([x]), dupe, x))
                        else:
                            if dupe is None:
                                todo.append((trail, x, x))
                else:
                    todo.append((trail | set([x]), dupe, x))

    return trails

def test(log):
    values = log.decode_values("""
        start-A
        start-b
        A-c
        A-b
        b-d
        A-end
        b-end
    """)

    log.test(calc(log, values, 1), 10)
    log.test(calc(log, values, 2), 36)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))
