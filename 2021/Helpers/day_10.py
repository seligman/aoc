#!/usr/bin/env python3

def get_desc():
    return 10, 'Day 10: Syntax Scoring'

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