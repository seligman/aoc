#!/usr/bin/env python3

from collections import defaultdict, deque

DAY_NUM = 9
DAY_DESC = 'Day 9: Marble Mania'

def calc(players, marbles):
    board = deque([0])
    player_scores = defaultdict(int)
    cur_player = 0

    for i in range(1, marbles + 1):
        if i % 23 == 0:
            board.rotate(7)
            removed = board.pop()
            board.rotate(-1)

            player_scores[cur_player] += removed
            player_scores[cur_player] += i
        else:
            board.rotate(-1)
            board.append(i)
        cur_player = (cur_player + 1) % players

    return max(player_scores.values())

def test(log):
    if calc(9, 25) == 32:
        return True
    else:
        return False

def run(log, values):
    import re
    m = re.search("(?P<a>[0-9]+) players; last marble is worth (?P<b>[0-9]+) points", values[0])
    log(calc(int(m['a']), int(m['b'])))
    log(calc(int(m['a']), int(m['b']) * 100))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2018/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
