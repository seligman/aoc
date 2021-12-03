#!/usr/bin/env python3

def get_desc():
    return 3, 'Day 3: Binary Diagnostic'

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
        a = ''
        old_values = values[:]
        while True:
            bin0, bin1 = [], []
            count = 0
            for cur in values:
                if cur[0] == '1':
                    count += 1
                    bin1.append(cur[1:])
                else:
                    bin0.append(cur[1:])
            if count >= len(values) / 2:
                a += '1'
                values = bin1
            else:
                a += '0'
                values = bin0
            if len(values) == 1 and len(values[0]) > 0:
                a += values[0]
                break
            if len(values[0]) == 0:
                break

        values = old_values
        b = ''
        while True:
            bin0, bin1 = [], []
            count = 0
            for cur in values:
                if cur[0] == '1':
                    bin1.append(cur[1:])
                else:
                    count += 1
                    bin0.append(cur[1:])

            if count <= len(values) / 2:
                b += '0'
                values = bin0
            else:
                b += '1'
                values = bin1

            if len(values) == 1 and len(values[0]) > 0:
                b += values[0]
                break
            if len(values[0]) == 0:
                break
        return int(a, 2) * int(b, 2)

    return 0

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
    log.test(calc(log, values, 2), 'TODO')

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))
