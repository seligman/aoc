#!/usr/bin/env python

def get_desc():
    return 18, 'Day 18: Like a GIF For Your Yard'


def calc(log, values, steps, mode):
    values = ["." * len(values[0])] + values + ["." * len(values[0])]
    values = [list("." + x + ".") for x in values]

    temp = [[x for x in y] for y in values]

    if mode == 1:
        for x in range(2):
            for y in range(2):
                values[y * (len(values) - 3) + 1][x * (len(values[0]) - 3) + 1] = "#"

    states = {"#": 1, ".": 0}
    wrap = []
    for x in range(-1, 2):
        for y in range(-1, 2):
            if x != 0 or y != 0:
                wrap.append((x, y))

    for _ in range(steps):
        for x in range(1, len(values[0])-1):
            for y in range(1, len(values)-1):
                on = 0
                for off in wrap:
                    on += states[values[y+off[1]][x+off[0]]]
                if values[y][x] == "#":
                    temp[y][x] = "#" if 2 <= on <= 3 else "."
                else:
                    temp[y][x] = "#" if on == 3 else "."

        values, temp = temp, values
        if mode == 1:
            for x in range(2):
                for y in range(2):
                    values[y * (len(values) - 3) + 1][x * (len(values[0]) - 3) + 1] = "#"

        if False:
            log.show("")
            log.show("\n".join(["".join(x) for x in values]))


    return sum([sum([states[x] for x in y]) for y in values])


def test(log):
    values = [
        ".#.#.#",
        "...##.",
        "#....#",
        "..#...",
        "#.#..#",
        "####..",
    ]

    if calc(log, values, 4, 0) == 4:
        return True
    else:
        return False


def run(log, values):
    log.show(calc(log, values, 100, 0))
    log.show(calc(log, values, 100, 1))
