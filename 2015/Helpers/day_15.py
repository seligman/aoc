#!/usr/bin/env python3

import re

def get_desc():
    return 15, 'Day 15: Science for Hungry People'


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

    log.show("Best 500 calorie: %d" % (best_500,))

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
    log.show(calc(log, values))

