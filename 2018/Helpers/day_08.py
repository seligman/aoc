#!/usr/bin/env python3


def get_desc():
    return 8, 'Day 8: Memory Maneuver'


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
    log.show("The target value is %d" % (value_node(nodes),))
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
    log.show(calc(log, values))
