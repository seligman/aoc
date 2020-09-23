#!/usr/bin/env python

def get_desc():
    return 2, 'Day 2: Bathroom Security'


def calc(values, mode):
    steps = {}

    if mode == 0:
        keypad = [
            "     ",
            " 123 ",
            " 456 ",
            " 789 ",
            "     ",
        ]
    else:
        keypad = [
            "       ",
            "   1   ",
            "  234  ",
            " 56789 ",
            "  ABC  ",
            "   D   ",
            "       ",
        ]

    keypad = [list(x) for x in keypad]
    for y in range(0, len(keypad)):
        for x in range(0, len(keypad[0])):
            if keypad[y][x] != ' ':
                steps[keypad[y][x]] = {
                    'U': keypad[y][x] if keypad[y-1][x] == " " else keypad[y-1][x],
                    'D': keypad[y][x] if keypad[y+1][x] == " " else keypad[y+1][x],
                    'L': keypad[y][x] if keypad[y][x-1] == " " else keypad[y][x-1],
                    'R': keypad[y][x] if keypad[y][x+1] == " " else keypad[y][x+1],
                }


    ret = ""

    digit = '5'
    for line in values:
        for cur in line:
            digit = steps[digit][cur]
        ret += digit

    return ret


def test(log):
    values = [
        "ULL",
        "RRDDD",
        "LURDL",
        "UUUUD",
    ]

    if calc(values, 0) == "1985":
        return True
    else:
        return False


def run(log, values):
    log.show(calc(values, 0))
    log.show(calc(values, 1))
