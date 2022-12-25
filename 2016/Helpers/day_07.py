#!/usr/bin/env python3

DAY_NUM = 7
DAY_DESC = 'Day 7: Internet Protocol Version 7'


def calc(log, values):
    ret = 0
    ssl_count = 0

    for cur in values:
        cur = "    " + cur + "    "
        in_square = 0
        good = False
        made_bad = False

        ssl_in = set()
        ssl_out = set()

        for i in range(len(cur) - 3):
            if cur[i] == "[":
                in_square += 1
            
            if (cur[i] == cur[i+3]) and (cur[i+1] == cur[i+2]) and (cur[i] != cur[i+1]):
                if in_square > 0:
                    good = False
                    made_bad = True
                else:
                    if not made_bad:
                        good = True

            if (cur[i] == cur[i+2]) and (cur[i] != cur[i+1]) and (cur[i+1] not in {']', '['}):
                if in_square > 0:
                    ssl_in.add((cur[i], cur[i+1]))
                else:
                    ssl_out.add((cur[i+1], cur[i]))

            if cur[i] == "]":
                in_square -= 1

        for ssl in ssl_in:
            if ssl in ssl_out:
                ssl_count += 1
                break

        if good:
            ret += 1

    log("SSL: " + str(ssl_count))
    return ret


def test(log):
    values = [
        "abba[mnop]qrst",
        "abcd[bddb]xyyx",
    ]

    if calc(log, values) == 1:
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
