#!/usr/bin/env python3

def get_desc():
    return 8, 'Day 8: Seven Segment Search'

def calc(log, values, mode):
    ret = 0
    for cur in values:
        unique, output = [x.strip().split() for x in cur.split("|")]
        unique = [set(x) for x in unique]
        if mode == 1:
            ret += len([x for x in output if len(x) in {2, 3, 4, 7}])
        else:
            digits = {}
            def find_digit(number, test):
                temp = [x for x in unique if test(x)]
                if len(temp) != 1:
                    raise Exception(f"Too many digits for {number}")
                unique.remove(temp[0])
                digits[number] = temp[0]

            find_digit(1, lambda x: len(x) == 2)
            find_digit(7, lambda x: len(x) == 3)
            find_digit(4, lambda x: len(x) == 4)
            find_digit(8, lambda x: len(x) == 7)
            find_digit(9, lambda x: len(x ^ (digits[7] | digits[4])) == 1)
            find_digit(0, lambda x: digits[1] < x and len(x) == 6)
            find_digit(6, lambda x: len(x) == 6)
            find_digit(3, lambda x: digits[1] < x and len(x) == 5)
            find_digit(5, lambda x: len(digits[9] - x) == 1)
            find_digit(2, lambda x: x)

            digits = {"".join(sorted(y)): str(x) for x, y in digits.items()}
            ret += int("".join(digits["".join(sorted(x))] for x in output))
    return ret

def rotate(origin, point, angle):
    import math
    angle = math.radians(angle)
    ox, oy = origin
    px, py = point
    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy

def get_segment(origin, angle, size):
    return [
        rotate(origin, (origin[0] + -(size*2.5), origin[1] + 0), angle),
        rotate(origin, (origin[0] + -(size*1.5), origin[1] + -size), angle),
        rotate(origin, (origin[0] + (size*1.5), origin[1] + -size), angle),
        rotate(origin, (origin[0] + (size*2.5), origin[1] + 0), angle),
        rotate(origin, (origin[0] + (size*1.5), origin[1] + size), angle),
        rotate(origin, (origin[0] + -(size*1.5), origin[1] + size), angle),
    ]

def ease(value):
    import math
    value = max(0, min(1, value))
    if value < 0.5:
        return 4 * (value ** 3)
    else:
        return 1 - math.pow(-2 * value + 2, 3) / 2

def other_draw(describe, values):
    if describe:
        return "Animate digits"
    import animate
    animate.prep()
    create_frames(values[0])
    animate.create_mp4(get_desc(), rate=30)


def draw_segment(data, dr, pt, on, step):
    pos_valid = [
        (pt[0], pt[1] - 100, 0),
        (pt[0] - 50, pt[1] - 50, 90),
        (pt[0] + 50, pt[1] - 50, 90),
        (pt[0], pt[1], 0),
        (pt[0] - 50, pt[1] + 50, 90),
        (pt[0] + 50, pt[1] + 50, 90),
        (pt[0], pt[1] + 100, 0),
    ]

    pos_invalid = [
        (pt[0] - 50, pt[1] + 120, 10),
        (pt[0] + 50, pt[1] + 140, -10),
        (pt[0] - 50, pt[1] + 160, 10),
        (pt[0] + 50, pt[1] + 180, -10),
        (pt[0] - 50, pt[1] + 200, 10),
        (pt[0] + 50, pt[1] + 220, -10),
        (pt[0] - 50, pt[1] + 240, 10),
    ]

    color = 0
    digits = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6}
    for cur in digits:
        if cur in data.animate:
            step = ease(step)
            a = pos_valid[digits[data.replace[cur]]]
            b = pos_invalid[digits[cur]]
            segment = (
                a[0] * step + b[0] * (1 - step),
                a[1] * step + b[1] * (1 - step),
                a[2] * step + b[2] * (1 - step),
            )
        elif cur in data.valid:
            segment = pos_valid[digits[data.replace[cur]]]
        else:
            segment = pos_invalid[digits[cur]]
        
        if cur in on:
            color = (240, 240, 210)
        else:
            color = (40, 40, 40)

        dr.polygon(get_segment((segment[0], segment[1]), segment[2], 18), color, (150, 150, 150))

