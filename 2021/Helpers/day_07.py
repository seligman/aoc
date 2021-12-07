#!/usr/bin/env python3

def get_desc():
    return 7, 'Day 7: The Treachery of Whales'

def calc(log, values, mode):
    values = [int(x) for x in values[0].split(",")]
    best = None
    cost = {}

    for target in range(min(values), max(values)+1):
        temp = 0
        for cur in values:
            if mode == 1:
                temp += abs(cur - target)
            else:
                x = abs(cur - target)
                if x not in cost:
                    cost[x] = sum(range(x + 1))
                temp += cost[x]
            if best is not None and temp > best:
                break
        if best is None:
            best = temp
        else:
            best = min(best, temp)
    
    return best

def test(log):
    values = log.decode_values("""
        16,1,2,0,4,2,7,1,2,14
    """)

    log.test(calc(log, values, 1), 37)
    log.test(calc(log, values, 2), 168)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))
