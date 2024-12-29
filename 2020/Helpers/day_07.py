#!/usr/bin/env python3

import re

DAY_NUM = 7
DAY_DESC = 'Day 7: Handy Haversacks'

def calc(log, values, mode):
    rules = {}

    def fix(value):
        value = value.strip()
        if value.endswith("bags"):
            value = value[:-1]
        return value

    r = re.compile("(?P<color>[a-z ]+) contains{0,1} (?P<in>.*)")
    rule = re.compile("(?P<num>[0-9]+) (?P<color>.*)")
    for value in values:
        if value.endswith("."):
            value = value[:-1]
        m = r.search(value)
        color = fix(m.group("color"))
        if m.group("in") == "no other bags":
            rules[color] = [(0, "END")]
        else:
            rules[color] = []
            for x in m.group("in").split(","):
                m = rule.search(x.strip())
                rules[color].append((int(m.group("num")), fix(m.group("color"))))

    if mode == 1:
        possible = set(["shiny gold bag"])
        while True:
            check = len(possible)
            for key in rules:
                for rule in rules[key]:
                    if rule[1] in possible:
                        possible.add(key)
            if check == len(possible):
                break
        possible.remove("shiny gold bag")
        return len(possible)
    else:
        todo = [(1,) + x for x in rules["shiny gold bag"]]
        bags = 0
        while len(todo) > 0:
            mult, count, name = todo.pop(0)
            bags += mult * count
            if name != "END":
                todo += [(mult * count,) + x for x in rules[name]]
        return bags


def test(log):
    values = log.decode_values("""
        light red bags contain 1 bright white bag, 2 muted yellow bags.
        dark orange bags contain 3 bright white bags, 4 muted yellow bags.
        bright white bags contain 1 shiny gold bag.
        muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
        shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
        dark olive bags contain 3 faded blue bags, 4 dotted black bags.
        vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
        faded blue bags contain no other bags.
        dotted black bags contain no other bags.
    """)

    log.test(calc(log, values, 1), 4)

    values = log.decode_values("""
        shiny gold bags contain 2 dark red bags.
        dark red bags contain 2 dark orange bags.
        dark orange bags contain 2 dark yellow bags.
        dark yellow bags contain 2 dark green bags.
        dark green bags contain 2 dark blue bags.
        dark blue bags contain 2 dark violet bags.
        dark violet bags contain no other bags.
    """)
    log.test(calc(log, values, 2), 126)

def run(log, values):
    log(f"Part 1: {calc(log, values, 1)}")
    log(f"Part 2: {calc(log, values, 2)}")

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2020/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
