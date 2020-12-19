#!/usr/bin/env python3

from collections import defaultdict
import inspect

class Instruction:
    def __init__(self, value):
        if value is None:
            self.op = None
            self.vals = None
        else:
            value = value.split(' ')
            self.op = value[0]
            self.vals = [value[1]]
    
    def get_val(self, program, index=0):
        return int(self.vals[index])

    def clone(self):
        ret = Instruction(None)
        ret.op = self.op
        ret.vals = self.vals[:]
        return ret


class Program:
    def __init__(self, values, log=None):
        self.log = log
        self.acc = 0
        self.pc = 0
        self.instructions = [Instruction(x) for x in values]
        self.visited = defaultdict(int)
        self.increment_pc = True
        self.ops = {x[0][3:]:x[1] for x in inspect.getmembers(self) if x[0].startswith("op_")}
        self.frame = 0
        self.steps = 0

    def show(self):
        from PIL import Image, ImageDraw, ImageFont
        import os

        source_code = os.path.join('Helpers', 'Font-SourceCodePro-Bold.ttf')
        source_code = ImageFont.truetype(source_code, int(float(12) * 1.5))
        w, h = 0, 0
        for x in range(32, 126):
            test = source_code.getsize(chr(x))
            w, h = max(w, test[0]), max(h, test[1])

        im = Image.new('RGB', (w * 47, h * 7), color=(0, 0, 0))
        d = ImageDraw.Draw(im, 'RGBA')

        y = 0
        d.rectangle(((0, 3 * h), (20 * w, 4 * h)), fill=(0, 0, 128))
        for pc in range(self.pc - 3, self.pc + 4):
            if pc >= 0 and pc < len(self.instructions):
                msg = f"{pc:4d}: {self.instructions[pc].op:<3} {', '.join(self.instructions[pc].vals)}"
                d.text((0, y * h), msg, (255, 255, 255), font=source_code)
            y += 1
        
        d.rectangle(((25 * w - 5, 1 * h - 5), (45 * w + 5, 4 * h + 5)), fill=(64, 64, 64))
        d.text((25 * w, 1 * h), f"pc: {self.pc}", (255, 255, 255), font=source_code)
        d.text((25 * w, 2 * h), f"acc: {self.acc}", (255, 255, 255), font=source_code)
        d.text((25 * w, 3 * h), f"steps: {self.steps}", (255, 255, 255), font=source_code)
        im.save("frame_%05d.png" % (self.frame,))
        self.frame += 1

    def clone(self):
        ret = Program([])
        ret.log = self.log
        ret.acc = self.acc
        ret.pc = self.pc
        ret.instructions = [x.clone() for x in self.instructions]
        ret.visited = self.visited.copy()
        ret.increment_pc = self.increment_pc
        ret.steps = self.steps
        ret.frame = self.frame
        return ret

    def op_nop(self, ins):
        if ins is None:
            return "No op"

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
        self.steps += 1
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
