#!/usr/bin/env python3

import re

DAY_NUM = 15
DAY_DESC = 'Day 15: Science for Hungry People'


class Ingredient:
    def __init__(self, name, capacity, durability, flavor, texture, calories):
        self.name = name
        self.capacity = int(capacity)
        self.durability = int(durability)
        self.flavor = int(flavor)
        self.texture = int(texture)
        self.calories = int(calories)
        self.teaspoons = 1


def enum_all(score, values):
    if len(values) == 1:
        values[0].teaspoons = score
        yield True
    else:
        for i in range(1, score - len(values) + 2):
            values[0].teaspoons = i
            for _ in enum_all(score - i, values[1:]):
                yield True


def calc(log, values):
    r = re.compile("(.*): capacity (.*), durability (.*), flavor (.*), texture (.*), calories (.*)")
    ingredients = []

    for cur in values:
        m = r.search(cur)
        ingredients.append(Ingredient(*m.groups()))

    best_score = 0
    best_500 = 0

    for _ in enum_all(100, ingredients):
        score = max(0, sum([x.capacity * x.teaspoons for x in ingredients]))
        score *= max(0, sum([x.durability * x.teaspoons for x in ingredients]))
        score *= max(0, sum([x.flavor * x.teaspoons for x in ingredients]))
        score *= max(0, sum([x.texture * x.teaspoons for x in ingredients]))

        if score > best_score:
            best_score = score

        if score > best_500:
            if sum([x.calories * x.teaspoons for x in ingredients]) == 500:
                best_500 = score

    log("Best 500 calorie: %d" % (best_500,))

    return best_score


def test(log):
    values = [
        "Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8",
        "Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3",
    ]

    if calc(log, values) == 62842880:
        return True
    else:
        return False


def run(log, values):
    log(calc(log, values))


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
