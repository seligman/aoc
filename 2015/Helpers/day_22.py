#!/usr/bin/env python3

from collections import deque

DAY_NUM = 22
DAY_DESC = 'Day 22: Wizard Simulator 20XX'


class History:
    def __init__(self, log):
        self.log = log
        self.player_wins = 0
        self.boss_wins = 0
        self.gave_up = 0
        self.best_mana = None
        self.notes = 0
        self.states = None

    def log_player_win(self, mana_spent):
        self.player_wins += 1
        if self.best_mana is None or mana_spent < self.best_mana:
            self.best_mana = mana_spent
        self.note()

    def log_boss_win(self):
        self.boss_wins += 1
        self.note()

    def log_gave_up(self):
        self.gave_up += 1
        self.note()

    def note(self):
        self.notes += 1
        if False and self.notes % 100000 == 0:
            self.log("Player: %8d, Boss: %8d, Gave Up: %8d, Best Mana: %5d: States: %5d" % (
                self.player_wins, 
                self.boss_wins, 
                self.gave_up,
                0 if self.best_mana is None else self.best_mana,
                len(self.states),
            ))


class Character:
    def __init__(self, name, hp, damage, spells, mana, armor):
        self.mana_spent = 0
        self.name = name
        self.hp = hp
        self.damage = damage
        self.spells = spells
        self.mana = mana
        self.armor = armor
        self.effects = None
        if self.spells is not None:
            self.effects = {}

    def clone(self):
        ret = Character(self.name, self.hp, self.damage, self.spells, self.mana, self.armor)
        if self.effects is not None:
            for key in self.effects:
                value = self.effects[key]
                ret.effects[key] = value[:]
        ret.mana_spent = self.mana_spent
        return ret


class Spell:
    def __init__(self, name, cost, effect, damage, heal, armor, earn_mana):
        self.name = name
        self.cost = cost
        self.effect = effect
        self.damage = damage
        self.heal = heal
        self.armor = armor
        self.earn_mana = earn_mana


def apply_effects(history, player, boss):
    to_del = []
    for key in player.effects:
        value = player.effects[key]
        value[0] -= 1
        if value[0] <= 0:
            to_del.append(key)
            player.armor -= value[1].armor
        player.hp += value[1].heal
        boss.hp -= value[1].damage
        player.mana += value[1].earn_mana

        if value[2]:
            value[2] = False
            player.armor += value[1].armor

    for key in to_del:
        del player.effects[key]


def run_spell(history, spell, player, boss, states, game_mode):
    if spell is not None:
        player.mana -= spell.cost
        player.mana_spent += spell.cost

        if history.best_mana is not None and player.mana_spent >= history.best_mana:
            history.log_gave_up()
            return

        if spell.effect == 0:
            boss.hp -= spell.damage
            player.mana += spell.earn_mana
            player.hp += spell.heal
            player.armor += spell.armor
        else:
            player.effects[spell.name] = [spell.effect, spell, True]

        if boss.hp <= 0:
            history.log_player_win(player.mana_spent)
            return

        apply_effects(history, player, boss)
        if boss.hp <= 0:
            history.log_player_win(player.mana_spent)
            return

        player.hp -= max(1, boss.damage - player.armor)
        if player.hp <= 0:
            history.log_boss_win()
            return

    if not run_board(history, player, boss, states, game_mode):
        return

    return


def run_board(history, player, boss, states, game_mode):
    if game_mode == 1:
        player.hp -= 1
        if player.hp <= 0:
            history.log_boss_win()
            return

    apply_effects(history, player, boss)

    if boss.hp <= 0:
        history.log_player_win(player.mana_spent)
        return

    cast = 0
    for spell in player.spells:
        if spell.cost <= player.mana and spell.name not in player.effects:
            player_temp = player.clone()
            if spell.effect > 0:
                player_temp.effects[spell.name] = None
            cast += 1
            states.append((spell, player_temp, boss.clone()))

    if cast == 0:
        history.log_boss_win()

    return


def calc(log, values, game_mode):
    boss = Character("boss", int(values[0].split(": ")[1]), int(values[1].split(": ")[1]), None, 0, 0)
    player = Character("player", 50, 0, [
        Spell("missle", 53, 0, 4, 0, 0, 0),
        Spell("drain", 73, 0, 2, 2, 0, 0),
        Spell("shield", 113, 6, 0, 0, 7, 0),
        Spell("poison", 173, 6, 3, 0, 0, 0),
        Spell("recharge", 229, 5, 0, 0, 0, 101),
    ], 500, 0)

    history = History(log)
    states = deque()
    history.states = states
    states.append((None, player, boss))
    while len(states) > 0:
        cur = states.pop()
        run_spell(history, cur[0], cur[1], cur[2], states, game_mode)

    log("Boss Wins: " + str(history.boss_wins))
    log("Player Wins: " + str(history.player_wins))
    log("Gave Up: " + str(history.gave_up))
    log(">> Best Mana Spent: " + str(history.best_mana))


def test(log):
    return True


def run(log, values):
    for game_mode in range(2):
        temp = [
            "Normal Game Mode",
            "Hard Game Mode",
        ][game_mode]
        log("%s %s %s" % ("#" * 5, temp, "#" * (60 - len(temp)),))
        calc(log, values[:], game_mode)

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2015/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
