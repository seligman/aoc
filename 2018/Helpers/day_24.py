#!/usr/bin/env python3

import re

DAY_NUM = 24
DAY_DESC = 'Day 24: Immune System Simulator 20XX'


# Just store stats for a group
class Group():
    def __init__(self, army, group_id, units, hp, specials, attack, attack_type, initiative):
        self.id = group_id
        self.units = units
        self.hp = hp
        self.specials = specials
        self.attack = attack
        self.attack_type = attack_type
        self.initiative = initiative
        self.army = army

        # These are updated during each round
        self.picked = False
        self.target = None
        self.damage = 0
        self.killed = 0
        self.mult = 0


def calc(values, boost):
    groups = []
    army = ""
    armies = {}

    # Crack out all of the groups
    r = re.compile("([0-9]+) units each with ([0-9]+) hit points (\\((.*)\\) |)with an attack that does ([0-9]+) (.*) damage at initiative ([0-9]+)")

    for cur in values:
        # Note when we move from the immune system to the infection "system"
        if cur == "Immune System:":
            army = "immune"
            armies[army] = 1
        elif cur == "Infection:":
            army = "infection"
            armies[army] = 1
        elif len(cur) > 0:
            # Crack the data out
            m = r.search(cur)
            if army == "immune":
                boost_army = boost
            else:
                boost_army = 0
            group = Group(army, armies[army], int(m.group(1)), int(m.group(2)), m.group(4), int(m.group(5)) + boost_army, m.group(6), int(m.group(7)))
            armies[army] += 1
            groups.append(group)

    # And fix up the "specials" so they're simple sets            
    for cur in groups:
        if cur.specials is None:
            cur.specials = set()
        else:
            temp = cur.specials.split("; ")
            cur.specials = set()
            for temp_cur in temp:
                flavor = None
                for sub in temp_cur.split(", "):
                    if sub.startswith("weak to "):
                        flavor = "weak to "
                        cur.specials.add(sub)
                    elif sub.startswith("immune to "):
                        flavor = "immune to "
                        cur.specials.add(sub)
                    else:
                        if " to " in sub:
                            raise Exception()
                        else:
                            cur.specials.add(flavor + sub)

    while True:
        # Reset the state
        for cur in groups:
            cur.picked = False
            cur.target = None
            cur.damage = 0
            cur.killed = 0

        # Sort by picking order
        groups.sort(key=lambda x: (x.units * x.attack, x.initiative), reverse=True)

        for cur in groups:
            best_option = None
            for sub in groups:
                if (not sub.picked) and (sub.units > 0):
                    if sub.army != cur.army:
                        # Figure out how much damager we do
                        mult = 1
                        if ("immune to " + cur.attack_type) in sub.specials:
                            mult = 0
                        if ("weak to " + cur.attack_type) in sub.specials:
                            mult = 2
                        
                        if mult > 0:
                            # Score it, and if it's better than the picked option, pick it
                            sub.damage = cur.attack * cur.units * mult
                            sub.mult = mult
                            if best_option is None:
                                best_option = sub
                            else:
                                if sub.damage > best_option.damage:
                                    best_option = sub
                                elif sub.damage == best_option.damage:
                                    if sub.units * sub.attack > best_option.units * best_option.attack:
                                        best_option = sub
                                    elif sub.units * sub.attack == best_option.units * best_option.attack:
                                        if sub.initiative > best_option.initiative:
                                            best_option = sub

            if best_option is not None:
                # We picked something, note the pick
                cur.target = best_option
                best_option.picked = True

        # Sort by initiative
        groups.sort(key=lambda x: (x.initiative,), reverse=True)

        # Track how many groups did damage
        did_damage = 0

        for cur in groups:
            if cur.units > 0:
                if cur.target is not None:
                    # Need to recalc damage, since a group's units might have changed
                    cur.target.damage = cur.attack * cur.units * cur.target.mult
                    cur.target.killed = cur.target.damage // cur.target.hp
                    if cur.target.killed > 0:
                        did_damage += 1
                    cur.target.units -= cur.target.damage // cur.target.hp
                    if cur.target.units <= 0:
                        # We killed this group, drop the count
                        armies[cur.army] -= 1

        if min(armies.values()) == 1:
            # The next ID for this army is one, that means it's out of groups, so it lost
            break

        if did_damage == 0:
            # No one's left standing that can attack and do damage, so no one wins
            return 0, 'nobody'

    # Count the remaining alive groups
    ret = 0
    for cur in groups:
        if cur.units > 0:
            ret += cur.units
            # Note the winning army
            winning = cur.army

    return ret, winning


def run(log, values):
    # Basic run is simple
    ret = calc(values, 0)
    log.show("The %s system wins with %d units" % (ret[1], ret[0]))

    # A simple binary search for the lowest option
    boost = 1
    span = 64
    found = {0: ret}
    while True:
        if boost not in found:
            found[boost] = calc(values, boost)
        if boost-1 not in found:
            found[boost-1] = calc(values, boost - 1)

        if found[boost][1] == "immune":
            if found[boost-1][1] != "immune":
                # This means we found the best option
                break
            # We're too high, so skip back
            span = span // 2
            boost = max(1, boost - span)
        else:
            boost += span

    log.show("The %s system wins with %d units, with an immune boost of %d" % (found[boost][1], found[boost][0], boost))


def test(log):
    values = [
        "Immune System:",
        "17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2",
        "989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3",
        "",
        "Infection:",
        "801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1",
        "4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4",
    ]

    temp = calc(values, 0)
    log.show(temp)
    if temp == (5216, "infection"):
        temp = calc(values, 1570)
        log.show(temp)
        if temp == (51, "immune"):
            return True
        else:
            return False
    else:
        return False
