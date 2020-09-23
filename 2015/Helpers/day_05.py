#!/usr/bin/env python

import re

def get_desc():
    return 5, 'Day 5: Doesn\'t He Have Intern-Elves For This?'


def calc(log, values):
    vowels = {"a", "e", "i", "o", "u"}
    bad = ["ab", "cd", "pq", "xy"]
    total_good = 0
    total_good_v2 = 0

    for cur in values:
        good = False
        vowel_count = 0
        for sub in cur:
            if sub in vowels:
                vowel_count += 1
                if vowel_count == 3:
                    good = True
                    break
        
        if good:
            for bad_word in bad:
                if bad_word in cur:
                    good = False
                    break

        if good:
            last = ""
            good = False
            for sub in cur:
                if last == sub:
                    good = True
                    break
                last = sub

        if good:
            total_good += 1

        if re.search("(..).*\\1", cur) and re.search("(.).\\1", cur):
            total_good_v2 += 1

    log.show("Ver 2: " + str(total_good_v2))

    return total_good


def test(log):
    values = [
        "ugknbfddgicrmopn",
        "aaa",
        "jchzalrnumimnmhp",
        "haegwjzuvuyypxyu",
        "dvszwmarrgswjxmb",
    ]

    if calc(log, values) == 2:
        return True
    else:
        return False


def run(log, values):
    log.show(calc(log, values))
