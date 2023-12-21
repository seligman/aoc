#!/usr/bin/env python3

DAY_NUM = 21
DAY_DESC = 'Day 21: Step Counter'

from collections import deque

def calc(log, values, mode, target_steps):
    # TODO: Maybe clean this mess up

    # from grid import Grid, Point
    # grid = Grid.from_text(values)

    # for (x, y), val in grid.grid.items():
    #     if val == "S":
    #         grid[x, y] = "."
    #         start = (x, y)

    # empty = sum(1 for val in grid.grid.values() if val == ".")

    # todo = deque([((start[0], start[1], target_steps))])
    # seen = set()
    # final = set()
    # valid = set()
    # while len(todo) > 0:
    #     x, y, left = todo.pop()
    #     if left == 0:
    #         final.add((x, y))
    #         # print(x, y)
    #     else:
    #         left -= 1
    #         for x, y in grid.get_dirs(2, (x, y), False):
    #             if grid[x % grid.width(), y % grid.height()] == ".":
    #                 # seen.add((x, y))
    #                 if (x, y, left) not in valid:
    #                     valid.add((x, y, left))
    #                     todo.append((x, y, left ))
    # return len(final)

    G = [[c for c in row] for row in values]
    R = len(G)
    C = len(G[0])

    for r in range(R):
        for c in range(C):
            if G[r][c]=='S':
                sr,sc = r,c

    def findD(r,c):
        D = {}
        Q = deque([(0,0,sr,sc,0)])
        while Q:
            tr,tc,r,c,d = Q.popleft()
            if r<0:
                tr -= 1
                r += R
            if r>=R:
                tr += 1
                r -= R
            if c<0:
                tc -= 1
                c += C
            if c>=C:
                tc += 1
                c -= C
            if not (0<=r<R and 0<=c<C and G[r][c]!='#'):
                continue
            if (tr,tc,r,c) in D:
                continue
            if abs(tr)>4 or abs(tc)>4:
                continue
            D[(tr,tc,r,c)] = d
            for dr,dc in [[-1,0],[0,1],[1,0],[0,-1]]:
                Q.append((tr,tc,r+dr, c+dc, d+1))
        return D

    D = findD(sr,sc)

    SOLVE = {}
    def solve(d,v,L):
        amt = (L-d)//R
        if (d,v,L) in SOLVE:
            return SOLVE[(d,v,L)]
        ret = 0
        for x in range(1,amt+1):
            if d+R*x<=L and (d+R*x)%2==(L%2):
                ret += ((x+1) if v==2 else 1)
        SOLVE[(d,v,L)] = ret
        return ret

    ans = 0
    for r in range(R):
        for c in range(C):
            if (0,0,r,c) in D:
                for tr in [-3,-2,-1,0,1,2,3]:
                    for tc in [-3,-2,-1,0,1,2,3]:
                        if mode == 1 and (tr!=0 or tc!=0):
                            continue
                        d = D[(tr,tc,r,c)]
                        if d%2==target_steps%2 and d<=target_steps:
                            ans += 1
                        if tr in [-3,3] and tc in [-3,3]:
                            ans += solve(d,2,target_steps)
                        elif tr in [-3,3] or tc in [-3,3]:
                            ans += solve(d,1,target_steps)
    return ans


    # TODO
    return 0

def test(log):
    values = log.decode_values("""
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
    """)

    # log.test(calc(log, values, 1, 6), '16')
    # log.test(calc(log, values, 2, 100), '6536')

def run(log, values):
    log(calc(log, values, 1, 64))
    log(calc(log, values, 2, 26501365))

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
