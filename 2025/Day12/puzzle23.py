#!/usr/bin/env python3
import sys
import re


def main():
    lines = [line.rstrip("\n") for line in sys.stdin]

    shapes = []
    i = 0
    n = len(lines)

    # Parse shape definitions at the top
    while i < n:
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if re.match(r"^\d+x\d+:", line):
            break

        m = re.match(r"^(\d+):", line)
        if not m:
            raise ValueError(f"Expected shape index line at {i}, got: {line!r}")

        i += 1
        rows = []
        # Collect rows of this shape until blank / next header
        while i < n:
            l = lines[i]
            if not l.strip():
                i += 1
                break
            if re.match(r"^\d+:", l) or re.match(r"^\d+x\d+:", l.strip()):
                break
            rows.append(l)
            i += 1

        shapes.append(rows)

        while i < n and not lines[i].strip():
            i += 1

    # Compute area (number of '#') of each shape
    shape_areas = []
    for rows in shapes:
        area = 0
        for r in rows:
            area += r.count("#")
        shape_areas.append(area)

    # Parse regions and count how many pass the area check
    valid_regions = 0

    while i < n:
        line = lines[i].strip()
        i += 1
        if not line:
            continue

        m = re.match(r"^(\d+)x(\d+):\s*(.*)$", line)
        if not m:
            continue

        w = int(m.group(1))
        h = int(m.group(2))
        rest = m.group(3).strip()
        counts = [int(x) for x in rest.split()] if rest else []

        region_area = w * h
        total_present_area = sum(c * a for c, a in zip(counts, shape_areas))

        if total_present_area <= region_area:
            valid_regions += 1

    print(valid_regions)


if __name__ == "__main__":
    main()
