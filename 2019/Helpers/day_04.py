#!/usr/bin/env python3

DAY_NUM = 4
DAY_DESC = 'Day 4: Secure Container'

def enum_increasing(start):
    temp = [int(x) for x in start]
    last = 0
    for i in range(len(temp)):
        if temp[i] < last:
            temp = temp[:i] + [last] * (len(temp) - i)
            break
        last = temp[i]
    temp[-1] -= 1

    while True:
        if temp[-1] == 9:
            if min(temp) == 9:
                break
            i = max([x for x in range(len(temp)) if temp[x] != 9])
            temp = temp[:i] + [temp[i] + 1] * (len(temp) - i)
        else:
            temp[-1] += 1

        yield "".join([str(x) for x in temp])

def calc(log, values):
    values = values[0].split("-")
    hits, hits_double = 0, 0

    for digits in enum_increasing(values[0]):
        if digits > values[1]:
            break

        last, counts = "", []
        for x in digits:
            if x == last:
                counts[-1] += 1
            else:
                last = x
                counts.append(1)

        if max(counts) > 1:
            hits += 1
            if 2 in counts:
                hits_double += 1

    log("Part 1: " + str(hits))
    log("Part 2: " + str(hits_double))

    return hits, hits_double

def test(log):
    values = log.decode_values("""
        236491-713787
    """)

    ret, expected = calc(log, values), (1169, 757)
    log("Test returned %s, expected %s" % (str(ret), str(expected)))
    if ret != expected:
        return False

    return True

def run(log, values):
    calc(log, values)

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
