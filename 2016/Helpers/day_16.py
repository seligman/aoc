#!/usr/bin/env python3

DAY_NUM = 16
DAY_DESC = 'Day 16: Dragon Checksum'


def calc(values, target_len):
    value = values[0]

    while len(value) < target_len:
        value = value + "0" + "".join(["1" if x == "0" else "0" for x in reversed(value)])

    value = value[0:target_len]

    code = {
        "00": "1",
        "11": "1",
        "01": "0",
        "10": "0",
    }

    while len(value) % 2 != 1:
        value = "".join([code[value[x:x+2]] for x in range(0, len(value), 2)])

    return value


def test(log):
    values = [
        "10000",
    ]

    if calc(values, 20) == "01100":
        return True
    else:
        return False


def run(log, values):
    log(calc(values, 272))
    log(calc(values, 35651584))

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
