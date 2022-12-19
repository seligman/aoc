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

# Cache all of the answers because my solver is slow
# This will also be handy to compare answers as I test my solver
# trying to speed it up
CACHED = {
    (True, 1, 24): 9, (True, 2, 24): 12,

    (False, 1, 24): 0, (False, 2, 24): 15, (False, 3, 24): 1, (False, 4, 24): 3, (False, 5, 24): 3, 
    (False, 6, 24): 0, (False, 7, 24): 2, (False, 8, 24): 5, (False, 9, 24): 9, (False, 10, 24): 2, 
    (False, 11, 24): 5, (False, 12, 24): 0, (False, 13, 24): 0, (False, 14, 24): 1, (False, 15, 24): 0, 
    (False, 16, 24): 0, (False, 17, 24): 13, (False, 18, 24): 5, (False, 19, 24): 0, (False, 20, 24): 2, 
    (False, 21, 24): 1, (False, 22, 24): 0, (False, 23, 24): 1, (False, 24, 24): 0, (False, 25, 24): 4, 
    (False, 26, 24): 0, (False, 27, 24): 0, (False, 28, 24): 5, (False, 29, 24): 1, (False, 30, 24): 1,

    (False, 1, 32): 11, (False, 2, 32): 69, (False, 3, 32): 21,

    # Unverified
    (False, 4, 32): 28, (False, 5, 32): 31, (False, 6, 32): 8, (False, 7, 32): 35, (False, 8, 32): 42, 
    (False, 9, 32): 54, (False, 10, 32): 25, (False, 11, 32): 39, (False, 12, 32): 6, (False, 13, 32): 13, 
    (False, 14, 32): 16, (False, 15, 32): 15, (False, 16, 32): 9, (False, 17, 32): 64, (False, 18, 32): 43, 
    (False, 19, 32): 11, (False, 20, 32): 31, (False, 21, 32): 22, (False, 22, 32): 11, (False, 23, 32): 18, 
    (False, 24, 32): 15, (False, 25, 32): 39, (False, 26, 32): 11, (False, 27, 32): 13, (False, 28, 32): 38, 
    (False, 29, 32): 21, (False, 30, 32): 26,
}

def solve(cost):
    cost = Costs(*cost)
    cached_key = (cost.is_test, cost.blueprint, cost.time)
    if CACHED is not None:
        if cached_key in CACHED:
            return CACHED[cached_key], tuple(cost)

    todo = deque([State(1, 0, 0, 0, 0, 0, 0, 0, cost.time)])
    seen = set()

    max_ore = max(cost.ore_for_ore, cost.ore_for_clay, cost.ore_for_obsidian, cost.ore_for_geode)
    max_clay = cost.clay_for_obsidian
    max_obsidian = cost.obsidian_for_geode

    best = 0
    steps = 0

    while len(todo) > 0:
        cur = todo.popleft()

        key = (
            cur.ore_robots, 
            cur.clay_robots, 
            cur.obsidian_robots, 
            cur.geode_robots, 
            min(cur.ore, max_ore*3), 
            min(cur.clay, max_clay*9), 
            min(cur.obsidian, max_obsidian*3),
        )

        if key not in seen:
            seen.add(key)
            steps += 1
            old_state = cur
            cur = cur._replace(time=cur.time-1)

            if 0 < cur.ore_robots : cur = cur._replace(ore=cur.ore + cur.ore_robots)
            if 0 < cur.clay_robots : cur = cur._replace(clay=cur.clay + cur.clay_robots)
            if 0 < cur.obsidian_robots : cur = cur._replace(obsidian=cur.obsidian + cur.obsidian_robots)
            if 0 < cur.geode_robots: cur = cur._replace(geode=cur.geode + cur.geode_robots)

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

    # Cache these, because I can't find a faster path yet
    print("    " + str(cached_key) + ": " + str(best) + ",")
    
    return best, tuple(cost)

def calc(log, values, mode, is_test=False):
    from parsers import get_ints

    time = 24 if mode == 1 else 32
    costs = [Costs(*(get_ints(x) + [time, is_test, None])) for x in values]
    if mode == 2:
        costs = costs[:3]

    if CACHED is not None:
        for i, cost in enumerate(costs):
            key = (is_test, cost.blueprint, cost.time)
            if key in CACHED:
                costs[i] = cost._replace(best=CACHED[key])

    todo = [x for x in costs if x.best is None]
    if len(todo) > 0:
        if len(todo) == 1:
            best, cost = solve(todo[0])
            cost = Costs(*cost)
            costs = [(x._replace(best=best) if cost.blueprint == x.blueprint else x) for x in costs]
        else:
            with multiprocessing.Pool() as pool:
                for best, cost in pool.imap_unordered(solve, todo):
                    cost = Costs(*cost)
                    costs = [(x._replace(best=best) if cost.blueprint == x.blueprint else x) for x in costs]
    
    if mode == 1:
        ret = 0
        for cost in costs:
            ret += cost.blueprint * cost.best
    else:
        ret = 1
        for cost in costs:
            ret *= cost.best

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
    if fn is None: print("Unable to find input file!"); exit(1)
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
