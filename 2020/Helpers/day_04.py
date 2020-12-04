#!/usr/bin/env python

import re

def get_desc():
    return 4, 'Day 4: Passport Processing'

def calc(log, values, mode):
    seen = {}
    ret = 0
    needed = set([
        "byr",
        "iyr",
        "eyr",
        "hgt",
        "hcl",
        "ecl",
        "pid",
        # "cid",
    ])
    for cur in values + [""]:
        if len(cur) == 0 or cur == "-":
                missing = 0
                present = 0
                for x in needed:
                    if x in seen:
                        if mode == 1:
                            good = True
                        else:
                            good = False
                            if x == "byr":
                                if int(seen[x]) >= 1920 and int(seen[x]) <= 2002:
                                    good = True
                            elif x == "iyr":
                                if int(seen[x]) >= 2010 and int(seen[x]) <= 2020:
                                    good = True
                            elif x == "eyr":
                                if int(seen[x]) >= 2020 and int(seen[x]) <= 2030:
                                    good = True
                            elif x == "hgt":
                                if seen[x][-2:] == "in":
                                    if int(seen[x][:-2]) >= 59 and int(seen[x][:-2]) <= 76:
                                        good = True
                                elif seen[x][-2:] == "cm":
                                    if int(seen[x][:-2]) >= 150 and int(seen[x][:-2]) <= 193:
                                        good = True
                            elif x == "hcl":
                                if re.search("^#[0-9a-f]{6}$", seen[x]) is not None:
                                    good = True
                            elif x == "ecl":
                                if seen[x] in {'amb', 'blu', 'brn', 'gry', "grn", "hzl", "oth"}:
                                    good = True
                            elif x == "pid":
                                if re.search("^[0-9]{9}$", seen[x]) is not None:
                                    good = True
                        if good:
                            present += 1
                        else:
                            missing += 1
                    else:
                        missing += 1
                if present == len(needed) and missing == 0:
                    ret += 1
                seen = {}
        else:
            cur = cur.split(' ')
            for x in cur:
                x = x.split(":")
                seen[x[0]] = x[1]

    return ret

def test(log):
    values = log.decode_values("""
        ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
        byr:1937 iyr:2017 cid:147 hgt:183cm

        iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
        hcl:#cfa07d byr:1929

        hcl:#ae17e1 iyr:2013
        eyr:2024
        ecl:brn pid:760753108 byr:1931
        hgt:179cm

        hcl:#cfa07d eyr:2025 pid:166559648
        iyr:2011 ecl:brn hgt:59in
    """)

    log.test(calc(log, values, 1), 2)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))
