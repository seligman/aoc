#!/usr/bin/env python3

from collections import defaultdict, deque

DAY_NUM = 18
DAY_DESC = 'Day 18: Duet'


def deref(r, value):
    if len(value) == 1 and value >= 'a' and value <= 'z':
        return r[value]
    else:
        return int(value)


class Machine:
    def __init__(self, values, p):
        self.ip = 0
        self.r = defaultdict(int)
        self.r["p"] = p
        self.values = [x.split(' ') for x in values]
        self.sent = 0
        self.state = "starting"
        self.queue = deque()
        self.other_queue = None
        self.ran = 0

    def step(self):
        if self.state == "eop":
            return

        while self.ip < len(self.values):
            self.ran += 1
            cur = self.values[self.ip]

            new_ip = self.ip + 1
            if cur[0] == "snd":
                self.other_queue.append(deref(self.r, cur[1]))
                self.sent += 1
            elif cur[0] == "set":
                self.r[cur[1]] = deref(self.r, cur[2])
            elif cur[0] == "add":
                self.r[cur[1]] += deref(self.r, cur[2])
            elif cur[0] == "mul":
                self.r[cur[1]] *= deref(self.r, cur[2])
            elif cur[0] == "mod":
                self.r[cur[1]] %= deref(self.r, cur[2])
            elif cur[0] == "rcv":
                if len(self.queue) == 0:
                    self.state = "queue"
                    return
                else:
                    self.r[cur[1]] = self.queue.popleft()
            elif cur[0] == "jgz":
                if deref(self.r, cur[1]) > 0:
                    new_ip = self.ip + deref(self.r, cur[2])
            else:
                raise Exception()
            self.ip = new_ip

        self.queue.clear()
        self.state = "eop"


def calc2(log, values):
    m0 = Machine(values, 0)
    m1 = Machine(values, 1)
    m0.other_queue = m1.queue
    m1.other_queue = m0.queue

    while True:
        m0.step()
        m1.step()
        if len(m0.queue) == 0 and len(m1.queue) == 0:
            break

    return m1.sent


def calc(log, values):
    sound = None
    r = defaultdict(int)
    ip = 0

    values = [x.split(' ') for x in values]
    while ip < len(values):
        cur = values[ip]
        new_ip = ip + 1
        if cur[0] == "snd":
            sound = deref(r, cur[1])
        elif cur[0] == "set":
            r[cur[1]] = deref(r, cur[2])
        elif cur[0] == "add":
            r[cur[1]] += deref(r, cur[2])
        elif cur[0] == "mul":
            r[cur[1]] *= deref(r, cur[2])
        elif cur[0] == "mod":
            r[cur[1]] %= deref(r, cur[2])
        elif cur[0] == "rcv":
            if deref(r, cur[1]) != 0:
                return sound
        elif cur[0] == "jgz":
            if deref(r, cur[1]) > 0:
                new_ip = ip + deref(r, cur[2])
        else:
            raise Exception()
        ip = new_ip

    return None


def test(log):
    values = [
        "set a 1",
        "add a 2",
        "mul a a",
        "mod a 5",
        "snd a",
        "set a 0",
        "rcv a",
        "jgz a -1",
        "set a 1",
        "jgz a -2",
    ]

    if calc(log, values) == 4:
        log("Pass 1 worked")

        values = [
            "snd 1",
            "snd 2",
            "snd p",
            "rcv a",
            "rcv b",
            "rcv c",
            "rcv d",
        ]

        if calc2(log, values) == 3:
            log("Pass 2 worked")
            return True
        else:
            return False
    else:
        return False


def run(log, values):
    log(calc(log, values))
    log(calc2(log, values))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2017/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
