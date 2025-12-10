#!/usr/bin/env python3
"""Sum invalid product IDs where an ID is a repetition of a digit-block >=2 times.

Reads a file of comma-separated ranges (or stdin). For each inclusive range,
find all numbers that consist of some block of digits repeated r times with r>=2
and no leading zero in the block, then sum them (deduplicated) and print the total.
"""
import sys
import argparse
from math import ceil


def iter_ranges_from_line(line):
    parts = [p.strip() for p in line.strip().split(',') if p.strip()]
    for part in parts:
        if '-' not in part:
            continue
        a, b = part.split('-', 1)
        try:
            lo = int(a)
            hi = int(b)
        except Exception:
            continue
        if lo > hi:
            lo, hi = hi, lo
        yield lo, hi


def sum_invalid_in_range(lo: int, hi: int) -> int:
    found = set()
    lo_len = len(str(lo))
    hi_len = len(str(hi))

    # base length k must be at least 1, and at most hi_len//2 (since r>=2)
    max_k = hi_len // 2
    for k in range(1, max_k + 1):
        # possible repeat counts r so that total length L = k*r falls within [lo_len, hi_len]
        r_min = max(2, ceil(lo_len / k))
        r_max = hi_len // k
        if r_min > r_max:
            continue

        start = 10 ** (k - 1)
        end = 10 ** k - 1
        for r in range(r_min, r_max + 1):
            # for fixed r, values increase with base; we can break early when exceeding hi
            for base in range(start, end + 1):
                s = str(base) * r
                val = int(s)
                if val < lo:
                    continue
                if val > hi:
                    break
                found.add(val)

    return sum(found)


def solve_ranges_line(line: str) -> int:
    total = 0
    for lo, hi in iter_ranges_from_line(line):
        total += sum_invalid_in_range(lo, hi)
    return total


def main(argv=None):
    parser = argparse.ArgumentParser(description='Sum invalid repeated-block IDs (r>=2)')
    parser.add_argument('input_file', nargs='?', help='path to input file (default: stdin)')
    args = parser.parse_args(argv)

    if args.input_file:
        with open(args.input_file, 'r') as f:
            content = f.read()
    else:
        content = sys.stdin.read()

    content = content.replace('\n', ',').strip()
    if not content:
        print(0)
        return

    print(solve_ranges_line(content))


if __name__ == '__main__':
    main()
