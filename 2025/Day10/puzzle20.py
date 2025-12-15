#!/usr/bin/env python3
import sys
import re
import pulp


def parse_line(line):
    """
    Parse a single machine line into:
      buttons: list of tuples of indices (one tuple per button)
      target: list of ints
    Example:
      "[##..#.] (2) (4,5) ... {4,135,127,8,135,155}"
    """
    # Get all (...) segments – these are the buttons.
    button_parts = re.findall(r'\(([^)]*)\)', line)
    buttons = []
    for part in button_parts:
        part = part.strip()
        if part == "":
            buttons.append(())
        else:
            buttons.append(tuple(int(x) for x in part.split(',')))

    # Get {...} – the target joltage vector.
    m = re.search(r'\{([^}]*)\}', line)
    if not m:
        raise ValueError("No target {} found in line: %r" % line)
    target_vals = [int(x) for x in m.group(1).split(',')]

    return buttons, target_vals


def solve_machine_lp(buttons, target):
    """
    Solve:
      For each counter i:
        sum_{j: i in buttons[j]} x_j == target[i]
      x_j >= 0 integer
      Minimize sum_j x_j

    Returns minimum total presses as an int.
    """
    m = len(target)      # number of counters
    n = len(buttons)     # number of buttons

    # Build incidence matrix A where A[i][j] = 1 if button j affects counter i.
    A = [[0] * n for _ in range(m)]
    for j, b in enumerate(buttons):
        for idx in b:
            if idx < 0 or idx >= m:
                raise ValueError("Button index %d out of range for %d counters" % (idx, m))
            A[idx][j] = 1

    # Define ILP
    prob = pulp.LpProblem("machine", pulp.LpMinimize)

    # One variable per button: how many times we press it.
    x = [pulp.LpVariable(f"x_{j}", lowBound=0, cat="Integer") for j in range(n)]

    # Objective: minimize total presses
    prob += pulp.lpSum(x)

    # Constraints: for each counter i, sum over buttons that affect it = target[i]
    for i in range(m):
        prob += pulp.lpSum(x[j] for j in range(n) if A[i][j] == 1) == target[i]

    # Solve
    status = prob.solve(pulp.PULP_CBC_CMD(msg=False))
    if pulp.LpStatus[status] != "Optimal":
        raise RuntimeError("No optimal solution found (status: %s)" % pulp.LpStatus[status])

    # Extract integer solution
    presses = 0
    for var in x:
        val = var.value()
        if val is None:
            raise RuntimeError("Variable has no value in solution")
        presses += int(round(val))

    return presses


def main():
    lines = [line.strip() for line in sys.stdin if line.strip()]
    total = 0
    per_machine = []

    for i, line in enumerate(lines, 1):
        buttons, target = parse_line(line)
        presses = solve_machine_lp(buttons, target)
        per_machine.append(presses)
        total += presses

    for i, presses in enumerate(per_machine, 1):
        print("Machine %d: %d presses" % (i, presses))

    print("Total presses:", total)


if __name__ == "__main__":
    main()
