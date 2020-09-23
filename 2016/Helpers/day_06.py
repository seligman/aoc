#!/usr/bin/env python

from collections import defaultdict

def get_desc():
    return 6, 'Day 6: Signals and Noise'


def calc(values, first_pass):
    ret = ""
    for i in range(len(values[0])):
        hist = defaultdict(int)
        for cur in values:
            hist[cur[i]] += 1
        letters = list(hist)
        letters.sort(key=lambda x: hist[x], reverse=first_pass)
        ret += letters[0]

    return ret


def test(log):
    values = [
        "eedadn",
        "drvtee",
        "eandsr",
        "raavrd",
        "atevrs",
        "tsrnev",
        "sdttsa",
        "rasrtv",
        "nssdts",
        "ntnada",
        "svetve",
        "tesnvt",
        "vntsnd",
        "vrdear",
        "dvrsen",
        "enarar",
    ]

    if calc(values, True) == "easter":
        return True
    else:
        return False


def run(log, values):
    log.show(calc(values, True))
    log.show(calc(values, False))
