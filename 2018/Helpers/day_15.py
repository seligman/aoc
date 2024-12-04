#!/usr/bin/env python3

from collections import defaultdict

DAY_NUM = 15
DAY_DESC = 'Day 15: Beverage Bandits'


class Creature:
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.attack = 3
        self.hp = 200
        self.name = name
        self.dead = False


def calc(values, elve_power):
    creatures = {}
    counts = defaultdict(int)

    for y in range(len(values)):
        values[y] = list(values[y])
        for x in range(len(values[y])):
            if values[y][x] in {"G", "E"}:
                creature = Creature(x, y, values[y][x])
                creatures[(x, y)] = creature
                counts[creature.name] += 1
                if values[y][x] == "E":
                    creature.attack = elve_power

    start_elves = counts['E']

    rounds = 0
    while counts['G'] > 0 and counts['E'] > 0:
        rounds += 1
        units = list(creatures.values())
        units.sort(key=lambda x: (x.y, x.x))
        for creature in units:
            if not creature.dead:
                if counts['G'] == 0 or counts['E'] == 0:
                    rounds -= 1
                    break
                skip_move = False
                for off in ((0, -1), (-1, 0), (1, 0), (0, 1)):
                    x = creature.x + off[0]
                    y = creature.y + off[1]
                    if (x, y) in creatures and creatures[(x, y)].name != creature.name:
                        skip_move = True
                        break

                if not skip_move:
                    paths = [
                        {
                            'x': creature.x,
                            'y': creature.y,
                            'prev': [],
                        }
                    ]
                    moved = False
                    used = set()
                    while len(paths) > 0:
                        if moved:
                            break
                        new_items = []
                        for path in paths:
                            if moved:
                                break
                            for off in ((0, -1), (-1, 0), (1, 0), (0, 1)):
                                x = path['x'] + off[0]
                                y = path['y'] + off[1]
                                if ((x, y) not in used) and (values[y][x] == "."):
                                    new_items.append({
                                        'x': x,
                                        'y': y,
                                        'prev': [z for z in path['prev']] + [(x, y)],
                                    })
                                    used.add((x, y))
                                elif (values[y][x] in {"E", "G"}) and (values[y][x] != creature.name):
                                    path['prev'].append((x, y))
                                    off = path['prev'][0]

                                    values[off[1]][off[0]] = creature.name
                                    values[creature.y][creature.x] = "."
                                    del creatures[(creature.x, creature.y)]
                                    creature.x = off[0]
                                    creature.y = off[1]
                                    creatures[(creature.x, creature.y)] = creature

                                    moved = True
                                    break
                        paths = new_items

                best_hp = None
                best_off = None
                for off in ((0, -1), (-1, 0), (1, 0), (0, 1)):
                    x = creature.x + off[0]
                    y = creature.y + off[1]
                    if (x, y) in creatures and creatures[(x, y)].name != creature.name:
                        if best_hp is None or best_hp > creatures[(x, y)].hp:
                            best_hp = creatures[(x, y)].hp
                            best_off = (x, y)
                if best_off is not None:
                    x, y = best_off
                    creatures[(x, y)].hp -= creature.attack
                    if creatures[(x, y)].hp <= 0:
                        creatures[(x, y)].dead = True
                        counts[creatures[(x, y)].name] -= 1
                        values[y][x] = "."
                        del creatures[(x, y)]

    return rounds * sum([x.hp for x in creatures.values()]), counts['E'], start_elves


def test(log):
    tests = [
        [
            [
                "#######",
                "#.G...#",
                "#...EG#",
                "#.#.#G#",
                "#..G#E#",
                "#.....#",
                "#######",
            ], 27730
        ],
        [
            [
                "#######",
                "#G..#E#",
                "#E#E.E#",
                "#G.##.#",
                "#...#E#",
                "#...E.#",
                "#######",
            ], 36334
        ],
        [
            [
                "#######",
                "#E..EG#",
                "#.#G.E#",
                "#E.##E#",
                "#G..#.#",
                "#..E#.#",
                "#######",
            ], 39514
        ],
        [
            [
                "#######",
                "#E.G#.#",
                "#.#G..#",
                "#G.#.G#",
                "#G..#.#",
                "#...E.#",
                "#######",
            ], 27755
        ],
        [
            [
                "#######",
                "#.E...#",
                "#.#..G#",
                "#.###.#",
                "#E#G#G#",
                "#...#G#",
                "#######",
            ], 28944
        ],
        [
            [
                "#########",
                "#G......#",
                "#.E.#...#",
                "#..##..G#",
                "#...##..#",
                "#...#...#",
                "#.G...G.#",
                "#.....G.#",
                "#########",
            ], 18740
        ],
    ]

    test_number = 0
    for values, expected in tests:
        test_number += 1
        if calc(values, 3)[0] != expected:
            log("Test number %d FAILED" % (test_number,))
            return False

    return True


def run(log, values):
    elve_power = 3
    while True:
        ret = calc(values[:], elve_power)
        log("%d == %d of %d" % (ret[0], ret[1], ret[2]))
        if ret[1] == ret[2]:
            break
        elve_power += 1

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2018/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
