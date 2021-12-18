#!/usr/bin/env python3

def get_desc():
    return 18, 'Day 18: Snailfish'

def tokens(value):
    ret = []
    for cur in value:
        if cur in "[]":
            if len(ret) > 0 and ret[-1] is None:
                ret[-1] = cur
            else:
                ret.append(cur)
        elif cur in "0123456789":
            if len(ret) > 0 and ret[-1] is None:
                ret[-1] = int(cur)
            else:
                if not isinstance(ret[-1], int):
                    ret.append(0)
                ret[-1] = ret[-1] * 10 + int(cur)
        elif cur == ",":
            ret.append(None)
    return ret

def are_tokens(ret, i, *args):
    for cur in args:
        if isinstance(cur, str):
            if cur != ret[i]:
                return False
        else:
            if not isinstance(ret[i], cur):
                return False
        i += 1
    return True

def calc(log, values, mode, parse_values=True):
    if parse_values:
        values = [tokens(x) for x in values]

    if mode == 2:
        best = 0
        for i, a in enumerate(values):
            for j, b in enumerate(values):
                if i != j:
                    temp = calc(log, [a, b], 1, parse_values=False)
                    if temp > best:
                        best = temp
        return best

    ret = None

    while len(values) > 0:
        if ret is None:
            ret = values.pop(0)
        else:
            ret = ["["] + ret + values.pop(0) + ["]"]

        while True:
            depth = 0
            found = False
            for i in range(len(ret)):
                if ret[i] == "[":
                    depth += 1
                elif ret[i] == "]":
                    depth -= 1
                elif depth >= 5 and are_tokens(ret, i, int, int):
                    found = True
                    for j in range(i-1, 0, -1):
                        if isinstance(ret[j], int):
                            ret[j] += ret[i]
                            break
                    for j in range(i+2, len(ret)):
                        if isinstance(ret[j], int):
                            ret[j] += ret[i+1]
                            break
                    ret = ret[:i-1] + [0] + ret[i+3:]
                    break

            if not found:
                for i in range(len(ret)):
                    if isinstance(ret[i], int) and ret[i] >= 10:
                        a = ret[i] // 2
                        b = ret[i] - a
                        ret = ret[:i] + ["[", a, b, "]"] + ret[i+1:]
                        found = True
                        break
            if not found:
                break

    while True:
        found = False
        for i in range(len(ret)):
            if are_tokens(ret, i, "[", int, int, "]"):
                ret = ret[:i] + [ret[i + 1] * 3 + ret[i + 2] * 2] + ret[i+4:]
                found = True
                break
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
