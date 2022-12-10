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
    log.show(calc(473, 70904))
    log.show(calc(473, 7090400))
