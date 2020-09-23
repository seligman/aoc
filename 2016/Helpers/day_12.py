#!/usr/bin/env python

def get_desc():
    return 12, 'Day 12: Leonardo\'s Monorail'


def get_value(r, value):
    deref = {"a": 0, "b": 1, "c": 2, "d": 3}
    if value in deref:
        return r[deref[value]]
    else:
        return int(value)


def calc(values, init_c):
    deref = {"a": 0, "b": 1, "c": 2, "d": 3}

    ip = 0
    r = [0, 0, init_c, 0]
    while ip < len(values):
        cur = values[ip]
        cur = cur.split(' ')
        new_ip = ip + 1
        if cur[0] == "cpy":
            r[deref[cur[2]]] = get_value(r, cur[1])
        elif cur[0] == "inc":
            r[deref[cur[1]]] += 1
        elif cur[0] == "dec":
            r[deref[cur[1]]] -= 1
        elif cur[0] == "jnz":
            if get_value(r, cur[1]) != 0:
                new_ip = ip + get_value(r, cur[2])
        else:
            raise Exception(cur)
        ip = new_ip

    return r[0]


def test(log):
    values = [
        "cpy 41 a",
        "inc a",
        "inc a",
        "dec a",
        "jnz a 2",
        "dec a",
    ]

    if calc(values, 0) == 42:
        return True
    else:
        return False


def run(log, values):
    log.show(calc(values, 0))
    log.show(calc(values, 1))
