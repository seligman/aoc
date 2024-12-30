#!/usr/bin/env python3

DAY_NUM = 23
DAY_DESC = 'Day 23: LAN Party'

def other_draw(describe, values):
    if describe:
        return "Draw this"
    from dummylog import DummyLog
    calc(DummyLog(), values, 3)

def calc(log, values, mode):
    connected = set()
    computers = set()
    for row in values:
        row = row.split("-")
        connected.add((row[0], row[1]))
        connected.add((row[1], row[0]))
        computers.add(row[0])
        computers.add(row[1])
    
    computers = list(sorted(computers))

    if mode == 3:
        import networkx as nx # optional package
        import os
        graph = nx.Graph()
        for x in computers:
            graph.add_node(x)
        for x, y in connected:
            graph.add_edge(x, y)
        import matplotlib.pyplot as plt # optional package
        layout = nx.kamada_kawai_layout(graph)
        fig = plt.figure(1, figsize=(1920/100, 1080/100), dpi=100)
        nx.draw(graph, with_labels=False, node_size=500, pos=layout)
        plt.savefig(os.path.join("animations", f"image_{DAY_NUM}.png"))
        return

    if mode == 1:
        ret = 0
        for a in computers:
            for b in computers:
                if b > a and (a, b) in connected:
                    for c in computers:
                        if c > b and (a, c) in connected and (b, c) in connected:
                            if "t" in a[0] + b[0] + c[0]:
                                ret += 1
        return ret
    else:
        from collections import deque
        todo = deque([(x,) for x in computers])
        best = tuple()
        while len(todo) > 0:
            cur = todo.pop()
            if len(cur) > len(best):
                best = cur
            last = cur[-1]
            for x in computers:
                if x > last:
                    good = True
                    for y in cur:
                        if (x, y) not in connected:
                            good = False
                            break
                    if good:
                        todo.append(cur + (x,))
        return ",".join(sorted(best))
        

def test(log):
    values = log.decode_values("""
        kh-tc
        qp-kh
        de-cg
        ka-co
        yn-aq
        qp-ub
        cg-tb
        vc-aq
        tb-ka
        wh-tc
        yn-cg
        kh-ub
        ta-co
        de-co
        tc-td
        tb-wq
        wh-td
        ta-ka
        td-qp
        aq-cg
        wq-ub
        ub-vc
        de-ta
        wq-aq
        wq-vc
        wh-yn
        ka-de
        kh-ta
        co-tc
        wh-qp
        tb-vc
        td-yn
    """)

    log.test(calc(log, values, 1), '7')
    log.test(calc(log, values, 2), 'co,de,ka,ta')

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
