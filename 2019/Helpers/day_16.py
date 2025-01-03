#!/usr/bin/env python3

DAY_NUM = 16
DAY_DESC = 'Day 16: Flawed Frequency Transmission'

def get_lcm(vals):
    from fractions import gcd
    lcm = vals[0]
    for i in vals[1:]:
        lcm = lcm * i // gcd(lcm, i)
    return lcm

def calc(log, values, phases):
    fft = list(map(int, values[0]))

    for _ in range(phases):
        step = []
        i = 0
        while i < len(fft):
            i += 1
            mult_off, value = 0, 0
            off = i - 1
            while off < len(fft):
                mult_off = (mult_off + 1) % 4
                if mult_off == 1:
                    value += sum(fft[off:off+i])
                elif mult_off == 3:
                    value -= sum(fft[off:off+i])
                off += i
            step.append(abs(value) % 10)
        fft = step

    ret = "".join(map(str, fft[:8]))
    log("Part 1: " + ret)

    fft = list(map(int, values[0]))
    offset = int("".join(map(str, fft[:7])))
    fft = (fft * 10000)[offset:][::-1]
    for _ in range(100):
        step = []
        last = 0
        for val in fft:
            last = (last + val) % 10
            step.append(last)
        fft = step

    log("Part 2: " + "".join(map(str, fft[:-9:-1])))

    return ret

def test(log):
    values = log.decode_values("""
        80871224585914546619083218645595
    """)

    ret, expected = calc(log, values, 100), "24176176"
    log("Test returned %s, expected %s" % (str(ret), str(expected)))
    if ret != expected:
        return False

    return True

def run(log, values):
    calc(log, values, 100)

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2019/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
