#!/usr/bin/env python3

import itertools

DAY_NUM = 21
DAY_DESC = 'Day 21: RPG Simulator 20XX'


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
    log(calc(values))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2015/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
