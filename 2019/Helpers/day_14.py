#!/usr/bin/env python

def get_desc():
    return 14, 'Day 14: Space Stoichiometry'


def calc(log, values):
    import re

    reactions = {}

    r = re.compile("([0-9]+) ([A-Z]+)")
    for cur in values:
        source, dest = cur.split(" => ")
        dest_count, dest_name = r.search(dest).groups()
        dest_count = int(dest_count)

        reactions[dest_name] = {
            'count': dest_count,
            'sources': [],
        }

        for other in source.split(", "):
            other_count, other_name = r.search(other).groups()
            other_count = int(other_count)
            reactions[dest_name]['sources'].append((other_name, other_count))

    needed = {
        'FUEL': 1,
    }

    trillion = 1000000000000
    left_ore = trillion
    got_fuel = 0
    opf = None
    step = 0
    scale = trillion
    too_high = False
    safe_left, safe_needed = None, None

    while True:
        step += 1
        if step == 1:
            try_fuel = 1
        else:
            if too_high:
                if scale == 1:
                    break
                scale = scale // 10
                left_ore, needed = safe_left, safe_needed
            try_fuel = scale
        needed['FUEL'] = try_fuel
        safe_left, safe_needed = left_ore, needed.copy()
        too_high = False
        try:
            while True:
                found = False
                for key in list(needed):
                    if needed[key] > 0 and key != 'ORE':
                        found = True
                        while needed[key] > 0:
                            mult = needed[key] // reactions[key]['count']
                            if mult < 1:
                                mult = 1
                            needed[key] -= reactions[key]['count'] * mult
                            for val, val_count in reactions[key]['sources']:
                                if val == "ORE":
                                    if val_count > left_ore:
                                        raise Exception()
                                    left_ore -= val_count * mult
                                needed[val] = needed.get(val, 0) + val_count * mult
                if not found:
                    if opf is None:
                        opf = needed['ORE']
                    break
            got_fuel += try_fuel

        except:
            too_high = True

    return opf, got_fuel


def test(log):
    values = log.decode_values("""
        157 ORE => 5 NZVS
        165 ORE => 6 DCFZ
        44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
        12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
        179 ORE => 7 PSHF
        177 ORE => 5 HKGWZ
        7 DCFZ, 7 PSHF => 2 XJWVT
        165 ORE => 2 GPVTF
        3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT
    """)

    ret, expected = calc(log, values), (13312, 82892753) 
    log("Test returned %s, expected %s" % (str(ret), str(expected)))
    if ret != expected:
        return False

    return True


def run(log, values):
    ret = calc(log, values)
    log("One fuel requires: " + str(ret[0]))
    log("A trillion ore gives: " + str(ret[1]))