def draw_all(data, step, pos=None, text=None):
    if data.todo is not None:
        data.todo.append(data.serialize({"step": step, "pos": pos, "text": text}))
        data.frame += 1
    else:
        import os
        from PIL import Image, ImageDraw, ImageFont
        source_code = os.path.join('Helpers', 'Font-SourceCodePro-Bold.ttf')
        fnt = ImageFont.truetype(source_code, 30)
        off = 0
        im = Image.new('RGB', (3350, 500))
        dr = ImageDraw.Draw(im)
        dr.rectangle((2400, 0, im.width, im.height), (50, 50, 80))
        for i, cur in enumerate(data.unique + data.output):
            draw_segment(data, dr, (off + 100, 130), cur, step)
            note = data.notes.get(i)
            if pos is not None:
                if pos == i:
                    note = text
            if note is not None:
                dr.text((off, 385), note, font=fnt)
            off += 240
        im.thumbnail((im.width // 2, im.height // 2))
        im.save(f"frame_{data.frame:05d}.png")
        return f"Saving frame {data.frame}"

def freeze(data):
    data.animate = ""
    for _ in range(15):
        draw_all(data, 0)

class Data:
    unique = ""
    output = ""
    frame = 0
    valid = ""
    animate = ""
    replace = {}
    notes = {}
    known = {}
    todo = None

    def serialize(self, other):
        return {
            "unique": self.unique,
            "output": self.output,
            "frame": self.frame,
            "valid": self.valid,
            "animate": self.animate,
            "replace": self.replace.copy(),
            "notes": self.notes.copy(),
            "known": self.known.copy(),
            "other": other,
        }
    
    @staticmethod
    def deserialize(data):
        ret = Data()
        ret.unique = data["unique"]
        ret.output = data["output"]
        ret.frame = data["frame"]
        ret.valid = data["valid"]
        ret.animate = data["animate"]
        ret.replace = data["replace"]
        ret.notes = data["notes"]
        ret.known = data["known"]
        return ret, data["other"]

def draw_helper(job):
    data, other = Data.deserialize(job)
    msg = draw_all(data, other["step"], other["pos"], other["text"])
    return msg

def create_frames(script):
    data = Data()
    data.unique, data.output = [x.split() for x in script.split(" | ")]
    data.todo = []

    def check_swap(a, b, dig):
        if a in [data.replace[x] for x in data.known[dig]]:
            swap = a + b
            reverse = {y:x for x,y in data.replace.items()}
            data.animate = "".join(reverse[x] for x in swap)
            data.valid = "".join([x for x in data.valid if x not in data.animate])
            for i in range(31):
                draw_all(data, (30 - i) / 30, pos, f" Must be '{dig}'")
            data.replace[data.animate[0]], data.replace[data.animate[1]] = data.replace[data.animate[1]], data.replace[data.animate[0]]
            for i in range(31):
                draw_all(data, i / 30, pos, f" Must be '{dig}'")
            data.valid += data.animate
        else:
            for i in range(31):
                draw_all(data, i / 30, pos, f" Must be '{dig}'")
        data.notes[pos] = f" Locked\n {dig}"
        freeze(data)

    def animate_cur(pos, dig):
        for i in range(31):
            draw_all(data, i / 30, pos, f" Must be '{dig}'")
        data.notes[pos] = f" Locked\n {dig}"
        data.valid += data.animate

    draw_all(data, 0)

    for pos, cur in enumerate(data.unique):
        if cur not in data.known.values():
            if len(cur) == 2:
                data.animate = cur
                data.known[1] = cur
                break
    data.replace[data.animate[0]] = "c"
    data.replace[data.animate[1]] = "f"
    animate_cur(pos, '1')
    freeze(data)

    for pos, cur in enumerate(data.unique):
        if cur not in data.known.values():
            if len(cur) == 3:
                data.animate = "".join(x for x in cur if x not in data.valid)
                data.known[7] = cur
                break
    data.replace[data.animate[0]] = "a"
    animate_cur(pos, '7')
    freeze(data)

    for pos, cur in enumerate(data.unique):
        if cur not in data.known.values():
            if len(cur) == 4:
                data.animate = "".join(x for x in cur if x not in data.valid)
                data.known[4] = cur
                break
    data.replace[data.animate[0]] = "b"
    data.replace[data.animate[1]] = "d"
    animate_cur(pos, '4')
    freeze(data)

    for pos, cur in enumerate(data.unique):
        if cur not in data.known.values():
            if len(cur) == 7:
                data.animate = "".join(x for x in cur if x not in data.valid)
                data.known[8] = cur
                break
    data.replace[data.animate[0]] = "e"
    data.replace[data.animate[1]] = "g"
    animate_cur(pos, '7')
    freeze(data)

    for pos, cur in enumerate(data.unique):
        if cur not in data.known.values():
            if len(set(cur) - (set(data.known[7]) | set(data.known[4]))) == 1:
                data.known[9] = cur
                data.animate = ""
                break
    check_swap('e', 'g', 9)

    for pos, cur in enumerate(data.unique):
        if cur not in data.known.values():
            if set(data.known[1]) < set(cur) and len(cur) == 6:
                data.known[0] = cur
                data.animate = ""
                break
    check_swap('d', 'b', 0)

    for pos, cur in enumerate(data.unique):
        if cur not in data.known.values():
            if len(cur) == 6:
                data.known[6] = cur
                data.animate = ""
                break
    check_swap('c', 'f', 6)

    for pos, cur in enumerate(data.unique):
        if cur not in data.known.values():
            if set(data.known[1]) < set(cur) and len(cur) == 5:
                data.known[3] = cur
                data.animate = ""
                break
    animate_cur(pos, '3')
    freeze(data)

    for pos, cur in enumerate(data.unique):
        if cur not in data.known.values():
            if len(set(data.known[9]) - set(cur)) == 1:
                data.known[5] = cur
                data.animate = ""
                break
    animate_cur(pos, '5')
    freeze(data)

    for pos, cur in enumerate(data.unique):
        if cur not in data.known.values():
            data.known[2] = cur
            data.animate = ""
            break
    animate_cur(pos, '2')
    freeze(data)

    for pos, cur in enumerate(data.unique + data.output):
        if pos >= len(data.unique):
            for key, value in data.known.items():
                if "".join(sorted(cur)) == "".join(sorted(value)):
                    data.notes[pos] = f"  {key}"
            freeze(data)

    import multiprocessing
    from datetime import datetime, timedelta
    next_msg = datetime.utcnow()
    with multiprocessing.Pool() as pool:
        for msg in pool.imap_unordered(draw_helper, data.todo):
            if datetime.utcnow() >= next_msg:
                next_msg += timedelta(seconds=1)
                print(msg)


def test(log):
    values_simple = log.decode_values("""
        acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf
    """)
    values = log.decode_values("""
        be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
        edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
        fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
        fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
        aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
        fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
        dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
        bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
        egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
        gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
    """)

    log.test(calc(log, values_simple, 1), 0)
    log.test(calc(log, values, 1), 26)
    log.test(calc(log, values_simple, 2), 5353)
    log.test(calc(log, values, 2), 61229)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))
