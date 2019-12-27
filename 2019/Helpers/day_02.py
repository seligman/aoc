#!/usr/bin/env python

def get_desc():
    return 2, 'Day 2: 1202 Program Alarm'


def calc(log, values, replace_1=None, replace_2=None):
    ticker = [int(x) for x in values[0].split(",")]
    if replace_1:
        ticker[1] = replace_1
        ticker[2] = replace_2
    off = 0
    while True:
        op = ticker[off]
        if op == 1:
            ticker[ticker[off+3]] = ticker[ticker[off+1]] + ticker[ticker[off+2]]
        elif op == 2:
            ticker[ticker[off+3]] = ticker[ticker[off+1]] * ticker[ticker[off+2]]
        elif op == 99:
            break
        else:
            raise Exception()
        off += 4

    return ticker[0]


def test(log):
    if calc(log, ["1,9,10,3,2,3,11,0,99,30,40,50"]) != 3500:
        return False
    if calc(log, ["1,0,0,0,99"]) != 2:
        return False
    if calc(log, ["2,4,4,5,99,0"]) != 2:
        return False
    if calc(log, ["1,1,1,4,99,5,6,0,99"]) != 30:
        return False

    return True


def run(log, values):
    log.show(calc(log, values, replace_1=12, replace_2=2))
    found = False
    for a in range(100):
        if found:
            break
        for b in range(200):
            try:
                if calc(log, values, replace_1=a, replace_2=b) == 19690720:
                    log.show(100 * a + b)
                    found = True
                    break
            except:
                pass
