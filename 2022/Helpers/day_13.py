#!/usr/bin/env python3

DAY_NUM = 13
DAY_DESC = 'Day 13: Distress Signal'

def calc(log, values, mode):
    if mode == 2:
        values.append("[[2]]")
        values.append("[[6]]")

    def compare(a, b):
        a = a[:]
        b = b[:]
        while len(a) < len(b):
            a.append(None)
        while len(b) < len(a):
            b.append(None)
        for aa, bb in zip(a, b):
            if aa is None:
                return 1
            elif bb is None:
                return -1
            elif isinstance(aa, int) and isinstance(bb, int):
                if aa > bb:
                    return -1
                elif aa < bb:
                    return 1
            else:
                if isinstance(aa, int):
                    aa = [aa]
                if isinstance(bb, int):
                    bb = [bb]
                
                test = compare(aa, bb)
                if test != 0:
                    return test
        return 0

    if mode == 2:
        from functools import cmp_to_key
        values = [x for x in values if len(x)]
        values = [eval(x) for x in values]
        values.sort(key=cmp_to_key(compare), reverse=True)
        ret = 1
        for i, x in enumerate(values):
            if str(x) in {"[[2]]", "[[6]]"}:
                ret *= i + 1
        return ret

    stack = [[]]
    for cur in values:
        if len(cur) > 0:
            if len(stack[-1]) == 2:
                stack.append([])
            stack[-1].append(eval(cur))

    ret = 0
    for i, (a, b) in enumerate(stack):
        test = compare(a, b)
        if test == 1:
            ret += i+1

    return ret

def test(log):
    values = log.decode_values("""
        [1,1,3,1,1]
        [1,1,5,1,1]

        [[1],[2,3,4]]
        [[1],4]

        [9]
        [[8,7,6]]

        [[4,4],4,4]
        [[4,4],4,4,4]

        [7,7,7,7]
        [7,7,7]

        []
        [3]

        [[[]]]
        [[]]

        [1,[2,[3,[4,[5,6,7]]]],8,9]
        [1,[2,[3,[4,[5,6,0]]]],8,9]
    """)

    log.test(calc(log, values, 1), 13)
    log.test(calc(log, values, 2), 140)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))

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