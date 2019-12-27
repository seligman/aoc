#!/usr/bin/env python

import re
import itertools
import heapq

def get_desc():
    return 11, 'Day 11: Radioisotope Thermoelectric Generators'


def correct(floor):
    if not floor or floor[-1] < 0: # no generators
        return True
    return all(-chip in floor for chip in floor if chip < 0)
    

def calc(values, extra=None):
    r = re.compile("The (.*) floor contains (.*)\\.")

    floors = []
    ids = {}
    
    for cur in values:
        floors.append([])
        m = r.search(cur)
        cur = m.group(2)
        cur = cur.replace(", and", ",")
        cur = cur.replace(" and", ",")
        if cur != "nothing relevant":
            cur = cur.split(", ")
            if len(floors) == 1 and extra is not None:
                cur += extra
            for sub in cur:
                negate = 1
                if "-compatible microchip" in sub:
                    negate = -1
                sub = sub.replace("-compatible microchip", "")
                sub = sub.replace(" generator", "")
                if sub not in ids:
                    ids[sub] = str(len(ids) + 1)
                floors[-1].append(int(ids[sub]) * negate)

    for i in range(len(floors)):
        floors[i] = tuple(sorted(floors[i]))
    initial = (0, tuple(floors))

    frontier = []
    heapq.heappush(frontier, (0, initial))
    cost_so_far = {initial: 0}

    while frontier:
        _, current = heapq.heappop(frontier)
        floor, floors = current
        if floor == 3 and all(len(f) == 0 for f in floors[:-1]):
            break

        directions = [dir for dir in (-1, 1) if 0 <= floor + dir < 4]
        moves = list(itertools.combinations(floors[floor], 2))
        moves += list(itertools.combinations(floors[floor], 1))
        for move in moves:
            for direction in directions:
                new_floors = list(floors)
                new_floors[floor] = tuple(x for x in floors[floor] if x not in move)
                new_floors[floor+direction] = tuple(sorted(floors[floor+direction] + move))

                if not correct(new_floors[floor]) or not correct(new_floors[floor+direction]):
                    continue

                next = (floor+direction, tuple(new_floors))
                new_cost = cost_so_far[current] + 1
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost - len(new_floors[3]) * 10
                    heapq.heappush(frontier, (priority, next))

    return cost_so_far[current]


def test(log):
    values = [
        "The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.",
        "The second floor contains a hydrogen generator.",
        "The third floor contains a lithium generator.",
        "The fourth floor contains nothing relevant.",
    ]

    if calc(values) == 11:
        return True
    else:
        return False


def run(log, values):
    log.show(calc(values))
    extra = [
        "an elerium generator",
        "an elerium-compatible microchip",
        "a dilithium generator",
        "a dilithium-compatible microchip",
    ]
    log.show(calc(values, extra))
