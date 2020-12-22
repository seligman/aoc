#!/usr/bin/env python3

from collections import deque

def get_desc():
    return 22, 'Day 22: Crab Combat'

def to_str(cards):
    return ",".join([str(x) for x in cards[0]]) + "|" + ",".join([str(x) for x in cards[1]])

def limit(deck, val):
    deck = deck.copy()
    while len(deck) > val:
        deck.pop()
    return deck

def play_game(wins, cards, mode, level=1):
    seen = set()
    deck_a, deck_b = cards
    deck = to_str(cards)
    while len(deck_a) > 0 and len(deck_b) > 0:
        if deck in seen:
            return True
        seen.add(deck)
        a, b = deck_a.popleft(), deck_b.popleft()
        deck = to_str(cards)
        a_won = True

        if a <= len(deck_a) and b <= len(deck_b) and mode == 2:
            if deck not in wins:
                wins[deck] = play_game(wins, [limit(deck_a, a), limit(deck_b, b)], mode, level=level+1)
            a_won = wins[deck]
        else:
            a_won = a > b
        
        if a_won:
            deck_a.append(a)
            deck_a.append(b)
        else:
            deck_b.append(b)
            deck_b.append(a)

    return len(deck_a) > 0

def calc(log, values, mode):
    cards = []
    for cur in values:
        if cur.startswith("Player"):
            cards.append(deque())
        elif len(cur) > 0:
            cards[-1].append(int(cur))

    play_game({}, cards, mode)
    cards = list(cards[0]) + list(cards[1])
    ret, i = 0, 1
    while len(cards) > 0:
        ret += cards.pop(-1) * i
        i += 1

    return ret

def test(log):
    values = log.decode_values("""
        Player 1:
        9
        2
        6
        3
        1

        Player 2:
        5
        8
        4
        7
        10
    """)

    log.test(calc(log, values, 1), 306)
    log.test(calc(log, values, 2), 291)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))
