#!/usr/bin/env python3

DAY_NUM = 14
DAY_DESC = 'Day 14: Chocolate Charts'

def calc(log, values, target=None):
    scores = [3, 7]
    elv_0 = 0
    elv_1 = 1

    steps = 0
    if target is not None:
        target = tuple(int(x) for x in target)
    while values == 0 or len(scores) < values + 10:
        # print(scores, elv_0, elv_1)
        temp = scores[elv_0] + scores[elv_1]
        if temp >= 10:
            scores.append(temp // 10)
            if target is not None:
                if tuple(scores[-len(target):]) == target:
                    return str(len(scores) - len(target))
        scores.append(temp % 10)
        if target is not None:
            if tuple(scores[-len(target):]) == target:
                return str(len(scores) - len(target))
        elv_0 = (elv_0 + scores[elv_0] + 1) % len(scores)
        elv_1 = (elv_1 + scores[elv_1] + 1) % len(scores)
        # if steps % 1000 == 0 and target is not None:
        #     if target in scores:
        #         return str(scores.index(target))
        # if steps > 4000000:
        #     print("loo")
        #     for i in range(2, 2000000):
        #         good = True
        #         for j in range(i):
        #             if scores[i] != scores[i+j]:
        #                 good = False
        #                 break
        #         if good:
        #             print(i)
        #     print("no")
    return "".join(str(x) for x in scores[values:values+10])

def test(log):
    tests = [
        ((9,), "5158916779",),
        ((5,), "0124515891",),
        ((18,), "9251071085",),
        ((2018,), "5941429882",),
        ((0, "51589"), "9"),
        ((0, "01245"), "5"),
        ((0, "92510"), "18"),
        ((0, "59414"), "2018"),
    ]
    for args, expected in tests:
        actual = calc(log, *args)
        if actual != expected:
            log("With %s, got %s, expected %s" % (str(args), str(actual), str(expected)))
            raise Exception()
        else:
            log("With %s, got %s as expected" % (str(args), str(actual)))

    log("All good")

def run(log, values):
    log("Part 1: %s" % (calc(log, int(values[0])),))
    log("Part 2: %s" % (calc(log, 0, values[0]),))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2018/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
