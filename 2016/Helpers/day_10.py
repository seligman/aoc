#!/usr/bin/env python

import re

def get_desc():
    return 10, 'Day 10: Balance Bots'


def calc(log, values):
    bots = {}

    while True:
        for i in range(len(values)):
            if values[i] is not None:
                m = re.search("value ([0-9]+) goes to (bot [0-9]+)", values[i])
                if m:
                    if m.group(2) not in bots:
                        bots[m.group(2)] = []
                    bots[m.group(2)].append(m.group(1))
                    values[i] = None

            if values[i] is not None:
                m = re.search("(bot [0-9]+) gives low to (.*) and high to (.*)", values[i])
                if m:
                    if m.group(1) in bots and len(bots[m.group(1)]) == 2:
                        a, b = m.group(2), m.group(3)
                        if a not in bots:
                            bots[a] = []
                        if b not in bots:
                            bots[b] = []

                        if bots[m.group(1)][0] == "61" and bots[m.group(1)][1] == "17":
                            log.show("Bot with 17 and 61: " + m.group(1))
                        if bots[m.group(1)][0] == "17" and bots[m.group(1)][1] == "61":
                            log.show("Bot with 17 and 61: " + m.group(1))

                        if int(bots[m.group(1)][0]) < int(bots[m.group(1)][1]):
                            bots[a].append(bots[m.group(1)][0])
                            bots[b].append(bots[m.group(1)][1])
                        else:
                            bots[a].append(bots[m.group(1)][1])
                            bots[b].append(bots[m.group(1)][0])

                        a = bots.get("output 0", None)
                        b = bots.get("output 1", None)
                        c = bots.get("output 2", None)

                        if a is not None and b is not None and c is not None:
                            log.show("Final answer: " + str(int(a[0]) * int(b[0]) * int(c[0])))
                            return

                        bots[m.group(1)] = []


def test(log):
    return True


def run(log, values):
    calc(log, values)
