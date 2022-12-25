#!/usr/bin/env python3

import re
from collections import defaultdict

DAY_NUM = 4
DAY_DESC = 'Day 4: Repose Record'


def calc(log, values):
    r = re.compile("\\[([0-9]{4})-([0-9]{2})-([0-9]{2}) ([0-9]{2}):([0-9]{2})\\] (Guard #([0-9]+) begins shift|falls asleep|wakes up)")

    guard_id = None
    asleep_at = None

    guards = {}

    for cur in sorted(values):
        m = r.search(cur)
        if m:
            _year, _month, _day, _hour, minute, state, new_id = m.groups()
            if state == "falls asleep":
                asleep_at = int(minute)
            elif state == "wakes up":
                for x in range(asleep_at, int(minute)):
                    guards[guard_id]['asleep_time'] += 1
                    guards[guard_id]['minutes'][x] += 1
                asleep_at = None
            elif state.startswith("Guard #"):
                if asleep_at is not None:
                    raise("Error with asleep at")
                guard_id = int(new_id)
                if guard_id not in guards:
                    guards[guard_id] = {
                        'asleep_time': 0,
                        'minutes': defaultdict(int),
                    }
            else:
                raise Exception("Invalid state: " + state)
        else:
            raise Exception("Invalid line: " + cur)

    sleepy = list(guards)
    sleepy.sort(key=lambda x: guards[x]['asleep_time'], reverse=True)
    best_min = 0
    best_val = 0
    for i in range(60):
        if guards[sleepy[0]]['minutes'][i] > best_val:
            best_val = guards[sleepy[0]]['minutes'][i]
            best_min = i

    best_count = 0
    best_val = None
    for guard_id in guards:
        value = guards[guard_id]
        for minute in value['minutes']:
            count = value['minutes'][minute]
            if count > best_count:
                best_val = (guard_id, minute)
                best_count = count

    log("Guard: %d, Minute %d == %d" % (best_val[0], best_val[1], best_val[0] * best_val[1]))

    return sleepy[0] * best_min


def test(log):
    values = [
        "[1518-11-01 00:00] Guard #10 begins shift",
        "[1518-11-01 00:05] falls asleep",
        "[1518-11-01 00:25] wakes up",
        "[1518-11-01 00:30] falls asleep",
        "[1518-11-01 00:55] wakes up",
        "[1518-11-01 23:58] Guard #99 begins shift",
        "[1518-11-02 00:40] falls asleep",
        "[1518-11-02 00:50] wakes up",
        "[1518-11-03 00:05] Guard #10 begins shift",
        "[1518-11-03 00:24] falls asleep",
        "[1518-11-03 00:29] wakes up",
        "[1518-11-04 00:02] Guard #99 begins shift",
        "[1518-11-04 00:36] falls asleep",
        "[1518-11-04 00:46] wakes up",
        "[1518-11-05 00:03] Guard #99 begins shift",
        "[1518-11-05 00:45] falls asleep",
        "[1518-11-05 00:55] wakes up",
    ]

    if calc(log, values) == 240:
        return True
    else:
        return False


def run(log, values):
    log(calc(log, values))

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
