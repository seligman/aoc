#!/usr/bin/env python3

from collections import deque

DAY_NUM = 21
DAY_DESC = 'Day 21: Dirac Dice'

class State:
    __slots__ = ['roll', 'rolls', 'd', 'p1', 'p2', 'p1_score', 'p2_score', 'cur_step', 'winner', 'depth']

    def __init__(self, p1, p2, p1_score=0, p2_score=0, roll=0, rolls=0, d=1, cur_step=0, depth=0):
        self.roll = roll
        self.rolls = rolls
        self.d = d
        self.p1 = p1
        self.p2 = p2
        self.p1_score = p1_score
        self.p2_score = p2_score
        self.cur_step = cur_step
        self.depth = depth
        self.winner = None

    def copy(self, d):
        return State(self.p1, self.p2, self.p1_score, self.p2_score, self.roll, self.rolls, d, self.cur_step, self.depth)
    
    def step(self, mode):
        if self.cur_step == 0:
            self.roll = 0
        elif 1 <= self.cur_step <= 3:
            self.roll += self.d
            self.rolls += 1
            self.d = (self.d % 100) + 1
        elif self.cur_step == 4:
            self.p1 = (((self.p1 - 1) + self.roll) % 10) + 1
            self.p1_score += self.p1
            if self.p1_score >= (1000 if mode == 1 else 21):
                self.winner = 1
                return False
            self.roll = 0
        elif 5 <= self.cur_step <= 7:
            self.roll += self.d
            self.rolls += 1
            self.d = (self.d % 100) + 1
        elif self.cur_step == 8:
            self.p2 = (((self.p2 - 1) + self.roll) % 10) + 1
            self.p2_score += self.p2
            if self.p2_score >= (1000 if mode == 1 else 21):
                self.winner = 2
                return False
            self.cur_step = -1
            self.depth += 1
        
        self.cur_step += 1

        return True

def decode(known, state, target_depth):
    wins = [0, 0]
    todo = deque([state])
    while len(todo) > 0:
        state = todo.pop()
        if state.cur_step == 0 and state.depth == target_depth:
            key = (state.p1, state.p2, state.p1_score, state.p2_score)
            if key not in known:
                known[key] = decode(known, state, target_depth+1)
            wins = [known[key][0] + wins[0], known[key][1] + wins[1]]
        else:
            if not state.step(2):
                wins[state.winner - 1] += 1
            else:
                if state.cur_step in {1, 2, 3, 5, 6, 7}:
                    todo.append(state.copy(1))
                    todo.append(state.copy(2))
                    todo.append(state.copy(3))
                else:
                    todo.append(state)
    return wins

def calc(log, values, mode):
    p1, p2 = [int(x.split(": ")[1]) for x in values]
    state = State(p1, p2)
    if mode == 1:
        while state.step(mode):
            pass
        if state.winner == 0:
            return state.p1_score * state.rolls
        else:
            return state.p2_score * state.rolls
    else:
        return max(decode({}, state, 1))

def test(log):
    values = log.decode_values("""
        Player 1 starting position: 4
        Player 2 starting position: 8
    """)

    log.test(calc(log, values, 1), 739785)
    log.test(calc(log, values, 2), 444356092776315)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in [[], ["Puzzles"], ["..", "Puzzles"]]:
                cur = os.path.join(*(dn + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!"); exit(1)
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
