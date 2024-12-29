#!/usr/bin/env python3

from collections import deque

DAY_NUM = 22
DAY_DESC = 'Day 22: Crab Combat'

def deck_to_val(deck_a, deck_b):
    a, b = 0, 0
    for x in reversed(deck_a):
        a = (a * 100) + x
    for x in reversed(deck_b):
        b = (b * 100) + x
    return (a, b)

def remove_card(val):
    a, b = val
    return (a // 100, b // 100)

def add_to_deck(val, deck_id, deck, card):
    a, b = val
    if deck_id == 0:
        a += (10 ** (len(deck) * 2)) * card
    else:
        b += (10 ** (len(deck) * 2)) * card
    deck.append(card)
    return (a, b)

def limit(deck, val):
    deck = deck.copy()
    while len(deck) > val:
        deck.pop()
    return deck

def play_game(wins, deck_a, deck_b, mode, level=1):
    seen = set()
    as_val = deck_to_val(deck_a, deck_b)
    while len(deck_a) > 0 and len(deck_b) > 0:
        if as_val in seen:
            return True
        seen.add(as_val)
        a, b, as_val = deck_a.popleft(), deck_b.popleft(), remove_card(as_val)
        a_won = True

        if a <= len(deck_a) and b <= len(deck_b) and mode == 2:
            a_won = wins.get(as_val, None)
            if a_won is None:
                a_won = play_game(wins, limit(deck_a, a), limit(deck_b, b), mode, level=level+1)
                wins[as_val] = a_won
        else:
            a_won = a > b
        
        if a_won:
            as_val = add_to_deck(as_val, 0, deck_a, a)
            as_val = add_to_deck(as_val, 0, deck_a, b)
        else:
            as_val = add_to_deck(as_val, 1, deck_b, b)
            as_val = add_to_deck(as_val, 1, deck_b, a)

    return len(deck_a) > 0

def calc(log, values, mode):
    cards = []
    for cur in values:
        if cur.startswith("Player"):
            cards.append(deque())
        elif len(cur) > 0:
            cards[-1].append(int(cur))

    play_game({}, cards[0], cards[1], mode)
    cards = cards[0] if len(cards[0]) > 0 else cards[1]
    ret, i = 0, 1
    while len(cards) > 0:
        ret += cards.pop() * i
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
    log(f"Part 1: {calc(log, values, 1)}")
    log(f"Part 2: {calc(log, values, 2)}")

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2020/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
