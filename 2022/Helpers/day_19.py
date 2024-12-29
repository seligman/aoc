#!/usr/bin/env python3

DAY_NUM = 19
DAY_DESC = 'Day 19: Not Enough Minerals'

from collections import deque, namedtuple
import multiprocessing

Costs = namedtuple("Costs", [
    "blueprint", 
    "ore_for_ore", 
    "ore_for_clay", 
    "ore_for_obsidian", "clay_for_obsidian",
    "ore_for_geode", "obsidian_for_geode",
    "time", "is_test", "best",
])

def solve(cost):
    cost = Costs(*cost)

    resources = {"ore": 0, "clay": 0, "obsidian": 0, "geode": 0}
    robots = {"ore": 1, "clay": 0, "obsidian": 0, "geode": 0}
    maxes = {
        "ore": max(cost.ore_for_ore, cost.ore_for_clay, cost.ore_for_obsidian, cost.ore_for_geode),
        "clay": cost.clay_for_obsidian,
        "obsidian": cost.obsidian_for_geode,
        "geode": 9999999,
    }
    cost_map = {
        "ore": {"ore": cost.ore_for_ore},
        "clay": {"ore": cost.ore_for_clay},
        "obsidian": {"ore": cost.ore_for_obsidian, "clay": cost.clay_for_obsidian},
        "geode": {"ore": cost.ore_for_geode, "obsidian": cost.obsidian_for_geode},
    }

    time = cost.time
    best = 0
    todo = deque([(time, resources, robots, None)])

    while len(todo) > 0:
        time, resources, robots, last = todo.pop()

        if time == 0:
            best = max(best, resources["geode"])
            continue

        if best - resources["geode"] >= (time * (2 * robots["geode"] + time - 1)) // 2:
            continue

        time -= 1
        wait = False

        next_resources = {t: v + robots[t] for t, v in resources.items()}
        for cost_source, cost_items in cost_map.items():
            if cost_source != "geode" and robots[cost_source] * time + resources[cost_source] > maxes[cost_source] * time:
                continue

            if (last is None or last == cost_source) and all(v <= resources[t] - robots[t] for t, v in cost_items.items()):
                continue

            if any(resources[t] < v for t, v in cost_items.items()):
                wait = wait or all(robots[t] > 0 for t in cost_items.keys())
                continue

            copy_resources = {t: v - cost_items.get(t, 0) for t, v in next_resources.items()}
            next_robots = {t: v + int(t == cost_source) for t, v in robots.items()}

            todo.append((time, copy_resources, next_robots, cost_source))

        if wait:
            todo.append((time, next_resources, robots, None))

    return best, cost.blueprint

def calc(log, values, mode, is_test=False, pool=None):
    from parsers import get_ints

    time = 24 if mode == 1 else 32
    costs = [Costs(*(get_ints(x) + [time, is_test, None])) for x in values]

    costs = [tuple(x) for x in costs]
    if mode == 1:
        ret = 0
    else:
        ret = 1
        costs = costs[:3]

    results = []
    if pool is None:
        for cost in costs:
            results.append(solve(cost))
    else:
        for result in pool.imap_unordered(solve, costs):
            results.append(result)
    
    for solution, blueprint in results:
        if mode == 1:
            ret += blueprint * solution
        else:
            ret *= solution

    return ret

def test(log):
    values = log.decode_values("""
        Blueprint 1:
          Each ore robot costs 4 ore.
          Each clay robot costs 2 ore.
          Each obsidian robot costs 3 ore and 14 clay.
          Each geode robot costs 2 ore and 7 obsidian.
        
        Blueprint 2:
          Each ore robot costs 2 ore.
          Each clay robot costs 3 ore.
          Each obsidian robot costs 3 ore and 8 clay.
          Each geode robot costs 3 ore and 12 obsidian.
    """)

    temp = [""]
    for row in values:
        if len(row.strip()) == 0:
            temp.append("")
        else:
            temp[-1] = " ".join([temp[-1], row.strip()])
    values = temp

    log.test(calc(log, values, 1, is_test=True), 33)
    log.test(calc(log, values, 2, is_test=True), 3472)

def run(log, values):
    with multiprocessing.Pool() as pool:
        log(f"Part 1: {calc(log, values, 1, pool=pool)}")
        log(f"Part 2: {calc(log, values, 2, pool=pool)}")

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2022/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
