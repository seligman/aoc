#!/usr/bin/env python3

DAY_NUM = 19
DAY_DESC = 'Day 19: A Series of Tubes'


def calc(log, values):
    y = 0
    for x in range(len(values[0])):
        if values[0][x] == "|":
            break

    dx, dy = 0, 1
    ret = ""
    steps = 0

    while True:
        x, y = x + dx, y + dy
        steps += 1

        if values[y][x] == "+":
            for ox, oy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                if (ox, oy) != (-dx, -dy) and values[y + oy][x + ox] != ' ':
                    dx, dy = ox, oy
                    break
        elif values[y][x] == " ":
            break
        elif values[y][x] not in {"-", "|"}:
            ret += values[y][x]

    log.show("Steps: " + str(steps))

    return ret


def test(log):
    values = [
        "     |          ",
        "     |  +--+    ",
        "     A  |  C    ",
        " F---|----E|--+ ",
        "     |  |  |  D ",
        "     +B-+  +--+ ",
        "                ",
    ]

    if calc(log, values) == "ABCDEF":
        return True
    else:
        return False


def run(log, values):
    log.show(calc(log, values))
