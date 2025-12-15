#!/usr/bin/env python3

import sys
from typing import List, Tuple


def parse_line(line: str) -> Tuple[int, List[List[int]], List[int]]:
    # returns m (lights), A (m x n list), b (m)
    line = line.strip()
    if not line:
        return 0, [], []
    # find diagram in [..]
    try:
        i0 = line.index('[')
        i1 = line.index(']', i0)
    except ValueError:
        raise ValueError('no diagram')
    diagram = line[i0+1:i1]
    m = len(diagram)
    b = [1 if ch == '#' else 0 for ch in diagram]
    # parse button tuples (...) after diagram
    rest = line[i1+1:]
    buttons = []
    idx = 0
    while True:
        try:
            p0 = rest.index('(', idx)
            p1 = rest.index(')', p0)
        except ValueError:
            break
        inside = rest[p0+1:p1].strip()
        if inside == '':
            btn = []
        else:
            parts = [s.strip() for s in inside.split(',') if s.strip()!='']
            btn = [int(x) for x in parts]
        buttons.append(btn)
        idx = p1 + 1
    n = len(buttons)
    # build A as m x n matrix (list of int bitmasks for columns)
    A = [[0]*n for _ in range(m)]
    for j, btn in enumerate(buttons):
        for lit in btn:
            if 0 <= lit < m:
                A[lit][j] = 1
    return m, A, b


def gaussian_elim_bits(A: List[List[int]], b: List[int]) -> Tuple[bool, List[int], List[List[int]]]:
    # Solve A x = b over GF(2). A is m x n (list of rows as lists).
    m = len(A)
    n = len(A[0]) if m>0 else 0
    # Convert rows to bitmasks for columns
    rows = []
    rhs = []
    for i in range(m):
        mask = 0
        for j in range(n):
            if A[i][j]:
                mask |= (1 << j)
        rows.append(mask)
        rhs.append(b[i] & 1)

    row = 0
    where = [-1]*n
    for col in range(n):
        # find pivot row with bit in col
        sel = -1
        for r in range(row, m):
            if (rows[r] >> col) & 1:
                sel = r; break
        if sel == -1:
            continue
        # swap
        rows[row], rows[sel] = rows[sel], rows[row]
        rhs[row], rhs[sel] = rhs[sel], rhs[row]
        where[col] = row
        # eliminate
        for r in range(m):
            if r != row and ((rows[r] >> col) & 1):
                rows[r] ^= rows[row]
                rhs[r] ^= rhs[row]
        row += 1
    # check consistency
    for r in range(row, m):
        if rows[r] == 0 and rhs[r]:
            return False, [], []
    # build particular solution with zeros
    x_part = [0]*n
    for j in range(n):
        if where[j] != -1:
            x_part[j] = rhs[where[j]]
    # build nullspace basis vectors for free variables
    basis = []
    for j in range(n):
        if where[j] == -1:
            vec = [0]*n
            vec[j] = 1
            # set dependent vars
            for k in range(n):
                if where[k] != -1:
                    r = where[k]
                    # if pivot row has bit at free col j then this dependent var toggles
                    if ((rows[r] >> j) & 1):
                        vec[k] = 1
            basis.append(vec)
    return True, x_part, basis


def min_weight_solution(x_part: List[int], basis: List[List[int]]) -> int:
    # enumerate basis combinations
    f = len(basis)
    n = len(x_part)
    # represent x_part and bases as bitmasks
    part_mask = 0
    for i, v in enumerate(x_part):
        if v & 1:
            part_mask |= (1 << i)
    base_masks = []
    for vec in basis:
        mask = 0
        for i, v in enumerate(vec):
            if v & 1:
                mask |= (1 << i)
        base_masks.append(mask)
    best = None
    # if f small, brute force
    if f <= 22:
        for s in range(1<<f):
            mask = part_mask
            # xor selected bases
            for i in range(f):
                if (s>>i)&1:
                    mask ^= base_masks[i]
            w = mask.bit_count()
            if best is None or w < best:
                best = w
        return best if best is not None else 0
    # otherwise use greedy heuristic: try random sampling and also consider linear programming-like approach
    # fallback: try meet-in-middle
    half = f//2
    left = {}
    for s in range(1<<half):
        mask = 0
        cnt = 0
        for i in range(half):
            if (s>>i)&1:
                mask ^= base_masks[i]
                cnt += 1
        # store minimal bitcount for this mask
        if mask in left:
            if cnt < left[mask]: left[mask] = cnt
        else:
            left[mask] = cnt
    right = {}
    for s in range(1<<(f-half)):
        mask = 0
        cnt = 0
        for i in range(f-half):
            if (s>>i)&1:
                mask ^= base_masks[half+i]
                cnt += 1
        if mask in right:
            if cnt < right[mask]: right[mask] = cnt
        else:
            right[mask] = cnt
    # try combine: want mask ^ part_mask has minimal bitcount
    best = None
    # precompute right list
    right_items = list(right.items())
    for lmask, lcnt in left.items():
        for rmask, rcnt in right_items:
            mask = part_mask ^ lmask ^ rmask
            w = mask.bit_count()
            total_presses = w + lcnt + rcnt
            if best is None or total_presses < best:
                best = total_presses
    return best if best is not None else 0


def solve_file(path: str) -> int:
    total = 0
    with open(path, 'r') as f:
        for line in f:
            if not line.strip():
                continue
            m, A, b = parse_line(line)
            if m == 0:
                continue
            ok, x_part, basis = gaussian_elim_bits(A, b)
            if not ok:
                # unsolvable -> ignore or treat as impossible (skip)
                continue
            presses = min_weight_solution(x_part, basis)
            total += presses
    return total


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else '/home/vikasv/projects/AOC/2025/Day10/input.txt'
    print(solve_file(path))


if __name__ == '__main__':
    main()
