#!/usr/bin/env python3


DAY_NUM = 8
DAY_DESC = 'Day 8: Memory Maneuver'


class Index:
    def __init__(self):
        self.val = 0

    def get(self):
        ret = self.val
        self.val += 1
        return ret


def sum_meta(node):
    ret = 0

    for sub in node['child_nodes']:
        ret += sum_meta(sub)

    ret += sum(node['metadata_entries'])

    return ret


def value_node(node):
    ret = 0

    child = node['child_nodes']
    meta = node['metadata_entries']

    if len(child) == 0:
        ret += sum(meta)
    else:
        for i in meta:
            i -= 1
            if i < len(child):
                ret += value_node(child[i])

    return ret


def load(values, i):
    ret = {}
    child_nodes = values[i.get()]
    ret['child_nodes'] = []
    metadata_entries = values[i.get()]
    ret['metadata_entries'] = []

    for _ in range(child_nodes):
        ret['child_nodes'].append(load(values, i))

    for _ in range(metadata_entries):
        ret['metadata_entries'].append(values[i.get()])
    
    return ret


def calc(log, values):
    values = [int(x) for x in values[0].split(' ')]

    nodes = load(values, Index())
    log("The target value is %d" % (value_node(nodes),))
    return sum_meta(nodes)


def test(log):
    values = [
        "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2",
    ]

    if calc(log, values) == 138:
        return True
    else:
        return False


def run(log, values):
    log(calc(log, values))

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
