#!/usr/bin/env python3
import sys
import re
import pulp


def parse_input(lines):
    """
    Parse input in the format:

    0:
    ### 
    ..#
    ###

    1:
    ...

    41x38: 26 26 29 23 21 30
    40x38: 17 28 31 34 26 19
    ...

    Returns:
        shapes: list of list-of-rows (strings with '#' and '.')
        regions: list of (width, height, [counts...])
    """
    shapes = []
    regions = []

    i = 0
    n = len(lines)

    # Parse shapes until first WxH region line
    while i < n:
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if re.match(r'^\d+x\d+:', line):
            break

        m = re.match(r'^(\d+):', line)
        if not m:
            raise ValueError(f"Expected shape index line at {i}, got: {line!r}")
        idx = int(m.group(1))

        i += 1
        rows = []
        # Read rows until blank or next shape/region header
        while i < n:
            l = lines[i]
            if not l.strip():
                i += 1
                break
            if re.match(r'^\d+:', l) or re.match(r'^\d+x\d+:', l.strip()):
                break
            rows.append(l.rstrip("\n"))
            i += 1

        shapes.append(rows)

        # Skip extra blank lines if any
        while i < n and not lines[i].strip():
            i += 1

    # Parse regions
    while i < n:
        line = lines[i].strip()
        i += 1
        if not line:
            continue
        m = re.match(r'^(\d+)x(\d+):\s*(.*)$', line)
        if not m:
            raise ValueError(f"Bad region line at {i-1}: {line!r}")
        w = int(m.group(1))
        h = int(m.group(2))
        rest = m.group(3).strip()
        counts = [int(x) for x in rest.split()] if rest else []
        regions.append((w, h, counts))

    return shapes, regions


def shape_cells_from_rows(rows):
    """
    Convert a shape given as rows of '#' and '.' into a list of (x, y) cells where '#'.
    """
    cells = []
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch == '#':
                cells.append((x, y))
    if not cells:
        raise ValueError("Shape has no '#' cells")
    return cells


def normalize_cells(cells):
    """
    Translate cells so that minimum x and y are 0; return sorted tuple of (x, y).
    """
    xs = [x for x, y in cells]
    ys = [y for x, y in cells]
    minx = min(xs)
    miny = min(ys)
    norm = sorted((x - minx, y - miny) for x, y in cells)
    return tuple(norm)


def all_orientations(cells):
    """
    Generate all unique orientations (rotations + flips) of a shape.
    Returns list of normalized tuples of (x, y).
    """
    def rotate90(x, y):
        return y, -x

    def flipx(x, y):
        return -x, y

    seen = set()
    oris = []

    for r in range(4):
        rot = cells
        for _ in range(r):
            rot = [rotate90(x, y) for x, y in rot]
        for flip in (False, True):
            if flip:
                trans = [flipx(x, y) for x, y in rot]
            else:
                trans = rot
            norm = normalize_cells(trans)
            if norm not in seen:
                seen.add(norm)
                oris.append(norm)

    return oris


def build_shape_orientations(shapes):
    """
    For each shape (rows), compute all unique orientations as normalized lists of cells.
    Returns:
        shape_oris: list indexed by shape index; each entry is list of orientations,
                    each orientation is tuple of (x, y) cells.
        shape_areas: list of area (number of '#' cells) per shape.
    """
    shape_oris = []
    shape_areas = []
    for rows in shapes:
        base_cells = shape_cells_from_rows(rows)
        oris = all_orientations(base_cells)
        shape_oris.append(oris)
        shape_areas.append(len(oris[0]))  # all orientations have same area
    return shape_oris, shape_areas


def build_placements_for_region(w, h, counts, shape_oris):
    """
    For a given region (w x h) and requested counts, generate all possible placements.

    Returns:
        placements_cells: list of list of board cell indices
        placements_shape: list of shape index for each placement
        cell_to_placements: dict mapping cell index -> list of placement indices
    """
    placements_cells = []
    placements_shape = []
    cell_to_placements = {}

    for s, cnt in enumerate(counts):
        if cnt <= 0:
            continue
        oris = shape_oris[s]
        for ori in oris:
            maxx = max(x for x, y in ori)
            maxy = max(y for x, y in ori)
            if maxx + 1 > w or maxy + 1 > h:
                continue
            # Slide orientation over the board
            for oy in range(h - maxy):
                row_base = oy * w
                for ox in range(w - maxx):
                    cells = []
                    for cx, cy in ori:
                        idx = row_base + cy * w + (ox + cx)
                        cells.append(idx)
                    p_idx = len(placements_cells)
                    placements_cells.append(cells)
                    placements_shape.append(s)
                    for idx_cell in cells:
                        cell_to_placements.setdefault(idx_cell, []).append(p_idx)

    return placements_cells, placements_shape, cell_to_placements


def region_can_fit(w, h, counts, shape_oris, shape_areas, solver=None):
    """
    Check if a given region can fit all requested shapes, using ILP.
    Returns True/False.
    """
    # Basic sanity: counts length must match number of shapes
    if len(counts) != len(shape_oris):
        return False

    # Simple area check
    total_present_area = sum(c * shape_areas[i] for i, c in enumerate(counts))
    if total_present_area > w * h:
        return False

    # Generate placements
    placements_cells, placements_shape, cell_to_placements = build_placements_for_region(
        w, h, counts, shape_oris
    )

    # If a shape is requested but has no placements, impossible
    for s, cnt in enumerate(counts):
        if cnt > 0 and all(ps != s for ps in placements_shape):
            return False

    # Build ILP model
    prob = pulp.LpProblem("presents_region", pulp.LpMinimize)

    n_placements = len(placements_cells)
    if n_placements == 0:
        # Only possible if all counts are zero; else impossible
        return all(c == 0 for c in counts)

    x_vars = [
        pulp.LpVariable(f"x_{i}", lowBound=0, upBound=1, cat="Binary")
        for i in range(n_placements)
    ]

    # Objective: no need to optimize anything, just feasibility
    prob += 0

    # Shape count constraints: for each shape s, sum x_p == counts[s]
    for s, required in enumerate(counts):
        if required == 0:
            continue
        indices = [i for i, sh in enumerate(placements_shape) if sh == s]
        if not indices and required > 0:
            return False
        prob += pulp.lpSum(x_vars[i] for i in indices) == required

    # Cell constraints: each cell used at most once
    for cell_idx, p_indices in cell_to_placements.items():
        prob += pulp.lpSum(x_vars[i] for i in p_indices) <= 1

    # Solve
    if solver is None:
        solver = pulp.PULP_CBC_CMD(msg=False)

    status = prob.solve(solver)
    return pulp.LpStatus[status] == "Optimal"


def main():
    lines = [line.rstrip("\n") for line in sys.stdin]
    shapes, regions = parse_input(lines)
    shape_oris, shape_areas = build_shape_orientations(shapes)

    if not regions:
        print(0)
        return

    # Check all regions
    solver = pulp.PULP_CBC_CMD(msg=False)
    ok = 0
    total = len(regions)

    for idx, (w, h, counts) in enumerate(regions, start=1):
        can_fit = region_can_fit(w, h, counts, shape_oris, shape_areas, solver=solver)
        if can_fit:
            ok += 1

    print(ok)


if __name__ == "__main__":
    main()
