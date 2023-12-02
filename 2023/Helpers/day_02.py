#!/usr/bin/env python3

import re

DAY_NUM = 2
DAY_DESC = 'Day 2: Cube Conundrum'

def calc(log, values, mode):
    ret = 0
    for row in values:
        game_id = int(row[5:].split(": ")[0])
        valid = True
        max_count = {}
        for bunch in row.split(": ")[1].split("; "):
            bag = {
                "red": 12,
                "green": 13,
                "blue": 14,
            }
            cubes = bunch.split(", ")
            for cube in cubes:
                num, color = cube.split(" ")
                num = int(num)
                bag[color] = bag.get(color, 0) - num
                max_count[color] = max(max_count.get(color, 0), num)
            for value in bag.values():
                if value < 0:
                    valid = False
        if mode == 1:
            if valid:
                ret += game_id
        else:
            temp = 1
            for x in max_count.values():
                temp *= x
            ret += temp

    return ret

def test(log):
    values = log.decode_values("""
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
    """)

    log.test(calc(log, values, 1), '8')
    log.test(calc(log, values, 2), '2286')

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in [[], ["Puzzles"], ["..", "Puzzles"]]:
                cur = os.path.join(*(dn + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
