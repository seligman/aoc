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

    rounds = 0
    starting_elves = counts['E']

    while counts['G'] > 0 and counts['E'] > 0:
        rounds += 1
        units = list(sorted(creatures.values(), key=lambda x: (x.y, x.x)))
        # for row in values:
        #     print("".join(row))
        # print(str(rounds) + " -- " + ", ".join(f"{x.x}-{x.y}-{x.name}-{x.hp}" for x in units))
        for creature in units:
            if counts['G'] == 0 or counts['E'] == 0:
                rounds -= 1
                break
            if not creature.dead:
                skip_move = False
                for off in ((0, -1), (-1, 0), (1, 0), (0, 1)):
                    x = creature.x + off[0]
                    y = creature.y + off[1]
                    if (x, y) in creatures and creatures[(x, y)].name != creature.name:
                        skip_move = True
                        break

                if not skip_move:
                    targets = []
                    for other in creatures.values():
                        if other.name != creature.name:
                            for off in ((0, -1), (-1, 0), (1, 0), (0, 1)):
                                x = other.x + off[0]
                                y = other.y + off[1]
                                if values[y][x] == ".":
                                    targets.append((x, y))

                    paths = []
                    for target_x, target_y in targets:
                        todo = [(creature.x, creature.y, [])]
                        used = set()
                        while len(todo) > 0:
                            sx, sy, path = todo.pop(0)
                            for off in ((0, -1), (-1, 0), (1, 0), (0, 1)):
                                x = sx + off[0]
                                y = sy + off[1]
                                if (x, y) not in used:
                                    used.add((x, y))
                                    if (x, y) == (target_x, target_y):
                                        todo = []
                                        paths.append(path + [(x, y)])
                                    else:
                                        if values[y][x] == ".":
                                            todo.append((x, y, path + [(x, y)]))

                    if len(paths) > 0:
                        paths.sort(key=lambda x: len(x), reverse=False)
                        paths = [x for x in paths if len(x) == len(paths[0])]
                        paths.sort(key=lambda x: (x[-1][1], x[-1][0]))
                        path = paths[0]
                        x, y = path[0]
                        values[y][x] = values[creature.y][creature.x]
                        values[creature.y][creature.x] = "."
                        del creatures[(creature.x, creature.y)]
                        creatures[(x, y)] = creature
                        creature.x = x
                        creature.y = y

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

    # print(counts)
    # for cur in creatures.values():
    #     print(cur.name, cur.hp, cur.dead)
    # print("final")
    # for y, row in enumerate(values):
    #     print("".join(row) + " -- " + f" - ".join(f"{x.hp}" for x in creatures.values() if x.y == y))
    # print(str(rounds) + " -- " + ", ".join(f"{x.x}-{x.y}-{x.name}-{x.hp}" for x in units))

    return rounds * sum([x.hp for x in creatures.values()]), counts['E'], starting_elves

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
    failures = 0
    for values, expected in tests:
        test_number += 1
        actual = calc(values, 3)[0]
        if actual != expected:
            failures += 1
            log("Test number %d FAILED, got %d, expected %d" % (test_number, actual, expected))
            break
        else:
            log("Test number %d worked, got %d" % (test_number, actual))
        # break
    if failures > 0:
        raise Exception()
    return True

def run(log, values):
    ret = calc(values[:], 3)
    log("Part 1: %d" % (ret[0],))

    elve_power = 3
    skip = 32
    while True:
        ret = calc(values[:], elve_power)
        if ret[2] - ret[1] == 1:
            log("  With elf power of %d, there was %d loss" % (elve_power, ret[2] - ret[1]))
        else:
            log("  With elf power of %d, there were %d losses" % (elve_power, ret[2] - ret[1]))
        if ret[1] == ret[2]:
            if skip == 1:
                log("Part 2: %d" % (ret[0],))
                break
            else:
                skip //= 2
                elve_power -= skip
        else:
            elve_power += skip

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
