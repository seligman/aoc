#!/usr/bin/env python

from collections import defaultdict

class Instruction:
    def __init__(self, value):
        value = value.split(' ')
        self.op = value[0]
        self.val = int(value[1])

class Program:
    def __init__(self, values, log=None):
        self.log = log
        self.acc = 0
        self.pc = 0
        self.instructions = [Instruction(x) for x in values]
        self.visited = defaultdict(int)

    def step(self):
        self.visited[self.pc] += 1

        cur = self.instructions[self.pc]
        old_pc = self.pc
        increment_pc = True
        if cur.op == "nop":
            pass # No Op
        elif cur.op == "acc":
            # Accumulate
            self.acc += cur.val
        elif cur.op == "jmp":
            # Offset Jump
            self.pc += cur.val
            increment_pc = False
        else:
            raise Exception("Invalid op " + cur.op)
        
        if increment_pc:
            self.pc += 1

        if self.log:
            self.log(f"{old_pc:3d}: {cur.op} {cur.val:4d} -> {self.pc}: {self.acc}")

        return self.pc < len(self.instructions)

    def seen_pc(self):
        return self.visited[self.pc] >= 1
