#!/usr/bin/env python3

DAY_NUM = 7
DAY_DESC = 'Day 7: Camel Cards'

from collections import Counter

def calc(log, values, mode):
    (
        five_of_a_kind,
        four_of_a_kind,
        full_house,
        three_of_a_kind,
        two_pair,
        one_pair,
        high_card,
    ) = range(7)

    hands = []

    if mode == 2:
        card_values = {x: i for i, x in enumerate("AKQT98765432J")}
    else:
        card_values = {x: i for i, x in enumerate("AKQJT98765432")}

    for row in values:
        hand, bid = row.split(" ")
        hand_ranking = [card_values[x] for x in hand]
        bid = int(bid)

        temp = Counter(hand)
        joker = 0
        if mode == 2:
            joker = temp["J"]
            del temp["J"]
        temp2 = Counter(temp.values())

        if len(temp) == 1 or len(temp) == 0:
            hand_type = five_of_a_kind
        elif max(temp.values()) + joker == 4:
            hand_type = four_of_a_kind
        elif (len(temp) == 2 and 2 in temp.values() and 3 in temp.values()) or (temp2[2] == 2 and joker == 1):
            hand_type = full_house
        elif (3 - joker) in temp.values():
            hand_type = three_of_a_kind
        elif (2 in temp2 and temp2[2] == 2) or (joker > 0 and 2 in temp2):
            hand_type = two_pair
        elif (2 - joker) in temp.values():
            hand_type = one_pair
        else:
            hand_type = high_card

        hands.append((hand_type, tuple(hand_ranking), hand, bid))

    hands.sort(reverse=True)
    ret = 0
    for i, (hand_type, hand_ranking, hand, bid) in enumerate(hands):
        ret += bid * (i + 1)

    return ret

def test(log):
    values = log.decode_values("""
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
    """)

    log.test(calc(log, values, 1), '6440')
    log.test(calc(log, values, 2), '5905')

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2023/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
