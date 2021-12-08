#!/usr/bin/env python3

def get_desc():
    return 8, 'Day 8: Seven Segment Search'

def calc(log, values, mode):
    if mode == 1:
        hits = 0
        for cur in values:
            unique, output = [x.strip().split() for x in cur.split("|")]
            for test in output:
                if len(test) in {2, 3, 4, 7}:
                    hits += 1
                # test = "".join(sorted(x for x in test))
                # print(test)
                # hits[digits.get(test, -1)] += 1
        
        return hits
    else:
        ret = 0
        for cur in values:
            unique, output = [x.strip().split() for x in cur.split("|")]
            unique = [set(x) for x in unique]
            # print(unique)
            zunique, output = [[set(x) for x in part.split()] for part in cur.split(' | ')]
            # print(unique)

            digits = {}
            digits[1] = [x for x in unique if len(x) == 2][0]
            unique.remove(digits[1])
            digits[7] = [x for x in unique if len(x) == 3][0]
            unique.remove(digits[7])
            digits[4] = [x for x in unique if len(x) == 4][0]
            unique.remove(digits[4])
            digits[8] = [x for x in unique if len(x) == 7][0]
            unique.remove(digits[8])
            digits[9] = [x for x in unique if len(x ^ (digits[7] | digits[4])) == 1][0]
            unique.remove(digits[9])
            digits[0] = [x for x in unique if digits[1] < x and len(x) == 6][0]
            unique.remove(digits[0])
            digits[6] = [x for x in unique if len(x) == 6][0]
            unique.remove(digits[6])
            digits[3] = [x for x in unique if digits[1] < x and len(x) == 5][0]
            unique.remove(digits[3])
            digits[5] = [x for x in unique if len(digits[9] - x) == 1][0]
            unique.remove(digits[5])
            digits[2] = unique[0]

            digits = {"".join(sorted(y)): str(x) for x, y in digits.items()}
            ret += int("".join(digits["".join(sorted(x))] for x in output))

        return ret

def test(log):
    values = log.decode_values("""
        be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
        edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
        fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
        fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
        aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
        fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
        dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
        bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
        egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
        gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
    """)

    log.test(calc(log, values, 1), 26)
    log.test(calc(log, values, 2), 61229)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))
