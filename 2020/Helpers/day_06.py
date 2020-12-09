#!/usr/bin/env python3

from collections import defaultdict

def get_desc():
    return 6, 'Day 6: Custom Customs'

def calc(log, values, mode):
    total_answers = 0
    this_group = defaultdict(int)
    for value in values + [""]:
        if len(value) == 0:
            if len(this_group) > 0:
                if mode == 1:
                    total_answers += len(this_group) - 1
                else:
                    total_answers += len([x for x in this_group if this_group[x] == this_group['people']]) - 1
                this_group = defaultdict(int)
        else:
            for answer in value:
                this_group[answer] += 1
            this_group['people'] += 1

    return total_answers

def test(log):
    values = log.decode_values("""
        abc

        a
        b
        c

        ab
        ac

        a
        a
        a
        a

        b
    """)

    log.test(calc(log, values, 1), 11)
    log.test(calc(log, values, 2), 6)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))
