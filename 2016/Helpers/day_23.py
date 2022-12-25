#!/usr/bin/env python3

DAY_NUM = 23
DAY_DESC = 'Day 23: Safe Cracking'


def get_value(r, value):
    deref = {"a": 0, "b": 1, "c": 2, "d": 3}
    if value in deref:
        return r[deref[value]]
    else:
        return int(value)


def calc(log, values, init_a, munge_code, show_hot_spots):
    deref = {"a": 0, "b": 1, "c": 2, "d": 3}
    values = [x.split(' ') for x in values]
    hot_spots = [0] * len(values)

    ip = 0
    r = [init_a, 0, 0, 0]
    while ip < len(values):
        hot_spots[ip] += 1

        if munge_code and ip == 3:
            r[0] = r[1] * r[3]
            r[2] = 0
            r[3] = 0
            new_ip = 10
        elif munge_code and ip == 21:
            r[0] += r[3]
            r[3] = 0
            new_ip = 24
        else:
            cur = values[ip]
            new_ip = ip + 1

            if cur[0] == "cpy":
                if cur[2] in deref:
                    r[deref[cur[2]]] = get_value(r, cur[1])
            elif cur[0] == "inc":
                if cur[1] in deref:
                    r[deref[cur[1]]] += 1
            elif cur[0] == "dec":
                if cur[1] in deref:
                    r[deref[cur[1]]] -= 1
            elif cur[0] == "jnz":
                if get_value(r, cur[1]) != 0:
                    new_ip = ip + get_value(r, cur[2])
            elif cur[0] == "tgl":
                temp = ip + get_value(r, cur[1])
                if temp < len(values):
                    new_row = values[temp]
                    if new_row[0] in {'dec', 'tgl'}:
                        new_row[0] = 'inc'
                    elif new_row[0] in {'inc'}:
                        new_row[0] = 'dec'
                    elif new_row[0] in {'jnz'}:
                        new_row[0] = 'cpy'
                    elif new_row[0] in {'cpy'}:
                        new_row[0] = 'jnz'
                    else:
                        raise Exception(new_row)
            else:
                raise Exception(cur)
        ip = new_ip

    if show_hot_spots:
        for i in range(len(values)):
            log("%3d:  %5d %s" % (i, hot_spots[i], " ".join(values[i])))

    return r[0]


def test(log):
    values = [
        "cpy 2 a",
        "tgl a",
        "tgl a",
        "tgl a",
        "cpy 1 a",
        "dec a",
        "dec a",
    ]

    if calc(log, values, 7, False, True) == 3:
        return True
    else:
        return False


class DummyLog:
    def __init__(self):
        pass

    def show(self, value):
        print(value)


def other_hotspots(describe, values):
    if describe:
        return "Show hotspots in code"

    calc(DummyLog(), values, 7, False, True)


def run(log, values):
    log(calc(log, values, 7, True, False))
    log(calc(log, values, 12, True, False))

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
