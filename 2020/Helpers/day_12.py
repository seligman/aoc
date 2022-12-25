#!/usr/bin/env python3

DAY_NUM = 12
DAY_DESC = 'Day 12: Rain Risk'

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
                if draw:
                    from PIL import Image
                    im = Image.new('RGB',(int(max_pos.real - min_pos.real) + 10, int(max_pos.imag - min_pos.imag) + 10), color=(0,0,0))
                    pixels = im.load()
                    frame = 0
                    fade = []
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
                            def make_line(a, b):
                                while a.real != b.real:
                                    a = complex((b.real - a.real) / abs(b.real - a.real) + a.real, a.imag)
                                    yield a
                                while a.imag != b.imag:
                                    a = complex(a.real, (b.imag - a.imag) / abs(b.imag - a.imag) + a.imag)
                                    yield a
                            fade.append(set())
                            for x in make_line(last_pos, pos):
                                x = x - min_pos + complex(5,5)
                                for xo in range(-2, 3):
                                    for yo in range(-2, 3):
                                        fade[-1].add((int(x.real)+xo, int(x.imag)+yo))

                            while len(fade) > 8:
                                fade.pop(0)
                            
                            blue = 255
                            for cur in fade[::-1]:
                                for x in cur:
                                    pixels[x[0], x[1]] = (127, 127, blue)
                                blue -= 16

                            frame += 1
                            fn = "frame_%05d.png" % (frame,)
                            im.save(fn)
                            if frame % 10 == 0:
                                log("Saving " + fn)

        if draw:
            import os
            cmd = [
                "ffmpeg", "-y",
                "-hide_banner",
                "-f", "image2",
                "-framerate", "30", 
                "-i", "frame_%05d.png", 
                "-c:v", "libx264", 
                "-profile:v", "main", 
                "-pix_fmt", "yuv420p", 
                "-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2",
                "-an", 
                "-movflags", "+faststart",
                os.path.join("animations", "animation_%02d.mp4" % (get_desc()[0],)),
            ]
            log("$ " + " ".join(cmd))
            import subprocess
            subprocess.check_call(cmd)

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

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in [[], ["Puzzles"], ["..", "Puzzles"]]:
                cur = os.path.join(*(dn + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
