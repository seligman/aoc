#!/usr/bin/env python3

DAY_NUM = 22
DAY_DESC = 'Day 22: Slam Shuffle'


def calc(log, values):
    import re

    def get_steps(reverse=False):
        res = [
            ("deal", re.compile("deal into new stack()"), False),
            ("cut", re.compile("cut ([0-9-]+)"), True),
            ("inc", re.compile("deal with increment ([0-9-]+)"), True),
        ]

        for cur in values[::-1] if reverse else values:
            for name, cur_re, has_value in res:
                m = cur_re.search(cur)
                if m is not None:
                    yield name, int(m.group(1)) if has_value else None

    deck = 10007
    card = 2019

    for oper, value in get_steps():
        if oper == "deal":
            card = deck - 1 - card
        elif oper == "cut":
            card = (deck - value + card) % deck
        elif oper == "inc":
            card = card * value % deck

    log("Card 2019 is at offset: " + str(card))

    deck = 119315717514047
    card = 2020
    times = 101741582076661

    a = 1
    b = 0
    for oper, value in get_steps(reverse=True):
        if oper == "deal":
            b += 1
            a *= -1
            b *= -1
        elif oper == "cut":
            b += value
        elif oper == "inc":
            p = pow(value, deck-2, deck)
            a *= p
            b *= p

        a %= deck
        b %= deck

    temp_a = pow(a, times, deck) * card
    temp_b = pow(a, times, deck) + deck - 1
    temp_c = pow(a-1, deck - 2, deck)
    value = temp_a + b * temp_b * temp_c
    value %= deck

    log("Card at position 2020: " + str(value))


def test(log):
    return True


def run(log, values):
    calc(log, values)

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in [[], ["Puzzles"], ["..", "Puzzles"]]:
                cur = os.path.join(*(dn + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!"); exit(1)
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
