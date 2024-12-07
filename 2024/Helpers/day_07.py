#!/usr/bin/env python3

DAY_NUM = 7
DAY_DESC = 'Day 7: Bridge Repair'

def calc(log, values, mode):
    ret = 0
    for row in values:
        res, args = row.split(": ")
        args = list(map(int, args.split()))
        res = int(res)

        pos = ["+" for _ in range(len(args)-1)]
        while True:
            val = args[0]
            for func, x in zip(pos, args[1:]):
                if func == "+":
                    val += x
                elif func == "*":
                    val *= x
                elif func == "||":
                    val = int(str(val) + str(x))
            # print("test", res, "".join(args))
            # print(val)
            if val == res:
                # ret += eval("".join(args))
                ret += res
                # print(res, "".join(args))
                break
            i = 0
            ended = False
            possible = ["+", "*"] + ([] if mode == 1 else ["||"])
            while True:
                if i >= len(pos):
                    ended = True
                    break

                if pos[i] == possible[-1]:
                    pos[i] = possible[0]
                    i += 1
                else:
                    pos[i] = possible[possible.index(pos[i]) + 1]
                    break
            if ended:
                break

    return ret

def test(log):
    values = log.decode_values("""
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
    """)

    log.test(calc(log, values, 1), '3749')
    log.test(calc(log, values, 2), '11387')

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2024/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
