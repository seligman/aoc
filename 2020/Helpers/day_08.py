#!/usr/bin/env python3

DAY_NUM = 8
DAY_DESC = 'Day 8: Handheld Halting'

def calc(log, values, mode, debug=False, draw=False):
    from program import Program
    if mode == 1:
        prog = Program(values, log if debug else None)
        while not prog.seen_pc():
            prog.step()
        return prog.acc
    else:
        prog = Program(values)
        swap = {"jmp": "nop", "nop": "jmp"}
        to_test = []
        for i in range(len(values)):
            if prog.instructions[i].op in swap:
                to_test.append(i)
        
        for i in to_test:
            prog = Program(values)
            prog.instructions[i].op = swap[prog.instructions[i].op]
            backup = prog.clone()
            hit_end = True
            while prog.step():
                if prog.seen_pc():
                    hit_end = False
                    break
            if hit_end:
                if draw:
                    while True:
                        print(f"Drawing frame {backup.steps} of {prog.steps}")
                        backup.show()
                        if not backup.step():
                            break
                return prog.acc

    return 0

def other_draw(describe, values):
    if describe:
        return "Animate this"
    
    from dummylog import DummyLog
    calc(DummyLog(), values, 2, draw=True)

    import subprocess
    import os
    cmd = [
        "ffmpeg", "-y",
        "-hide_banner",
        "-f", "image2",
        "-framerate", "10", 
        "-i", "frame_%05d.png", 
        "-c:v", "libx264", 
        "-profile:v", "main", 
        "-pix_fmt", "yuv420p", 
        "-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2",
        "-an", 
        "-movflags", "+faststart",
        os.path.join("animations", "animation_%02d.mp4" % (get_desc()[0],)),
    ]
    print("$ " + " ".join(cmd))
    subprocess.check_call(cmd)


def test(log):
    values = log.decode_values("""
        nop +0
        acc +1
        jmp +4
        acc +3
        jmp -3
        acc -99
        acc +1
        jmp -4
        acc +6
    """)

    log.test(calc(log, values, 1, True), 5)
    log.test(calc(log, values, 2), 8)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))
