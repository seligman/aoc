#!/usr/bin/env python3

def get_desc():
    return 8, 'Day 8: Seven Segment Search'

def calc(log, values, mode):
    ret = 0
    for cur in values:
        unique, output = [x.strip().split() for x in cur.split("|")]
        unique = [set(x) for x in unique]
        if mode == 1:
            ret += len([x for x in output if len(x) in {2, 3, 4, 7}])
        else:
            digits = {}
            def find_digit(number, test):
                temp = [x for x in unique if test(x)]
                if len(temp) != 1:
                    raise Exception(f"Too many digits for {number}")
                unique.remove(temp[0])
                digits[number] = temp[0]

            find_digit(1, lambda x: len(x) == 2)
            find_digit(7, lambda x: len(x) == 3)
            find_digit(4, lambda x: len(x) == 4)
            find_digit(8, lambda x: len(x) == 7)
            find_digit(9, lambda x: len(x ^ (digits[7] | digits[4])) == 1)
            find_digit(0, lambda x: digits[1] < x and len(x) == 6)
            find_digit(6, lambda x: len(x) == 6)
            find_digit(3, lambda x: digits[1] < x and len(x) == 5)
            find_digit(5, lambda x: len(digits[9] - x) == 1)
            find_digit(2, lambda x: x)

            digits = {"".join(sorted(y)): str(x) for x, y in digits.items()}
            ret += int("".join(digits["".join(sorted(x))] for x in output))
    return ret


def test(log):
    values_simple = log.decode_values("""
        acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf
    """)
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

    log.test(calc(log, values_simple, 1), 0)
    log.test(calc(log, values, 1), 26)
    log.test(calc(log, values_simple, 2), 5353)
    log.test(calc(log, values, 2), 61229)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))
