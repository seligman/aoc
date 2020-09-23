#!/usr/bin/env python

import itertools

def get_desc():
    return 24, 'Day 24: It Hangs in the Balance'


def get_all(values, target, invalid):
    values = set(values)
    for cur in invalid:
        values.remove(cur)
    for i in range(len(values)):
        for test in itertools.combinations(values, i + 1):
            if sum(test) == target:
                yield test


def calc(values, include_trunk):
    values = [int(x) for x in values]
    total_weight = sum(values)
    group_weight = total_weight / (4 if include_trunk else 3)

    best_count = len(values)
    best_entangle = 0

    for group_1 in get_all(values, group_weight, []):
        if len(group_1) > best_count:
            break

        entangle = 1
        for cur in group_1:
            entangle *= cur
        if entangle < best_entangle:
            best_entangle = entangle

        skip = False
        if len(group_1) == best_count:
            if entangle >= best_entangle:
                skip = True

        if not skip:
            any_valid = False
            for group_2 in get_all(values, group_weight, group_1):
                for group_3 in get_all(values, group_weight, group_1 + group_2):
                    if include_trunk:
                        for _group_4 in get_all(values, group_weight, group_1 + group_2 + group_3):
                            any_valid = True
                            break
                        if any_valid:
                            break
                    else:
                        any_valid = True
                        break
                if any_valid:
                    break

            if any_valid:
                if len(group_1) < best_count:
                    best_count = len(group_1)
                    best_entangle = entangle
                elif len(group_1) == best_count:
                    best_entangle = entangle

    return best_entangle


def test(log):
    values = [
        "1",
        "2",
        "3",
        "4",
        "5",
        "7",
        "8",
        "9",
        "10",
        "11",
    ]

    log.show("With trunk: " + str(calc(values, True)))
    if calc(values, False) == 99:
        return True
    else:
        return False


def run(log, values):
    log.show("No trunk: " + str(calc(values, False)))
    log.show("With trunk: " + str(calc(values, True)))
