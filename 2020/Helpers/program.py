#!/usr/bin/env python3

from collections import defaultdict
import inspect

class Instruction:
    def __init__(self, value):
        value = value.split(' ')
        self.op = value[0]
        self.vals = [value[1]]
    
    def get_val(self, program, index=0):
        return int(self.vals[index])


class Program:
    def __init__(self, values, log=None):
        self.log = log
        self.acc = 0
        self.pc = 0
        self.instructions = [Instruction(x) for x in values]
        self.visited = defaultdict(int)
        self.increment_pc = True

        self.ops = {x[0][3:]:x[1] for x in inspect.getmembers(self) if x[0].startswith("op_")}

    def op_nop(self, ins):
        if ins is None:
            return "No op"
        pass

    def op_acc(self, ins):
        if ins is None:
            return "Accumulate"
        self.acc += ins.get_val(self)

    def op_jmp(self, ins):
        if ins is None:
            return "Jump by offset"
        self.increment_pc = False
        self.pc += ins.get_val(self)

    def step(self):
        self.visited[self.pc] += 1
        self.increment_pc = True
        ins = self.instructions[self.pc]
        old_pc = self.pc

        if ins.op in self.ops:
            self.ops[ins.op](ins)
        else:
            raise Exception("Invalid op " + ins.op)

        if self.increment_pc:
            self.pc += 1

        if self.log:
            msg = f"{old_pc:3d} [acc:{self.acc}]: {ins.op} {','.join(ins.vals)} # {self.ops[ins.op](None)}"
            if not self.increment_pc:
                msg += f", jump to {self.pc}"
            self.log(msg)

        return self.pc < len(self.instructions)

    def seen_pc(self):
        return self.visited[self.pc] >= 1
