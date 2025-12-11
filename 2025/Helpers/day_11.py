#!/usr/bin/env python3

DAY_NUM = 11
DAY_DESC = 'Day 11: Reactor'

def calc(log, values, mode):
    devices = {}
    for row in values:
        source, dest = row.split(": ")
        dest = dest.split(" ")
        devices[source] = dest

    def count_paths(src, dest):
        ret = 0
        todo = [(src, [])]
        while len(todo) > 0:
            target, count = todo.pop(0)
            if target == dest:
                ret += 1
            else:
                if target in devices:
                    for cur in devices[target]:
                        if cur not in count:
                            todo.append((cur, count + [cur]))
        return ret

    def count_paths_with_required(src, dest, required_nodes):
        from functools import lru_cache

        @lru_cache(maxsize=None)
        def count_from(current, visited_mask):
            if current == dest:
                return 1 if visited_mask == 3 else 0

            if current not in devices:
                return 0

            total = 0
            for next_node in devices[current]:
                new_mask = visited_mask
                if next_node == required_nodes[0]:
                    new_mask |= 1
                elif next_node == required_nodes[1]:
                    new_mask |= 2
                total += count_from(next_node, new_mask)

            return total

        initial_mask = 0
        if src == required_nodes[0]:
            initial_mask |= 1
        elif src == required_nodes[1]:
            initial_mask |= 2
        return count_from(src, initial_mask)

    if mode == 1:
        return count_paths("you", "out")
    else:
        return count_paths_with_required("svr", "out", ["dac", "fft"])

def test(log):
    values = log.decode_values("""
aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
    """)

    log.test(calc(log, values, 1), '5')

    values = log.decode_values("""
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
    """)

    log.test(calc(log, values, 2), '2')

def run(log, values):
    log("Part 1")
    log(calc(log, values, 1))
    log("Part 2")
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
