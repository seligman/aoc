#!/usr/bin/env python

from collections import defaultdict

def get_desc():
    return 6, 'Day 6: Chronal Coordinates'


def calc(log, values, max_dist):
    values = [[int(y) for y in x.split(",")] for x in values]
    max_x = max([x[0] for x in values])
    max_y = max([x[1] for x in values])

    edge = set()
    counts = defaultdict(int)
    size_of_safe = 0

    for x in range(0, max_x + 2):
        for y in range(0, max_y + 2):
            i = 0
            best_i = 0
            best_seen = 0
            best_val = None
            total_dist = 0
            for test_x, test_y in values:
                dist = abs(x - test_x) + abs(y - test_y)
                total_dist += dist

                if best_val is None or dist < best_val:
                    best_val = dist
                    best_i = i
                    best_seen = 0
                if best_val == dist:
                    best_seen += 1
                i += 1

            if total_dist < max_dist:
                size_of_safe += 1

            if best_seen == 1:
                if x == 0 or y == 0 or x == max_x + 1 or y == max_y + 1:
                    edge.add(best_i)
                else:
                    counts[best_i] += 1

    for i in edge:
        del counts[i]

    ids = list(counts)
    ids.sort(key=lambda x:counts[x], reverse=True)

    log.show("Size of safe area: %d" % (size_of_safe,))

    return counts[ids[0]]


def test(log):
    values = [
        "1, 1",
        "1, 6",
        "8, 3",
        "3, 4",
        "5, 5",
        "8, 9",
    ]

    if calc(log, values, 32) == 17:
        return True
    else:
        return False


def run(log, values):
    log.show(calc(log, values, 10000))
