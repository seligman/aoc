#!/usr/bin/env python

def get_desc():
    return 12, 'Day 12: Subterranean Sustainability'


def calc(log, values, generations):
    state = values[0][15:]
    seed = 0

    rules = {}
    for cur in values[2:]:
        if len(cur) > 0:
            rules[cur[0:5]] = cur[9]

    loop = ""
    loop_size = 0
    loop_left = 1
    loop_seed = 0

    while generations > 0:
        generations -= 1
        if state[0] == "#" or state[1] == "#" or state[2] == "#":
            seed -= 3
            state = "..." + state
        if state[-1] == "#" or state[-2] == "#" or state[-3] == "#":
            state += "..."

        while state[0:6] == "......":
            state = state[1:]
            seed += 1

        while state[-6:] == "......":
            state = state[0:-1]

        next_state = ".."
        for i in range(len(state)-4):
            next_state += rules.get(state[i:i+5], ".")
        next_state += ".."
        state = next_state

        score = 0
        i = seed
        for cur in state:
            if cur == "#":
                score += i
            i += 1

        loop_left -= 1
        if loop_left == 0:
            if loop == state:
                loops = generations // loop_size
                generations -= loops * loop_size
                seed += loops * (seed - loop_seed)
            else:
                loop_size += 1
                loop_left = loop_size
                loop = state
                loop_seed = seed

        if generations % 50 == 0:
            log.show("Gen: %12d, Score: %14d, State Len: %d" % (generations, score, len(state)))

    return score


def test(log):
    values = [
        "initial state: #..#.#..##......###...###",
        "",
        "...## => #",
        "..#.. => #",
        ".#... => #",
        ".#.#. => #",
        ".#.## => #",
        ".##.. => #",
        ".#### => #",
        "#.#.# => #",
        "#.### => #",
        "##.#. => #",
        "##.## => #",
        "###.. => #",
        "###.# => #",
        "####. => #",
    ]

    if calc(log, values, 20) == 325:
        return True
    else:
        return False


def run(log, values):
    log.show(calc(log, values, 20))
    log.show(calc(log, values, 50000000000))
