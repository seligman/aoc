#!/usr/bin/env python3

# Animation: https://imgur.com/a/nyVEK2j

DAY_NUM = 5
DAY_DESC = 'Day 5: Supply Stacks'

class TrackableLetter:
    def __init__(self, value, letter_id):
        self.value = value
        self.letter_id = letter_id

    def __str__(self):
        return self.value

def calc(log, values, mode, draw=False, info={}, get_info=False, replace_pattern=None):
    if draw:
        from grid import Grid
        animated = Grid()

    letters = []
    stacks = []
    values = [x.lstrip(".") for x in values]
    while True:
        row = values.pop(0)
        if row.strip().startswith("1"):
            break
        for i, val in enumerate(row):
            if 'A' <= val <= 'Z':
                i = int((i - 1) / 4)
                while len(stacks) <= i:
                    stacks.append([])
                val = TrackableLetter(val, len(letters))
                letters.append(val)
                stacks[i].append(val)
                if replace_pattern is not None:
                    val.value = replace_pattern[val.letter_id]

    for i in range(len(stacks)):
        stacks[i] = stacks[i][::-1]

    def save_grid(target=None):
        if draw or target is not None:
            for x in range(len(stacks)):
                for y in range(info['max_height'] - 1, -1, -1):
                    if draw:
                        animated[(x, info['max_height']-y)] = " " if y >= len(stacks[x]) else str(stacks[x][y])
                    if target is not None:
                        target.append(None if y >= len(stacks[x]) else stacks[x][y])
            if draw:
                animated.save_frame()

    import re
    if draw:
        slow_at = info['frames'] - 2
        info['frames'] = 0
        get_info = True

    for row in values:
        m = re.search("move ([0-9]+) from ([0-9]+) to ([0-9]+)", row)
        if m is not None:
            steps = list(map(int, m.groups()))
            if mode == 1:
                for _ in range(steps[0]):
                    if draw:
                        if info['frames'] >= slow_at:
                            save_grid()
                    stacks[steps[2]-1].append(stacks[steps[1]-1].pop())
                    if get_info:
                        info['max_height'] = max(info.get('max_height', 0), max(len(x) for x in stacks))
                save_grid()
                if get_info:
                    info['frames'] = info.get('frames', 0) + 1
            else:
                temp = []
                for _ in range(steps[0]):
                    temp.append(stacks[steps[1]-1].pop())
                stacks[steps[2]-1] += temp[::-1]

    ret = ""
    for cur in stacks:
        ret += str(cur[-1])

    if get_info:
        info['tracked'] = []
        save_grid(target=info['tracked'])

    if draw:
        animated.draw_frames(cell_size=(15, 15))

    if get_info:
        return info

    return ret

def other_draw_nggyu(describe, values):
    if describe:
        return "Draw this, in the style of Rick Astley"
    from dummylog import DummyLog
    import animate
    animate.prep()
    info = calc(DummyLog(), values, 1, get_info=True)

    words = "NEVERGONNAGIVEYOUUPNEVERGONNALETYOUDOWNNEVERGONNARUNAROUNDANDDESERTYOUNEVERGONNAMAKEYOUCRYNEVERGONNASAYGOODBYENEVERGONNATELLALIEANDHURTYOU"
    pattern = {}
    for cur in info['tracked']:
        if cur is not None:
            pattern[cur.letter_id] = words[0]
            words = words[1:]

    calc(DummyLog(), values, 1, draw=True, info=info, replace_pattern=pattern)
    animate.create_mp4(DAY_NUM, rate=10, final_secs=5)

def other_draw(describe, values):
    if describe:
        return "Draw this"
    from dummylog import DummyLog
    import animate
    animate.prep()
    info = calc(DummyLog(), values, 1, get_info=True)
    calc(DummyLog(), values, 1, draw=True, info=info)
    animate.create_mp4(DAY_NUM, rate=10, final_secs=5)

def test(log):
    values = log.decode_values("""
        .    [D]    
        .[N] [C]    
        .[Z] [M] [P]
        . 1   2   3 
        .
        .move 1 from 2 to 1
        .move 3 from 1 to 3
        .move 2 from 2 to 1
        .move 1 from 1 to 2
    """)

    log.test(calc(log, values, 1), 'CMZ')
    log.test(calc(log, values, 2), 'MCD')

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
