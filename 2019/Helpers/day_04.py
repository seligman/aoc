#!/usr/bin/env python

def get_desc():
    return 4, 'Day 4: Secure Container'


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

    log("Valid entries: " + str(hits))
    log("Valid entries with a double: " + str(hits_double))

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
