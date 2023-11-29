#!/usr/bin/env python3

import math

class Program:
    def __init__(self, values):
        self.values = values
        self.pc = 0
        self.regs = {'x': 1}
        self.cycles = 0
        self.ins = None

    def run(self):
        while True:
            self.ins = self.values[self.pc]
            ins = self.ins.split(' ')

            ins_cycles = 1

            if ins[0] == "addx":
                ins_cycles = 2

            for _ in range(ins_cycles):
                self.cycles += 1
                yield True

            if ins[0] == "addx":
                self.regs['x'] += int(ins[1])
            
            self.pc += 1

            if self.pc >= len(self.values):
                break
