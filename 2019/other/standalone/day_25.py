#!/usr/bin/env python3

def get_out(prog):
    l = ""
    while len(prog.output) > 0:
        l += chr(prog.get_output())
    return l


def add_in(prog, val):
    for cur in val + "\n":
        prog.add_to_input(ord(cur))


class Program:
    @staticmethod
    def make_ticker(values):
        return [int(x) for x in values[0].split(",")]

    @staticmethod
    def from_values(values, log, debug=False):
        ticker = Program.make_ticker(values)
        return Program(ticker, log, debug=debug)

    @staticmethod
    def debug(values, log=None):
        if log is None:
            log = DummyLog()
        values = [int(x) for x in values.split(",")]
        variables = {}
        off = 0
        log(" Offset    Val Op Code        'Description'")
        while off < len(values):
            off += Program.debug_line(log, values, off, variables=variables)

    @staticmethod
    def _to_string(value):
        ret = ""
        chars = "abcdefghijklmnopqrstuvwxyz"
        while True:
            ret += chars[int(value % 26)]
            value = int(value / 26)
            if value <= 0:
                break
        return ret[::-1]

    @staticmethod
    def debug_line(log, values, off, variables=None, relative=None):
        temp = Program([], 0)

        if values[off] % 100 not in temp.ops:
            log("{:7d} {:6d}".format(off, values[off]))
            return 1
        else:
            _func, name, params, desc = temp.ops[values[off] % 100]
            info = []
            for i in range(params):
                mode = (values[off] // [100, 1000, 10000][i]) % 10
                if mode == 1:
                    info.append(str(values[off + 1 + i]))
                elif mode == 0:
                    if variables is not None and values[off + 1 + i] >= len(values):
                        if values[off + 1 + i] not in variables:
                            variables[values[off + 1 + i]] = Program._to_string(len(variables))
                        info.append("[{}]".format(variables[values[off + 1 + i]]))
                    else:
                        info.append("[{}]".format(values[off + 1 + i]))
                elif mode == 2:
                    info.append("[{}+rel]".format(values[off + 1 + i]))
            desc = desc.format(*info)
            log("{:7d} {:6d} {:14s} {:5s} {:30s} {}".format(
                off, 
                values[off], 
                name, 
                "" if relative is None else str(relative),
                "'" + desc + "'", 
                ",".join([str(values[x + off]) for x in range(params + 1)]),
            ))
            return params + 1

    def make_copy(self):
        from collections import deque
        ret = Program([], self.log)
        ret.off = self.off
        ret.ticker = self.ticker.copy()
        ret.input = deque(self.input)
        ret.output = deque(self.output)
        ret.last_output = self.last_output
        ret.flag_running = self.flag_running
        ret.flag_input_dry = self.flag_input_dry
        ret.relative = self.relative
        return ret

    def __init__(self, ticker, log, debug=False):
        from collections import deque, defaultdict

        self.debug_frames = False
        self.frames = []
        self.show_debug = debug
        self.log = log
        self.ticker = defaultdict(int, [(i, ticker[i]) for i in range(len(ticker))])
        self.off = 0
        self.ops = {
            1: (self.op_add, "add", 3, "{} + {} -> {}"),
            2: (self.op_mult, "mult", 3, "{} * {} -> {}"),
            3: (self.op_input, "input", 1, "input -> {}"),
            4: (self.op_output, "output", 1, "{} -> output"),
            5: (self.op_jump_if_true, "jump_if", 2, "if {} != 0 then goto {}"),
            6: (self.op_jump_if_false, "jump_not", 2, "if {} == 0 then goto {}"),
            7: (self.op_less_than, "less_than", 3, "if {0} < {1} then 1 -> {2}, else 0 -> {2}"),
            8: (self.op_equals, "equals", 3, "if {0} == {1} then 1 -> {2}, else 0 -> {2}"),
            9: (self.op_relative, "set_relative", 1, "relative += {}"),
            90: (self.op_debug, "debug", 1, "debug {}"),
            99: (self.op_terminate, "terminate", 0, "exit"),
        }
        self.input = deque()
        self.output = deque()
        self.last_output = None
        self.source_output = None

        self.flag_running = True
        self.flag_input_dry = False
        self.relative = 0
        self.changes = None

    def look_for_changes(self):
        if self.changes is None:
            self.changes = self.ticker.copy()
            return {}
        else:
            ret = {}
            for key in self.ticker:
                if self.changes[key] != self.ticker[key]:
                    self.changes[key] = "changed"
                    ret[key] = self.ticker[key]
            return ret

    def save_frames(self):
        self.debug_frames = True

    def hook_up_output(self, source_output):
        self.source_output = source_output

    def add_to_input(self, value):
        if isinstance(value, list) or isinstance(value, tuple):
            for cur in value:
                self.input.appendleft(cur)
        else:
            self.input.appendleft(value)

    def peek_output(self, to_get=1):
        return self.output[-1]

    def get_output(self, to_get=1):
        if to_get == 1:
            return self.output.pop()
        else:
            return [self.output.pop() for _ in range(to_get)]

    def tick_till_end(self, allowed_reads=None):
        if allowed_reads is not None:
            from collections import deque
            temp = deque()
            while len(self.input) > allowed_reads:
                temp.append(self.input.popleft())
        while self.tick():
            pass
        if allowed_reads is not None:
            while len(temp) > 0:
                self.input.appendleft(temp.pop())

    def tick(self):
        if self.flag_running:
            self.flag_input_dry = False
            if self.show_debug:
                Program.debug_line(self.log, self.ticker, self.off, relative=self.relative)
            if self.debug_frames:
                self.frames.append([self.off, self.ticker.copy()])

            self.ops[self.ticker[self.off] % 100][0]()

            if self.debug_frames:
                if self.flag_input_dry:
                    self.frames.pop(-1)
        
        return (self.flag_running == True) and (self.flag_input_dry == False)

    def is_on_input(self):
        return self.ticker[self.off] % 100 == 3
        
    def is_on_output(self):
        return self.ticker[self.off] % 100 == 4
        
    def op_relative(self):
        self.relative += self.get_value(1)
        self.off += 2

    def op_debug(self):
        self.log("DEBUG: " + str(self.get_value(1)))
        self.off += 2

    def op_jump_if_true(self):
        if self.get_value(1) != 0:
            self.off = self.get_value(2)
        else:
            self.off += 3

    def op_jump_if_false(self):
        if self.get_value(1) == 0:
            self.off = self.get_value(2)
        else:
            self.off += 3

    def op_less_than(self):
        if self.get_value(1) < self.get_value(2):
            self.set_value(3, 1)
        else:
            self.set_value(3, 0)
        self.off += 4

    def op_equals(self):
        if self.get_value(1) == self.get_value(2):
            self.set_value(3, 1)
        else:
            self.set_value(3, 0)
        self.off += 4

    def op_input(self):
        if self.source_output is not None:
            while len(self.source_output.output) > 0:
                self.input.appendleft(self.source_output.output.pop())

        if len(self.input) > 0:
            temp = self.input.pop()
            if self.debug_frames:
                self.frames.append(["input", temp])
            self.set_value(1, temp)
            self.off += 2
        else:
            self.flag_input_dry = True

    def op_output(self):
        self.last_output = self.get_value(1)
        if self.debug_frames:
            self.frames.append(["output", self.last_output])
        self.output.appendleft(self.last_output)
        self.off += 2

    def op_terminate(self):
        self.off += 1
        self.flag_running = False

    def op_add(self):
        self.set_value(3, self.get_value(1) + self.get_value(2))
        self.off += 4

    def op_mult(self):
        self.set_value(3, self.get_value(1) * self.get_value(2))
        self.off += 4

    def get_value(self, index):
        mode = (self.ticker[self.off] // [0, 100, 1000, 10000][index]) % 10
        if mode == 2: # Relative
            return self.ticker[self.ticker[self.off + index] + self.relative]
        elif mode == 1: # Immediate
            return self.ticker[self.off + index]
        elif mode == 0: # Position
            return self.ticker[self.ticker[self.off + index]]
        else:
            raise Exception("Invalid get mode: " + str(mode))

    def set_value(self, index, value):
        mode = (self.ticker[self.off] // [0, 100, 1000, 10000][index]) % 10
        if mode == 2: # Relative
            self.ticker[self.ticker[self.off + index]+self.relative] = value
        elif mode == 0: # Position
            self.ticker[self.ticker[self.off + index]] = value
        else:
            raise Exception("Invalid set mode: " + str(mode))


def calc(log, values):
    import os
    import json

    if os.path.isfile("steps.json"):
        with open("steps.json") as f:
            steps = json.load(f)
    else:
        prog = Program.from_values(values, log)

        prog.tick_till_end()
        seen = set()
        final = None
        items = []
        seen.add(get_out(prog))

        from collections import deque
        todo = deque()
        todo.appendleft((prog.ticker.copy(), []))
        while len(todo) > 0:
            ticker, trail = todo.pop()
            for d in ["east", "west", "north", "south"]:
                prog.ticker = ticker.copy()
                add_in(prog, d)
                prog.tick_till_end()
                room = get_out(prog)
                if room not in seen:
                    seen.add(room)
                    if "Items here:" in room:
                        item_name = None
                        for cur in room.split("\n"):
                            if cur == "Items here:":
                                item_name = "--"
                            elif item_name == "--":
                                item_name = cur[2:]
                        items.append([False, item_name, trail + [d]])
                    elif "next" in room:
                        if final is None:
                            final = [trail + [d], room]
                    todo.appendleft((prog.ticker.copy(), trail + [d]))

        for i in range(len(items)):
            prog = Program.from_values(values, log)
            for cur in items[i][2]:
                add_in(prog, cur)
            prog.tick_till_end()
            get_out(prog)
            add_in(prog, "take " + items[i][1])
            add_in(prog, "inv")
            bail = 10000
            while prog.flag_running and bail > 0:
                bail -= 1
                prog.tick()
            if "Items in your inventory:\n- " + items[i][1] in get_out(prog):
                items[i][0] = True
            # log("Item: %s is %s" % (items[i][1], "valid" if items[i][0] else "invalid"))

        items = [x for x in items if x[0]]

        found_doors = False
        for cur in final[1].split("\n"):
            if cur == "Doors here lead:":
                found_doors = True
            elif found_doors:
                if cur[2:] != final[0][-1]:
                    final[0].append(cur[2:])
                    break

        import itertools
        rev = {
            "west": "east",
            "east": "west",
            "north": "south",
            "south": "north",
        }

        prog = Program.from_values(values, log)
        for item in items:
            for path in item[2]:
                add_in(prog, path)
            add_in(prog, "take " + item[1])
            for path in item[2][::-1]:
                add_in(prog, rev[path])
        for path in final[0][:-1]:
            add_in(prog, path)
        for item in items:
            add_in(prog, "drop " + item[1])
        prog.tick_till_end()
        get_out(prog)

        ticker = prog.ticker.copy()
        results = None

        for test_len in range(1, len(items)):
            for cur in itertools.combinations(items, test_len):
                prog.ticker = ticker.copy()
                for item in cur:
                    add_in(prog, "take " + item[1])
                prog.tick_till_end()
                get_out(prog)
                add_in(prog, final[0][-1])
                prog.tick_till_end()
                results = get_out(prog)

                if "keypad" in results:
                    # log("-- Items --")
                    # for item in cur:
                    #     log(item[1])
                    # log("-- Room --")
                    # log(results)

                    items_to_get = cur

                    break
                else:
                    results = None
            if results is not None:
                break

        last_path = []
        steps = []
        for item in items_to_get:
            path = item[2][:]
            print(item, path)
            while len(last_path) > 0 and len(path) > 0 and path[0] == last_path[0]:
                path.pop(0)
                last_path.pop(0)
            for cur in last_path[::-1]:
                steps.append(rev[cur])
            for cur in path:
                steps.append(cur)
            steps.append("take " + item[1])
            last_path = item[2][:]

        path = final[0]
        print("final", path)
        while len(last_path) > 0 and len(path) > 0 and path[0] == last_path[0]:
            path.pop(0)
            last_path.pop(0)
        for cur in last_path[::-1]:
            steps.append(rev[cur])
        for cur in path:
            steps.append(cur)

        with open("steps.json", "w") as f:
            json.dump(steps, f, indent=2)

    lines = [""] * 30
    frame = [0]
    prog = Program.from_values(values, log)
    for step in steps:
        prog.tick_till_end()
        animate_text(lines, prog, frame)
        for _ in range(15):
            draw_text(lines, frame)

        lines[-1] += "$"
        print("Step: " + step)
        for x in step:
            lines[-1] += x
            draw_text(lines, frame)
        lines.pop(0)
        lines.append("")
        draw_text(lines, frame)
        
        for _ in range(15):
            draw_text(lines, frame)

        add_in(prog, step)

    prog.tick_till_end()
    animate_text(lines, prog, frame)
    for _ in range(30):
        draw_text(lines, frame)


def animate_text(lines, prog, frame):
    added = 0
    for x in get_out(prog):
        added += 1
        if x == "\n":
            lines.pop(0)
            lines.append("")
        else:
            if len(lines[-1]) >= 70 and x == ' ':
                lines.pop(0)
                lines.append("")
            else:
                lines[-1] += x
        if added == 5:
            added = 0
            draw_text(lines, frame)
    draw_text(lines, frame)


def draw_text(lines, frame):
    from PIL import Image, ImageDraw, ImageFont
    fnt_source = ImageFont.truetype('SourceCodePro-Bold.ttf', 14)
    fnt_size = fnt_source.getsize("0")

    im = Image.new('RGB', (
        fnt_size[0] * 80 + 10, 
        fnt_size[1] * 30 + 15,
    ), color=(0, 0, 0))

    d = ImageDraw.Draw(im, 'RGBA')
    x, y = 5, 5
    for cur in lines:
        color = (255, 255, 255)
        if cur.startswith("$"):
            color = (192, 192, 255)
            cur = cur[1:]
        if len(cur) > 0:
            d.text((x, y), cur, color, font=fnt_source)
        y += fnt_size[1]
    del d

    im.save("frame_%05d.png" % (frame[0],))
    if frame[0] % 10 == 0:
        print("Frame: " + str(frame[0]))
    frame[0] += 1


class DummyLog:
    def __init__(self):
        pass

    def __call__(self, value):
        print(value)

    def show(self, value):
        print(value)


if __name__ == "__main__":
    values = []
    with open("day_25_input.txt") as f:
        values = [x.strip() for x in f]

    calc(DummyLog(), values)
