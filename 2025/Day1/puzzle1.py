#!/usr/bin/env python3
"""Part 2: count every time needle lands on 0."""

import sys


def count_zeros(lines):
    pos = 50
    zeros = 0
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        dirc = line[0].upper()
        try:
            dist = int(line[1:])
        except Exception:
            continue
        if dirc == 'L':
            pos = (pos - dist) % 100
        else:
            pos = (pos + dist) % 100
        if pos == 0:
            zeros += 1
    return zeros


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    if len(argv) >= 1:
        path = argv[0]
        with open(path, 'r') as f:
            lines = f.readlines()
    else:
        lines = sys.stdin.readlines()
    result = count_zeros(lines)
    print(result)


if __name__ == '__main__':
    main()
