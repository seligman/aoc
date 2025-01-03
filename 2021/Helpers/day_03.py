#!/usr/bin/env python3

DAY_NUM = 3
DAY_DESC = 'Day 3: Binary Diagnostic'

def calc(log, values, mode):
    counts = []
    
    if mode == 1:
        for cur in values:
            if len(counts) == 0:
                counts = [0] * len(cur)
            for i, x in enumerate(cur):
                if x == '1':
                    counts[i] += 1
        
        a = ''
        b = ''
        for x in counts:
            if x > len(values) / 2:
                a += '1'
                b += '0'
            else:
                a += '0'
                b += '1'

        return int(a,2) * int(b,2)
    else:
        digits = []
        for i in range(2):
            digits.append('')
            temp = values[:]
            while len(temp) and len(temp[0]):
                bin0, bin1 = [], []
                count = 0
                for cur in temp:
                    if cur[0] == '1':
                        count += 1
                        bin1.append(cur[1:])
                    else:
                        bin0.append(cur[1:])

                if (i == 0 and count >= len(temp) / 2) or (i == 1 and count < len(temp) / 2):
                    digits[-1] += '1'
                    temp = bin1
                else:
                    digits[-1] += '0'
                    temp = bin0

                if len(temp) == 1 and len(temp[0]) > 0:
                    digits[-1] += temp[0]
                    break

        return int(digits[0], 2) * int(digits[1], 2)

def test(log):
    values = log.decode_values("""
        00100
        11110
        10110
        10111
        10101
        01111
        00111
        11100
        10000
        11001
        00010
        01010
    """)

    log.test(calc(log, values, 1), 198)
    log.test(calc(log, values, 2), 230)

def run(log, values):
    log(f"Part 1: {calc(log, values, 1)}")
    log(f"Part 2: {calc(log, values, 2)}")

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2021/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
