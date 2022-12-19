#!/usr/bin/env python3

DAY_NUM = 19
DAY_DESC = 'Day 19: Not Enough Minerals'

from collections import deque, namedtuple

def solve(cost, T):
    best = 0

    # ore, clay, obsidian, geodes, ore_robot, clay_robot, obsidian_robot, geode_robot, time
    todo = deque([(0, 0, 0, 0, 1, 0, 0, 0, T)])
    used = set()
    while todo:
        ore, clay, obsidian, geodes, ore_robot, clay_robot, obsidian_robot, geode_robot, time = todo.popleft()

        best = max(best, geodes)
        if time==0:
            continue

        max_ore = max([cost.ore, cost.clay, cost.obsidian_ore, cost.geode_ore])
        if ore_robot >= max_ore:
            ore_robot = max_ore
        if clay_robot>=cost.obsidian_clay:
            clay_robot = cost.obsidian_clay
        if obsidian_robot>=cost.geode_clay:
            obsidian_robot = cost.geode_clay
        if ore >= time * max_ore - ore_robot * (time - 1):
            ore = time * max_ore - ore_robot * (time - 1)
        if clay >= time * cost.obsidian_clay - clay_robot * (time - 1):
            clay = time * cost.obsidian_clay - clay_robot * (time - 1)
        if obsidian>=time * cost.geode_clay - obsidian_robot * (time - 1):
            obsidian = time * cost.geode_clay - obsidian_robot * (time - 1)

        state = (ore, clay, obsidian, geodes, ore_robot, clay_robot, obsidian_robot, geode_robot, time)

        if state not in used:
            used.add(state)

            todo.append((
                ore + ore_robot,
                clay + clay_robot,
                obsidian + obsidian_robot,
                geodes + geode_robot,
                ore_robot,
                clay_robot,
                obsidian_robot,
                geode_robot,
                time - 1,
            ))
            if ore>=cost.ore:
                todo.append((
                    ore - cost.ore + ore_robot,
                    clay + clay_robot,
                    obsidian + obsidian_robot,
                    geodes + geode_robot,
                    ore_robot + 1,
                    clay_robot,
                    obsidian_robot,
                    geode_robot,
                    time - 1,
                ))
            if ore>=cost.clay:
                todo.append((
                    ore - cost.clay + ore_robot, 
                    clay + clay_robot,
                    obsidian + obsidian_robot,
                    geodes + geode_robot,
                    ore_robot,
                    clay_robot + 1,
                    obsidian_robot,
                    geode_robot,
                    time - 1,
                ))
            if ore>=cost.obsidian_ore and clay>=cost.obsidian_clay:
                todo.append((
                    ore - cost.obsidian_ore + ore_robot,
                    clay - cost.obsidian_clay + clay_robot,
                    obsidian + obsidian_robot,
                    geodes + geode_robot,
                    ore_robot,
                    clay_robot,
                    obsidian_robot + 1,
                    geode_robot,
                    time - 1,
                ))
            if ore>=cost.geode_ore and obsidian>=cost.geode_clay:
                todo.append((
                    ore - cost.geode_ore + ore_robot,
                    clay + clay_robot,
                    obsidian - cost.geode_clay + obsidian_robot,
                    geodes + geode_robot,
                    ore_robot,
                    clay_robot,
                    obsidian_robot,
                    geode_robot + 1,
                    time - 1,
                ))

    return best

def calc(log, values, mode):
    from parsers import get_ints

    Costs = namedtuple("Costs", ["id", "ore", "clay", "obsidian_ore", "obsidian_clay", "geode_ore", "geode_clay"])
    costs = [Costs(*get_ints(x)) for x in values]

    if mode == 1:
        ret = 0
        for cost in costs:
            ret += cost.id * solve(cost, 24)
    
    if mode == 2:
        ret = 1
        for cost in costs[:3]:
            ret *= solve(cost, 32)
    return ret

def test(log):
    values = log.decode_values("""
        Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
        Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
    """)

    log.test(calc(log, values, 1), 33)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in [[], ["Puzzles"], ["..", "Puzzles"]]:
                cur = os.path.join(*(dn + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!"); exit(1)
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
