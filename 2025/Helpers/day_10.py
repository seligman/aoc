#!/usr/bin/env python3

DAY_NUM = 10
DAY_DESC = 'Day 10: Factory'

import itertools
from multiprocessing import Pool

def solve_part2(buttons, joltages):
    n = len(buttons)
    m = len(joltages)

    matrix = []
    for j in range(m):
        row = [1 if j in buttons[i] else 0 for i in range(n)]
        row.append(joltages[j])
        matrix.append(row)

    pivot_cols = []
    current_row = 0

    for col in range(n):
        pivot_row = None
        for row in range(current_row, m):
            if matrix[row][col] != 0:
                pivot_row = row
                break

        if pivot_row is None:
            continue

        matrix[current_row], matrix[pivot_row] = matrix[pivot_row], matrix[current_row]
        pivot_cols.append(col)

        for row in range(current_row + 1, m):
            if matrix[row][col] != 0:
                factor = matrix[row][col]
                pivot = matrix[current_row][col]
                for j in range(n + 1):
                    matrix[row][j] = matrix[row][j] * pivot - matrix[current_row][j] * factor

        current_row += 1

    pivot_set = set(pivot_cols)
    free_vars = [i for i in range(n) if i not in pivot_set]

    best_solution = None
    best_sum = float('inf')

    def try_solution(free_values):
        nonlocal best_solution, best_sum

        solution = [0] * n
        for i, var in enumerate(free_vars):
            solution[var] = free_values[i]

        for row_idx in range(len(pivot_cols) - 1, -1, -1):
            col = pivot_cols[row_idx]
            val = matrix[row_idx][n]

            for j in range(col + 1, n):
                val -= matrix[row_idx][j] * solution[j]

            if matrix[row_idx][col] == 0:
                continue

            if val % matrix[row_idx][col] != 0:
                return
            
            solution[col] = val // matrix[row_idx][col]

            if solution[col] < 0:
                return
            
        for j in range(m):
            total = sum(solution[i] for i in range(n) if j in buttons[i])
            if total != joltages[j]:
                return

        total_sum = sum(solution)
        if total_sum < best_sum:
            best_sum = total_sum
            best_solution = solution[:]

    if len(free_vars) == 0:
        try_solution([])
    elif len(free_vars) == 1:
        max_val = max(joltages) * 3
        for val in range(max_val + 1):
            try_solution([val])
            if best_solution and val > best_sum:
                break
    elif len(free_vars) == 2:
        max_val = max(max(joltages), 200)
        for combo in itertools.product(range(max_val + 1), repeat=2):
            if best_solution and sum(combo) > best_sum:
                continue
            try_solution(list(combo))
    elif len(free_vars) == 3:
        for combo in itertools.product(range(250), repeat=3):
            if best_solution and sum(combo) > best_sum:
                continue
            try_solution(list(combo))
    elif len(free_vars) == 4:
        for combo in itertools.product(range(30), repeat=4):
            if best_solution and sum(combo) > best_sum:
                continue
            try_solution(list(combo))
    else:
        try_solution([0] * len(free_vars))
        for combo in itertools.product(range(15), repeat=min(len(free_vars), 5)):
            padded = list(combo) + [0] * (len(free_vars) - len(combo))
            if best_solution and sum(padded) > best_sum:
                continue
            try_solution(padded)

    return best_solution

def calc(log, values, mode):
    buttons = []
    for row in values:
        row = row.split(' ')
        cur = {
            "target": row[0][1:-1],
            "joltage": list(int(x) for x in row[-1][1:-1].split(",")),
            "buttons": [],
        }
        for button in row[1:-1]:
            cur['buttons'].append([int(x) for x in button[1:-1].split(",")])
        buttons.append(cur)

    ret = 0
    if mode == 1:
        for cur in buttons:
            todo = []
            seen = set()
            for button in cur['buttons']:
                todo.append({"press": button, "state": [False] * len(cur['target']), "score": 1})
            while len(todo) > 0:
                temp = todo.pop(0)
                for x in temp['press']:
                    temp['state'][x] = not temp['state'][x]
                new_state = "".join("#" if x else "." for x in temp['state'])
                if new_state == cur['target']:
                    ret += temp['score']
                    todo = []
                else:
                    if new_state not in seen:
                        seen.add(new_state)
                        for button in cur['buttons']:
                            todo.append({"press": button, "state": temp['state'][:], "score": temp['score'] + 1})
    else:
        with Pool() as pool:
            for solved in pool.imap_unordered(helper, buttons):
                ret += sum(solved)
        # for cur in buttons:
        #     ret += sum(solve_part2(cur['buttons'], cur['joltage']))

    return ret

def helper(cur):
    return solve_part2(cur['buttons'], cur['joltage'])

def test(log):
    values = log.decode_values("""
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
    """)

    log.test(calc(log, values, 1), '7')
    log.test(calc(log, values, 2), '33')

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
