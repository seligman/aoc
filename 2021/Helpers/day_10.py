#!/usr/bin/env python3

DAY_NUM = 10
DAY_DESC = 'Day 10: Syntax Scoring'

def calc(log, values, mode):
    brackets = "()[]{}<>"
    opens = {brackets[x]:brackets[x+1] for x in range(0, len(brackets), 2)}
    closes = {y:x for x,y in opens.items()}

    score_bad = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137,
    }
    score_good = {
        ')': 1,
        ']': 2,
        '}': 3,
        '>': 4,
    }

    ret = 0
    good_scores = []
    for cur in values:
        stack = []
        good = ""
        is_bad = False
        for x in cur:
            if x in "[<{(":
                stack.append(x)
                good += x
            else:
                if closes[x] == stack[-1]:
                    stack.pop(-1)
                    good += x
                else:
                    if mode == 1:
                        ret += score_bad[x]
                    is_bad = True
                    break
        if not is_bad and mode == 2:
            cur = 0
            for x in stack[::-1]:
                cur = cur * 5 + score_good[opens[x]]
            good_scores.append(cur)

    if mode == 2:
        good_scores.sort()
        return good_scores[(len(good_scores) - 1) // 2]

    return ret

def test(log):
    values = log.decode_values("""
        [({(<(())[]>[[{[]{<()<>>
        [(()[<>])]({[<{<<[]>>(
        {([(<{}[<>[]}>{[]{[(<()>
        (((({<>}<{<{<>}{[]{[]{}
        [[<[([]))<([[{}[[()]]]
        [{[{({}]{}}([{[{{{}}([]
        {<[[]]>}<{[{[{[]{()[[[]
        [<(<(<(<{}))><([]([]()
        <{([([[(<>()){}]>(<<{{
        <{([{{}}[<[[[<>{}]]]>[]]
    """)

    log.test(calc(log, values, 1), 26397)
    log.test(calc(log, values, 2), 288957)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2021/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
