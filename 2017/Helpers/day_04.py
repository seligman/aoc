#!/usr/bin/env python

def get_desc():
    return 4, 'Day 4: High-Entropy Passphrases'


def calc(log, values):
    ret = 0
    ret2 = 0
    for cur in values:
        cur = cur.split(' ')
        if len(set(cur)) == len(cur):
            ret += 1
        cur = ["".join(sorted(x)) for x in cur]
        if len(set(cur)) == len(cur):
            ret2 += 1

    log.show("Anagrams: " + str(ret2))

    return ret


def test(log):
    return True


def run(log, values):
    log.show(calc(log, values))
