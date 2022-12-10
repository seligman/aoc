#!/usr/bin/env python3

DAY_NUM = 9
DAY_DESC = 'Day 9: Stream Processing'


def parse_garb(value, i, removed):
    escape = False
    while True:
        i[0] += 1
        if escape:
            escape = False
        else:
            if value[i[0]] == "!":
                escape = True
            elif value[i[0]] == ">":
                return
            else:
                removed[0] += 1


def parse(value, i, level, removed):
    ret = level
    while i[0] < len(value):
        i[0] += 1
        if value[i[0]] == "{":
            ret += parse(value, i, level + 1, removed)
        elif value[i[0]] == "<":
            parse_garb(value, i, removed)
        elif value[i[0]] == "}":
            return ret


def calc(log, values):
    removed = [0]
    ret = parse(values[0], [0], 1, removed)
    log.show("Removed: " + str(removed[0]))
    return ret


def test(log):
    values = [
        "{{<!!>},{<!!>},{<!!>},{<!!>}}",
    ]

    if calc(log, values) == 9:
        return True
    else:
        return False


def run(log, values):
    log.show(calc(log, values))
