#!/usr/bin/env python3

DAY_NUM = 12
DAY_DESC = 'Day 12: Leonardo\'s Monorail'


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
    log(calc(values, 0))
    log(calc(values, 1))

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
