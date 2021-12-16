#!/usr/bin/env python3

import math

def get_desc():
    return 16, 'Day 16: Packet Decoder'

def get_bits(temp, len):
    ret = ''
    while len > 0:
        len -= 1
        ret += temp.pop(0)
    return ret

def decode(temp, results):
    ver = int(get_bits(temp, 3), 2)
    results["version_sum"] += ver
    pid = int(get_bits(temp, 3), 2)

    if pid == 4:
        val = ""
        while True:
            x = get_bits(temp, 5)
            val += x[1:]
            if x[0] == '0':
                break
        return int(val, 2)
    else:
        length = get_bits(temp, 1)
        stack = []
        if length == '0':
            sub_len = int(get_bits(temp, 15), 2)
            sub_temp = list(get_bits(temp, sub_len))
            while len(sub_temp) > 0:
                stack.append(decode(sub_temp, results))
        else:
            sub_count = int(get_bits(temp, 11), 2)
            for _ in range(sub_count):
                stack.append(decode(temp, results))
        if pid == 0:
            return sum(stack)
        elif pid == 1:
            return math.prod(stack)
        elif pid == 2:
            return min(stack)
        elif pid == 3:
            return max(stack)
        elif pid == 5:
            return 1 if stack[0] > stack[1] else 0
        elif pid == 6: 
            return 1 if stack[0] < stack[1] else 0
        elif pid == 7:
            return 1 if stack[0] == stack[1] else 0


def calc(log, values, mode):
    temp = bin(int(values[0], 16))[2:]
    temp = list(("0" * (len(values[0]) * 4) + temp)[-len(values[0]) * 4:])
    results = {
        "mode": mode,
        "version_sum": 0,
    }
    temp = decode(temp, results)
    if mode == 1:
        return results["version_sum"]
    else:
        return temp

def test(log):
    log.test(calc(log, ["620080001611562C8802118E34"], 1), 12)
    log.test(calc(log, ["C200B40A82"], 2), 3)
    log.test(calc(log, ["04005AC33890"], 2), 54)
    log.test(calc(log, ["880086C3E88112"], 2), 7)
    log.test(calc(log, ["CE00C43D881120"], 2), 9)
    log.test(calc(log, ["D8005AC2A8F0"], 2), 1)
    log.test(calc(log, ["F600BC2D8F"], 2), 0)
    log.test(calc(log, ["9C005AC2F8F0"], 2), 0)
    log.test(calc(log, ["9C0141080250320F1802104A08"], 2), 1)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))
