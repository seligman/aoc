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
    log("The lowest IP: %d" % (vals[0],))
    log("The number of allowed: %d" % (vals[1],))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in [[], ["Puzzles"], ["..", "Puzzles"]]:
                cur = os.path.join(*(dn + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!"); exit(1)
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
