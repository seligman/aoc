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
State = namedtuple('State', [
    'ore_robots', 'clay_robots', 'obsidian_robots', 'geode_robots',
    'ore', 'clay', 'obsidian', 'geode',
    'time',
])

def solve(cost):
    cost = Costs(*cost)

    todo = deque([State(1, 0, 0, 0, 0, 0, 0, 0, cost.time)])

    max_ore = max(cost.ore_for_ore, cost.ore_for_clay, cost.ore_for_obsidian, cost.ore_for_geode)
    max_clay = cost.clay_for_obsidian
    max_obsidian = cost.obsidian_for_geode

    max_ore = max_ore * 2 - 1
    max_clay = max_clay * 2 - 1
    max_obsidian = max_obsidian * 2 - 1

    best = 0
    steps = 0

    seen = set()

    while len(todo) > 0:
        cur = todo.popleft()

        key = (
            cur.ore_robots, 
            cur.clay_robots, 
            cur.obsidian_robots, 
            cur.geode, 
            min(cur.ore, max_ore),
            min(cur.clay, max_clay),
            min(cur.obsidian, max_obsidian),
        )

        if key not in seen:
            seen.add(key)
            steps += 1
            old_state = cur
            cur = cur._replace(time=cur.time-1)

            cur = cur._replace(ore=cur.ore + cur.ore_robots)
            cur = cur._replace(clay=cur.clay + cur.clay_robots)
            cur = cur._replace(obsidian=cur.obsidian + cur.obsidian_robots)
            cur = cur._replace(geode=cur.geode + cur.geode_robots)

            if cur.time == 0:
                if cur.geode > best:
                    best = cur.geode
            else:
                if old_state.ore >= cost.ore_for_ore and cur.ore_robots < max_ore:
                    todo.append(cur._replace(
                        ore=cur.ore - cost.ore_for_ore, 
                        ore_robots=cur.ore_robots + 1,
                    ))
                if old_state.ore >= cost.ore_for_clay and cur.clay_robots < max_clay:
                    todo.append(cur._replace(
                        ore=cur.ore - cost.ore_for_clay, 
                        clay_robots=cur.clay_robots + 1,
                    ))
                if old_state.ore >= cost.ore_for_obsidian and old_state.clay >= cost.clay_for_obsidian:
                    todo.append(cur._replace(
                        ore=cur.ore - cost.ore_for_obsidian, 
                        clay=cur.clay - cost.clay_for_obsidian,
                        obsidian_robots=cur.obsidian_robots + 1,
                    ))
                if old_state.ore >= cost.ore_for_geode and old_state.obsidian >= cost.obsidian_for_geode:
                    todo.append(cur._replace(
                        ore=cur.ore - cost.ore_for_geode, 
                        obsidian=cur.obsidian - cost.obsidian_for_geode,
                        geode_robots=cur.geode_robots + 1,
                    ))

                todo.append(cur)

    return best, tuple(cost)

def calc(log, values, mode, is_test=False):
    from parsers import get_ints

    time = 24 if mode == 1 else 32
    costs = [Costs(*(get_ints(x) + [time, is_test, None])) for x in values]

    with multiprocessing.Pool() as pool:
        costs = [tuple(x) for x in costs]
        if mode == 1:
            ret = 0
        else:
            ret = 1
            costs = costs[:3]

        for solution, cost in pool.imap_unordered(solve, costs):
            cost = Costs(*cost)
            if mode == 1:
                ret += cost.blueprint * solution
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
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
