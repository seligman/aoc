#!/usr/bin/env python3

import re
import itertools

DAY_NUM = 13
DAY_DESC = 'Day 13: Knights of the Dinner Table'


def calc(values, extra=[]):
    r = re.compile("(.*) would (gain|lose) (.*) happiness units by sitting next to (.*)\\.")

    people = set()
    changes = {}

    for cur in values:
        m = r.search(cur)
        a, change, value, b = m.groups()
        value = int(value)
        if change == "lose":
            value = -value
        people.add(a)
        changes[(a, b)] = value

    for cur in extra:
        people.add(cur)

    best_value = None

    for layout in itertools.permutations(people):
        value = 0
        for i in range(len(layout)):
            a = layout[(i - 1 + len(layout)) % (len(layout))]
            b = layout[i]
            c = layout[(i + 1) % (len(layout))]
            value += changes.get((b, a), 0)
            value += changes.get((b, c), 0)

        if best_value is None or value > best_value:
            best_value = value

    return best_value


def test(log):
    values = [
        "Alice would gain 54 happiness units by sitting next to Bob.",
        "Alice would lose 79 happiness units by sitting next to Carol.",
        "Alice would lose 2 happiness units by sitting next to David.",
        "Bob would gain 83 happiness units by sitting next to Alice.",
        "Bob would lose 7 happiness units by sitting next to Carol.",
        "Bob would lose 63 happiness units by sitting next to David.",
        "Carol would lose 62 happiness units by sitting next to Alice.",
        "Carol would gain 60 happiness units by sitting next to Bob.",
        "Carol would gain 55 happiness units by sitting next to David.",
        "David would gain 46 happiness units by sitting next to Alice.",
        "David would lose 7 happiness units by sitting next to Bob.",
        "David would gain 41 happiness units by sitting next to Carol.",
    ]

    if calc(values) == 330:
        return True
    else:
        return False


def run(log, values):
    log(calc(values))
    log(calc(values, ["<ME>"]))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in [[], ["Puzzles"], ["..", "Puzzles"]]:
                cur = os.path.join(*(dn + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
