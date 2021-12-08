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


def other_draw(describe, values):
    if describe:
        return "Animate digits"
    import animate
    animate.prep()
    create_frames(values[0])
    animate.create_mp4(get_desc(), rate=30)


def create_frames(script):
    from PIL import Image, ImageDraw, ImageFont
    import os
    import math

    class Data:
        unique = ""
        output = ""
        frame = 0
        valid = ""
        animate = ""
        replace = {}
        notes = {}
        known = {}

    data = Data()
    data.unique, data.output = script.split(" | ")
    data.unique = data.unique.split()
    data.output = data.output.split()
    data.frame = 0
    data.valid = ""
    data.animate = ""
    data.replace = {}
    data.notes = {}
    data.known = {}

    def rotate(origin, point, angle):
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
        value = max(0, min(1, value))
        if value < 0.5:
            return 4 * (value ** 3)
        else:
            return 1 - math.pow(-2 * value + 2, 3) / 2

    def draw_segment(dr, pt, on, step):
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
        digits = {
            'a': 0,
            'b': 1,
            'c': 2,
            'd': 3,
            'e': 4,
            'f': 5,
            'g': 6,
        }
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

    source_code = os.path.join('Helpers', 'Font-SourceCodePro-Bold.ttf')
    fnt = ImageFont.truetype(source_code, 30)

    def draw_all(step, pos=None, text=None):
        off = 0
        im = Image.new('RGB', (3350, 500))
        dr = ImageDraw.Draw(im)
        dr.rectangle((2400, 0, im.width, im.height), (50, 50, 80))
        for i, cur in enumerate(data.unique + data.output):
            draw_segment(dr, (off + 100, 130), cur, step)
            note = data.notes.get(i)
            if pos is not None:
                if pos == i:
                    note = text
            if note is not None:
                dr.text((off, 385), note, font=fnt)
            off += 240
        im.thumbnail((im.width // 2, im.height // 2))
        im.save(f"frame_{data.frame:05d}.png")
        if data.frame % 10 == 0:
            print(f"Saving frame {data.frame}")
        data.frame += 1

    draw_all(0)

    def freeze():
        data.animate = ""
        for _ in range(15):
            draw_all(0)

    for pos, cur in enumerate(data.unique):
        if cur not in data.known.values():
            if len(cur) == 2:
                data.animate = cur
                data.known[1] = cur
                break
    data.replace[data.animate[0]] = "c"
    data.replace[data.animate[1]] = "f"
    for i in range(31):
        draw_all(i / 30, pos, "Must be '1'")
    data.notes[pos] = "Locked\n1"
    data.valid += data.animate
    freeze()

    for pos, cur in enumerate(data.unique):
        if cur not in data.known.values():
            if len(cur) == 3:
                data.animate = "".join(x for x in cur if x not in data.valid)
                data.known[7] = cur
                break
    data.replace[data.animate[0]] = "a"
    for i in range(31):
        draw_all(i / 30, pos, "Must be '7'")
    data.notes[pos] = "Locked\n7"
    data.valid += data.animate
    freeze()

    for pos, cur in enumerate(data.unique):
        if cur not in data.known.values():
            if len(cur) == 4:
                data.animate = "".join(x for x in cur if x not in data.valid)
                data.known[4] = cur
                break
    data.replace[data.animate[0]] = "b"
    data.replace[data.animate[1]] = "d"
    for i in range(31):
        draw_all(i / 30, pos, "Must be '4'")
    data.notes[pos] = "Locked\n4"
    data.valid += data.animate
    freeze()

    for pos, cur in enumerate(data.unique):
        if cur not in data.known.values():
            if len(cur) == 7:
                data.animate = "".join(x for x in cur if x not in data.valid)
                data.known[8] = cur
                break
    data.replace[data.animate[0]] = "e"
    data.replace[data.animate[1]] = "g"
    for i in range(31):
        draw_all(i / 30, pos, "Must be '8'")
    data.notes[pos] = "Locked\n8"
    data.valid += data.animate
    freeze()

    for pos, cur in enumerate(data.unique):
        if cur not in data.known.values():
            if len(set(cur) - (set(data.known[7]) | set(data.known[4]))) == 1:
                data.known[9] = cur
                data.animate = ""
                break

    def check_swap(a, b, dig):
        if a in [data.replace[x] for x in data.known[dig]]:
            swap = a + b
            reverse = {y:x for x,y in data.replace.items()}
            data.animate = "".join(reverse[x] for x in swap)
            data.valid = "".join([x for x in data.valid if x not in data.animate])
            for i in range(31):
                draw_all((30 - i) / 30, pos, f"Must be '{dig}'")
            data.replace[data.animate[0]], data.replace[data.animate[1]] = data.replace[data.animate[1]], data.replace[data.animate[0]]
            for i in range(31):
                draw_all(i / 30, pos, f"Must be '{dig}'")
            data.valid += data.animate
        else:
            for i in range(31):
                draw_all(i / 30, pos, f"Must be '{dig}'")
        data.notes[pos] = f"Locked\n{dig}"
        freeze()
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
    for i in range(31):
        draw_all(i / 30, pos, "Must be '3'")
    data.notes[pos] = "Locked\n3"
    freeze()

    for pos, cur in enumerate(data.unique):
        if cur not in data.known.values():
            if len(set(data.known[9]) - set(cur)) == 1:
                data.known[5] = cur
                data.animate = ""
                break
    for i in range(31):
        draw_all(i / 30, pos, "Must be '5'")
    data.notes[pos] = "Locked\n5"
    freeze()

    for pos, cur in enumerate(data.unique):
        if cur not in data.known.values():
            data.known[2] = cur
            data.animate = ""
            break
    for i in range(31):
        draw_all(i / 30, pos, "Must be '2'")
    data.notes[pos] = "Locked\n2"
    freeze()

    for pos, cur in enumerate(data.unique + data.output):
        if pos >= len(data.unique):
            for key, value in data.known.items():
                if "".join(sorted(cur)) == "".join(sorted(value)):
                    data.notes[pos] = f"  {key}"
            freeze()


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
