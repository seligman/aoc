#!/usr/bin/env python3

DAY_NUM = 24
DAY_DESC = 'Day 24: Electromagnetic Moat'


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
        log("Pass 1 worked")
        if calc(log, values, 1) == 19:
            log("Pass 2 worked")
            return True
        else:
            return False
    else:
        return False


def run(log, values):
    log(calc(log, values, 0))
    log(calc(log, values, 1))

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
