#!/usr/bin/env python

import itertools

def get_desc():
    return 21, 'Day 21: RPG Simulator 20XX'


def calc(values):
    boss = [100, 8, 2]
    player = [100, 0, 0]

    weapons = [
        [8, 4, 0],
        [10, 5, 0],
        [25, 6, 0],
        [40, 7, 0],
        [74, 8, 0],
    ]

    armor = [
        [0, 0, 0],
        [13, 0, 1],
        [31, 0, 2],
        [53, 0, 3],
        [75, 0, 4],
        [102, 0, 5],
    ]

    rings = [
        [0, 0, 0],
        [0, 0, 0],
        [25, 1, 0],
        [50, 2, 0],
        [100, 3, 0],
        [20, 0, 1],
        [40, 0, 2],
        [80, 0, 3],
    ]

    best_cost = None
    worst_cost = None

    for a in weapons:
        for b in armor:
            for c in itertools.combinations(rings, 2):
                tools = [a] + [b] + list(c)
                cost = sum([x[0] for x in tools])
                player_temp = player[:]
                boss_temp = boss[:]
                player_temp[1] += sum([x[1] for x in tools])
                player_temp[2] += sum([x[2] for x in tools])

                while True:
                    boss_temp[0] -= max(1, player_temp[1] - boss_temp[2])
                    if boss_temp[0] <= 0:
                        if best_cost is None or cost < best_cost:
                            best_cost = cost
                        break
                    player_temp[0] -= max(1, boss_temp[1] - player_temp[2])
                    if player_temp[0] <= 0:
                        if worst_cost is None or cost > worst_cost:
                            worst_cost = cost
                        break
                        
    return "Best: %d, Worst %d" % (best_cost, worst_cost)


def test(log):
    return True


def run(log, values):
    log.show(calc(values))
