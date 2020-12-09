#!/usr/bin/env python3

def get_desc():
    return 24, 'Day 24: Electromagnetic Moat'


def longest(values, cur_path, mode):
    ret = []
    for i in range(len(values)):
        if cur_path[-1] == values[i][0]:
            temp = cur_path[:]
            temp.append(values[i][0])
            temp.append(values[i][1])
            next_values = values[:]
            next_values.pop(i)
            ret.append(longest(next_values, temp, mode))
        elif cur_path[-1] == values[i][1]:
            temp = cur_path[:]
            temp.append(values[i][1])
            temp.append(values[i][0])
            next_values = values[:]
            next_values.pop(i)
            ret.append(longest(next_values, temp, mode))
    
    if len(ret) == 0:
        return cur_path
    else:
        if mode == 0:
            ret.sort(key=lambda x:sum(x), reverse=True)
        else:
            ret.sort(key=lambda x:(len(x), sum(x)), reverse=True)
        return ret[0]


def calc(log, values, mode):
    values = [[int(x) for x in y.split("/")] for y in values]
    path = longest(values, [0], mode)
    return sum(path)


def test(log):
    values = [
        "0/2",
        "2/2",
        "2/3",
        "3/4",
        "3/5",
        "0/1",
        "10/1",
        "9/10",
    ]

    if calc(log, values, 0) == 31:
        log.show("Pass 1 worked")
        if calc(log, values, 1) == 19:
            log.show("Pass 2 worked")
            return True
        else:
            return False
    else:
        return False


def run(log, values):
    log.show(calc(log, values, 0))
    log.show(calc(log, values, 1))
