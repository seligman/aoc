#!/usr/bin/env python3

DAY_NUM = 20
DAY_DESC = 'Day 20: Firewall Rules'


def calc(values, max_ip):
    values = [[int(y) for y in x.split("-")] for x in values]
    values.sort(key=lambda x: x[0])

    ip = 0
    allowed = 0
    return_ip = None

    while True:
        if ip > max_ip:
            return return_ip, allowed
        blocked = False
        for x, y in values:
            if ip >= x and ip <= y:
                blocked = True
                ip = y + 1
                break
        if not blocked:
            if return_ip is None:
                return_ip = ip
            best = None
            for x, y in values:
                if x > ip:
                    if best is None or best > x:
                        best = x
            if best is None:
                best = max_ip
            else:
                best -= 1
            
            allowed += (best - ip) + 1
            
            if ip == max_ip:
                return return_ip, allowed
            else:
                ip = best + 1


def test(log):
    values = [
        "5-8",
        "0-2",
        "4-7",
    ]

    if calc(values, 9) == (3, 2):
        return True
    else:
        return False


def run(log, values):
    vals = calc(values, 4294967295)
    log.show("The lowest IP: %d" % (vals[0],))
    log.show("The number of allowed: %d" % (vals[1],))
