#!/usr/bin/env python3

DAY_NUM = 24
DAY_DESC = 'Day 24: Crossed Wires'

def other_draw(describe, values):
    import os
    if describe:
        return "Draw this, original input"
    from dummylog import DummyLog
    swaps = calc(DummyLog(), values, 2, return_swaps=True)
    calc(DummyLog(), values, 1, draw=True, fn=os.path.join("animations", f"image_{DAY_NUM}_p1.png"))

def other_draw2(describe, values):
    import os
    if describe:
        return "Draw this, original input"
    from dummylog import DummyLog
    swaps = calc(DummyLog(), values, 2, return_swaps=True)
    calc(DummyLog(), values, 1, draw=True, perform_swaps=swaps, fn=os.path.join("animations", f"image_{DAY_NUM}_p2.png"))

def calc(log, values, mode, draw=False, return_swaps=False, perform_swaps=None, fn=None):
    bits = {}
    wires = []
    for row in values:
        if ":" in row:
            row = row.split(": ")
            bits[row[0]] = int(row[1])
        elif "->" in row:
            row = row.split(' ')
            if perform_swaps is not None:
                for i in range(0, len(perform_swaps), 2):
                    a, b = perform_swaps[i:i+2]
                    if row[-1] == a:
                        row[-1] = b
                    elif row[-1] == b:
                        row[-1] = a
            wires.append((row[0], row[1], row[2], row[4]))

    if mode == 1:
        if draw:
            from collections import defaultdict
            pass_number = 0
            locs = defaultdict(dict)
        ll = set()
        while len(wires) > 0:
            temp = []
            good_bits = set(bits)
            ll = good_bits
            for a, op, b, dest in wires:
                if a in good_bits and b in good_bits:
                    if draw:
                        locs[a]["name"] = a
                        if "pass" not in locs[a]:
                            locs[a]["pass"] = pass_number
                        locs[b]["name"] = b
                        if "pass" not in locs[b]:
                            locs[b]["pass"] = pass_number
                        locs[dest]["op"] = op
                        locs[dest]["name"] = dest
                        locs[dest]["source"] = (a, b)
                        # locs[dest]["pass"] = pass_number + 1
                    if op == "XOR":
                        bits[dest] = bits[a] ^ bits[b]
                    elif op == "OR":
                        bits[dest] = bits[a] | bits[b]
                    elif op == "AND":
                        bits[dest] = bits[a] & bits[b]
                    else:
                        raise Exception()
                else:
                    temp.append((a, op, b, dest))
            if draw:
                pass_number += 1
            wires = temp

        if draw:
            for cur in locs.values():
                if "pass" not in cur:
                    cur["pass"] = pass_number

            for x in range(pass_number + 1):
                temp = [cur for cur in locs.values() if cur["pass"] == x]
                x *= 2
                temp.sort(key=lambda cur: cur["name"])
                y = 0
                for cur in temp:
                    cur["x"] = x
                    if "source" in cur:
                        cur["y"] = sum(locs[sub]["y"] for sub in cur["source"]) / len(cur["source"])
                    else:
                        cur["y"] = y
                    y += 2

            width = int(max(x["x"] for x in locs.values()) + 1.5)
            height = int(max(x["y"] for x in locs.values()) + 1.5)
            scale = 4
            size = 10 * scale
            from PIL import Image, ImageDraw
            im = Image.new('RGB', (width * size, height * size), (0, 0, 0))
            dr = ImageDraw.Draw(im)

            for cur in locs.values():
                if "source" in cur:
                    for source in cur["source"]:
                        src = locs[source]
                        dr.line(((src["x"] * size) + (size // 2), (src["y"] * size) + (size // 2), (cur["x"] * size) + (size // 2), (cur["y"] * size) + (size // 2)), (255, 255, 255), width=scale)
            for cur in locs.values():
                if "op" not in cur:
                    dr.circle(((cur["x"] * size) + (size // 2), (cur["y"] * size) + (size // 2)), size // 2, (255, 255, 255))
                elif cur["op"] == "AND":
                    dr.circle(((cur["x"] * size) + (size // 2), (cur["y"] * size) + (size // 2)), size // 2, (128, 128, 255))
                elif cur["op"] == "XOR":
                    dr.circle(((cur["x"] * size) + (size // 2), (cur["y"] * size) + (size // 2)), size // 2, (128, 255, 128))
                elif cur["op"] == "OR":
                    dr.circle(((cur["x"] * size) + (size // 2), (cur["y"] * size) + (size // 2)), size // 2, (128, 128, 128))
                else:
                    raise Exception(cur["op"])

            im.thumbnail((im.width / scale, im.height // scale), Image.Resampling.LANCZOS)
            im.save(fn)
            exit(0)

        shift = 0
        ret = 0
        for key in sorted(bits):
            if key.startswith("z"):
                ret |= bits[key] << shift
                shift += 1
        return ret
    else:
        swapped = []
        carry = None
        def returns(ta, tb, top):
            for a, op, b, dest in wires:
                if ((a, b) == (ta, tb) or (a, b) == (tb, ta)) and op == top:
                    return dest
            return None

        count_z = sum(1 for a, op, b, dest in wires if dest.startswith("z"))
        for i in range(count_z-1):
            sum_1 = returns(f"x{i:02d}", f"y{i:02d}", 'XOR')
            carry_1 = returns(f"x{i:02d}", f"y{i:02d}", 'AND')

            if carry is not None:
                carry_2 = returns(carry, sum_1, 'AND')
                if carry_2 is None:
                    carry_1, sum_1 = sum_1, carry_1
                    swapped.extend([sum_1, carry_1])
                    carry_2 = returns(carry, sum_1, 'AND')

                sum_2 = returns(carry, sum_1, 'XOR')
                if sum_1 is not None and sum_1.startswith("z"):
                    sum_1, sum_2 = sum_2, sum_1
                    swapped.extend([sum_1, sum_2])

                if carry_1 is not None and carry_1.startswith("z"):
                    carry_1, sum_2 = sum_2, carry_1
                    swapped.extend([carry_1, sum_2])

                if carry_2 is not None and carry_2.startswith("z"):
                    carry_2, sum_2 = sum_2, carry_2
                    swapped.extend([carry_2, sum_2])

                new_carry = returns(carry_2, carry_1, 'OR')
            else:
                new_carry = None

            if new_carry is not None and new_carry.startswith("z") and new_carry != f"z{count_z-1:02d}":
                new_carry, sum_2 = sum_2, new_carry
                swapped.extend([new_carry, sum_2])

            if carry is not None:
                carry = new_carry
            else:
                carry = carry_1

        if return_swaps:
            return swapped

        return ",".join(sorted(swapped))

def test(log):
    values = log.decode_values("""
        x00: 1
        x01: 0
        x02: 1
        x03: 1
        x04: 0
        y00: 1
        y01: 1
        y02: 1
        y03: 1
        y04: 1

        ntg XOR fgs -> mjb
        y02 OR x01 -> tnw
        kwq OR kpj -> z05
        x00 OR x03 -> fst
        tgd XOR rvg -> z01
        vdt OR tnw -> bfw
        bfw AND frj -> z10
        ffh OR nrd -> bqk
        y00 AND y03 -> djm
        y03 OR y00 -> psh
        bqk OR frj -> z08
        tnw OR fst -> frj
        gnj AND tgd -> z11
        bfw XOR mjb -> z00
        x03 OR x00 -> vdt
        gnj AND wpb -> z02
        x04 AND y00 -> kjc
        djm OR pbm -> qhw
        nrd AND vdt -> hwm
        kjc AND fst -> rvg
        y04 OR y02 -> fgs
        y01 AND x02 -> pbm
        ntg OR kjc -> kwq
        psh XOR fgs -> tgd
        qhw XOR tgd -> z09
        pbm OR djm -> kpj
        x03 XOR y03 -> ffh
        x00 XOR y04 -> ntg
        bfw OR bqk -> z06
        nrd XOR fgs -> wpb
        frj XOR qhw -> z04
        bqk OR frj -> z07
        y03 OR x01 -> nrd
        hwm AND bqk -> z03
        tgd XOR rvg -> z12
        tnw OR pbm -> gnj
    """)

    log.test(calc(log, values, 1), '2024')

def run(log, values):
    log(f"Part 1: {calc(log, values, 1)}")
    log(f"Part 2: {calc(log, values, 2)}")

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2024/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
