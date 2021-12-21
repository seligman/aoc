#!/usr/bin/env python3

from collections import deque

def get_desc():
    return 21, 'Day 21: Dirac Dice'

class State:
    __slots__ = ['roll', 'rolls', 'd', 'p1', 'p2', 'p1_score', 'p2_score', 'cur_step', 'winner', 'score', 'depth']

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
        self.score = None

    def copy(self):
        return State(self.p1, self.p2, self.p1_score, self.p2_score, self.roll, self.rolls, self.d, self.cur_step, self.depth)
    
    def step(self, mode):
        if self.cur_step == 0:
            self.roll = 0

        if 1 <= self.cur_step <= 3:
            self.roll += self.d
            self.rolls += 1
            self.d = 1 if self.d == 100 else self.d + 1

        if self.cur_step == 4:
            self.p1 += self.roll
            while self.p1 > 10:
                self.p1 -= 10
            self.p1_score += self.p1
            
            if self.p1_score >= (1000 if mode == 1 else 21):
                self.winner = 1
                self.score = self.p2_score * self.rolls
        
        if self.cur_step == 5:
            self.roll = 0
        
        if 6 <= self.cur_step <= 8:
            self.roll += self.d
            self.rolls += 1
            self.d = 1 if self.d == 100 else self.d + 1

        if self.cur_step == 9:
            self.p2 += self.roll
            while self.p2 > 10:
                self.p2 -= 10
            self.p2_score += self.p2
            
            if self.p2_score >= (1000 if mode == 1 else 21):
                self.winner = 2
                self.score = self.p1_score * self.rolls
        
        self.cur_step += 1
        if self.cur_step == 10:
            self.cur_step = 0
            self.depth += 1

def decode(known, state, target_depth):
    p1, p2 = 0, 0
    todo = deque([state])
    while len(todo) > 0:
        state = todo.popleft()
        if state.cur_step == 0 and state.depth == target_depth:
            key = (state.p1, state.p2, state.p1_score, state.p2_score)
            if key not in known:
                known[key] = decode(known, state, target_depth+1)
            p1 += known[key][0]
            p2 += known[key][1]
        else:
            state.step(2)
            if state.winner is not None:
                if state.winner == 1:
                    p1 += 1
                else:
                    p2 += 1
            else:
                if state.cur_step in {1, 2, 3, 6, 7, 8}:
                    for i in range(3):
                        temp = state.copy()
                        temp.d = i + 1
                        todo.append(temp)
                else:
                    todo.append(state)
    return p1, p2

def calc(log, values, mode):
    p1, p2 = [int(x.split(": ")[1]) for x in values]
    state = State(p1, p2)
    if mode == 1:
        while True:
            state.step(mode)
            if state.winner is not None:
                return state.score
    else:
        wins = [0, 0, 0]
        p1, p2 = decode({}, state, 1)
        return max(p1, p2)

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
