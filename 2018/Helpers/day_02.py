#!/usr/bin/env python3

DAY_NUM = 2
DAY_DESC = 'Day 2: Inventory Management System'


def calc(log, values):
    hits = {}
    valid = []
    for cur_value in values:
        counts = {}
        for cur in cur_value:
            counts[cur] = counts.get(cur, 0) + 1
        seen = set()
        for value in counts.values():
            if value > 1 and value not in seen:
                hits[value] = hits.get(value, 0) + 1
                seen.add(value)
        if (2 in seen) or (3 in seen):
            valid.append(cur_value)

    found = None
    for i in range(len(valid)):
        if found is not None:
            break
        for j in range(i + 1, len(valid)):
            if found is not None:
                break
            matches = ""
            for x in range(len(valid[i])):
                if valid[i][x] == valid[j][x]:
                    matches += valid[i][x]
            if len(matches) == len(valid[i]) - 1:
                log.show(matches)
                found = matches

    ret = 1
    for value in hits.values():
        ret *= value

    return ret


def test(log):
    test = [
        "abcdef",
        "bababc",
        "abbcde",
        "abcccd",
        "aabcdd",
        "abcdee",
        "ababab",
    ]

    if calc(log, test) != 12:
        return False

    return True


def run(log, values):
    log.show(calc(log, values))
