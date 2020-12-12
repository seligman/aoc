#!/usr/bin/env python3

def get_desc():
    return 12, 'Day 12: Rain Risk'

def calc(log, values, mode, draw=False):
    pos = complex(0, 0)
    way = complex(10, -1)
    dirs = {
        'E': [complex(1, 0), 'N', 'S'],
        'S': [complex(0, 1), 'E', 'W'],
        'W': [complex(-1, 0), 'S', 'N'],
        'N': [complex(0, -1), 'W', 'E'],
    }

    if mode == 1:
        min_pos = complex(0, 0)
        max_pos = complex(0, 0)
        for pass_no in range(2 if draw else 1):
            pos = complex(0, 0)
            if pass_no == 1:
                from PIL import Image
                print(max_pos, min_pos)
                im = Image.new('RGB',(int(max_pos.real - min_pos.real) + 10, int(max_pos.imag - min_pos.imag) + 10), color=(0,0,0))
                pixels = im.load()
                frame = 0
            dir = 'E'
            for cur in values:
                cardinal = cur[0]
                if cardinal == 'L':
                    for _ in range(0, int(cur[1:]), 90):
                        dir = dirs[dir][1]
                    cardinal = "x"
                elif cardinal == 'R':
                    for _ in range(0, int(cur[1:]), 90):
                        dir = dirs[dir][2]
                    cardinal = "x"
                elif cardinal == 'F':
                    cardinal = dir
                else:
                    cardinal = cur[0]
                if cardinal != "x":
                    last_pos = pos
                    pos += dirs[cardinal][0] * int(cur[1:])

                    if draw:
                        if pass_no == 0:
                            min_pos = complex(min(min_pos.real, pos.real), min(min_pos.imag, pos.imag))
                            max_pos = complex(max(max_pos.real, pos.real), max(max_pos.imag, pos.imag))
                        else:
                            while last_pos.real < pos.real:
                                last_pos += complex(1, 0)
                                pixels[int(last_pos.real - min_pos.real)+5, int(last_pos.imag - min_pos.imag)+5] = (192, 192, 255)
                            while last_pos.real > pos.real:
                                last_pos += complex(-1, 0)
                                pixels[int(last_pos.real - min_pos.real)+5, int(last_pos.imag - min_pos.imag)+5] = (192, 192, 255)
                            while last_pos.imag < pos.imag:
                                last_pos += complex(0, 1)
                                pixels[int(last_pos.real - min_pos.real)+5, int(last_pos.imag - min_pos.imag)+5] = (192, 192, 255)
                            while last_pos.imag > pos.imag:
                                last_pos += complex(0, -1)
                                pixels[int(last_pos.real - min_pos.real)+5, int(last_pos.imag - min_pos.imag)+5] = (192, 192, 255)
                            frame += 1
                            im.save("frame_%05d.png" % (frame,))
                            log.show(str(frame))
    else:
        for cur in values:
            if cur[0] == "F":
                pos += way * int(cur[1:])
            elif cur[0] in dirs:
                way += dirs[cur[0]][0] * int(cur[1:])
            elif cur[0] == "R":
                for _ in range(0, int(cur[1:]), 90):
                    way = complex(-int(way.imag), way.real)
            elif cur[0] == "L":
                for _ in range(0, int(cur[1:]), 90):
                    way = complex(way.imag, -int(way.real))

    return int(abs(pos.real) + abs(pos.imag))


def other_draw(describe, values):
    if describe:
        return "Animate this"
    else:
        from dummylog import DummyLog
        calc(DummyLog(), values, 1, draw=True)


def test(log):
    values = log.decode_values("""
        F10
        N3
        F7
        R90
        F11
    """)

    log.test(calc(log, values, 1), 25)
    log.test(calc(log, values, 2), 286)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))
