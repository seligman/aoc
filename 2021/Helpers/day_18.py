#!/usr/bin/env python3

DAY_NUM = 18
DAY_DESC = 'Day 18: Snailfish'

OPEN = -1
CLOSE = -2

def tokens(value):
    ret = []
    for cur in value:
        if cur == "[":
            ret.append(OPEN)
        elif cur == "]":
            ret.append(CLOSE)
        elif cur in "0123456789":
            ret.append(int(cur))
    return ret

def show_tokens(log, tokens):
    temp = []
    for cur in tokens:
        if cur == OPEN:
            cur = "["
        elif cur == CLOSE:
            cur = "]"
        if len(temp) == 0:
            temp.append(cur)
        else:
            if isinstance(cur, int):
                if temp[-1] != "[":
                    temp.append(",")
                temp.append(cur)
            else:
                if (temp[-1] == "[" and cur != "[") or (temp[-1] != "[" and cur == "["):
                    temp.append(",")
                temp.append(cur)
    temp = [str(x) for x in temp]
    temp = "".join(temp)
    log(temp)

def calc(log, values, mode, parse_values=True):
    if parse_values:
        values = [tokens(x) for x in values]

    if mode == 2:
        best = 0
        for i, a in enumerate(values):
            for j, b in enumerate(values):
                if i != j:
                    best = max(best, calc(log, [a, b], 1, parse_values=False))
        return best

    ret = values.pop(0)
    while len(values) > 0:
        ret = [OPEN] + ret + values.pop(0) + [CLOSE]
        while True:
            depth = 0
            found = False
            for i in range(len(ret)):
                if ret[i] == OPEN:
                    depth += 1
                elif ret[i] == CLOSE:
                    depth -= 1
                elif depth >= 5 and ret[i] >= 0 and ret[i+1] >= 0:
                    found = True
                    for j in range(i-2, 0, -1):
                        if ret[j] >= 0:
                            ret[j] += ret[i]
                            break
                    for j in range(i+3, len(ret)):
                        if ret[j] >= 0:
                            ret[j] += ret[i+1]
                            break
                    ret = ret[:i-1] + [0] + ret[i+3:]
                    break

            if not found:
                for i in range(len(ret)):
                    if ret[i] >= 10:
                        a = ret[i] // 2
                        b = ret[i] - a
                        ret = ret[:i] + [OPEN, a, b, CLOSE] + ret[i+1:]
                        found = True
                        break

            if not found:
                break

    while True:
        found = False
        i = 0
        while i < len(ret):
            if ret[i] == OPEN and ret[i+1] >= 0 and ret[i+2] >= 0 and ret[i+3] == CLOSE:
                ret = ret[:i] + [ret[i + 1] * 3 + ret[i + 2] * 2] + ret[i+4:]
                found = True
            i += 1
        if not found:
            break

    return ret[0]

def test(log):
    values = log.decode_values("""
        [[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
        [[[5,[2,8]],4],[5,[[9,9],0]]]
        [6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
        [[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
        [[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
        [[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
        [[[[5,4],[7,7]],8],[[8,3],8]]
        [[9,3],[[9,9],[6,[4,9]]]]
        [[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
        [[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
    """)

    log.test(calc(log, values, 1), 4140)
    log.test(calc(log, values, 2), 3993)

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
