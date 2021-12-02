#!/usr/bin/env python3

def get_desc():
    return 2, 'Day 2: Dive!'

def calc(log, values, mode):
    pos = 0
    depth = 0
    aim = 0
    for cur in values:
        dir, amt = cur.split()
        amt = int(amt)
        if mode == 1:
            if dir == "forward":
                pos += amt
            elif dir == "down":
                depth += amt
            elif dir == "up":
                depth -= amt
            else:
                raise Exception()
        else:
            if dir == "forward":
                pos += amt
                depth += aim * amt
            elif dir == "down":
                aim += amt
            elif dir == "up":
                aim -= amt
            else:
                raise Exception()

    return depth * pos

def test(log):
    values = log.decode_values("""
        forward 5
        down 5
        forward 8
        up 3
        down 8
        forward 2
    """)

    log.test(calc(log, values, 1), 150)
    log.test(calc(log, values, 2), 900)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))
