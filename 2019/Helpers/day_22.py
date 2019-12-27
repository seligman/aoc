#!/usr/bin/env python

def get_desc():
    return 22, 'Day 22: Slam Shuffle'


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

    log.show("Card 2019 is at offset: " + str(card))

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

    log.show("Card at position 2020: " + str(value))


def test(log):
    return True


def run(log, values):
    calc(log, values)
