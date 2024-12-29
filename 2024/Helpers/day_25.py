#!/usr/bin/env python3

DAY_NUM = 25
DAY_DESC = 'Day 25: Code Chronicle'

def calc(log, values, mode):
    from grid import Grid, Point

    temp = [[]]
    for row in values:
        if len(row) == 0:
            temp.append([])
        else:
            temp[-1].append(row)

    temp = [Grid.from_text(x) for x in temp]
    locks, keys = [], []
    for cur in temp:
        if cur[0, 0] == "#":
            locks.append(cur)
        else:
            keys.append(cur)

    ret = 0
    for lock in locks:
        for key in keys:
            fit = True
            for xy in lock.xy_range():
                if lock[xy] == "#" and key[xy] == "#":
                    fit = False
            if fit:
                ret += 1

    # TODO
    return ret

def test(log):
    values = log.decode_values("""
        #####
        .####
        .####
        .####
        .#.#.
        .#...
        .....

        #####
        ##.##
        .#.##
        ...##
        ...#.
        ...#.
        .....

        .....
        #....
        #....
        #...#
        #.#.#
        #.###
        #####

        .....
        .....
        #.#..
        ###..
        ###.#
        ###.#
        #####

        .....
        .....
        .....
        #....
        #.#..
        #.#.#
        #####
    """)

    log.test(calc(log, values, 1), '3')
    # log.test(calc(log, values, 2), 'TODO')

def run(log, values):
    log(f"Part 1: {calc(log, values, 1)}")
    # log(f"Part 2: {calc(log, values, 2)}")

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2024/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
