#!/usr/bin/env python3

DAY_NUM = 24
DAY_DESC = 'Day 24: Crossed Wires'

def calc(log, values, mode):
    bits = {}
    wires = []
    for row in values:
        if ":" in row:
            row = row.split(": ")
            bits[row[0]] = int(row[1])
        elif "->" in row:
            row = row.split(' ')
            wires.append((row[0], row[1], row[2], row[4]))

    if mode == 1:
        while len(wires) > 0:
            temp = []
            for a, op, b, dest in wires:
                if a in bits and b in bits:
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
            wires = temp

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
    log(calc(log, values, 1))
    log(calc(log, values, 2))

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
