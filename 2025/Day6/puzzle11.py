import sys
from functools import reduce
import operator

def read_lines():
	if len(sys.argv) > 1:
		path = sys.argv[1]
		with open(path, 'r') as f:
			lines = [ln.rstrip('\n') for ln in f]
	else:
		lines = [ln.rstrip('\n') for ln in sys.stdin]
	# preserve blank lines within input; but remove trailing completely empty file
	if not lines:
		return []
	return lines

def find_column_groups(lines):
	if not lines:
		return []
	width = max(len(ln) for ln in lines)
	grid = [ln.ljust(width) for ln in lines]
	col_has = [any(grid[r][c] != ' ' for r in range(len(grid))) for c in range(width)]
	groups = []
	in_group = False
	start = 0
	for c, has in enumerate(col_has):
		if has and not in_group:
			in_group = True
			start = c
		elif not has and in_group:
			groups.append((start, c - 1))
			in_group = False
	if in_group:
		groups.append((start, width - 1))
	return grid, groups

def parse_and_eval_group(grid, start, end):
	# extract segment rows and collect non-empty rows (trimmed)
	segs = [row[start:end+1] for row in grid]
	non_empty = [s.rstrip() for s in segs if s.strip() != '']
	if not non_empty:
		return 0
	op_row = non_empty[-1]
	# find first operator char in operator row
	op_char = None
	for ch in op_row:
		if ch in '+*':
			op_char = ch
			break
	if op_char is None:
		# fallback: take first non-space char
		op_char = op_row.strip()[0]
	# parse number rows (all rows above operator)
	num_rows = non_empty[:-1]
	nums = []
	for nr in num_rows:
		digits = ''.join(ch for ch in nr if ch.isdigit())
		if digits:
			nums.append(int(digits))
	# evaluate
	if not nums:
		return 0
	if op_char == '+':
		return sum(nums)
	elif op_char == '*':
		return reduce(operator.mul, nums, 1)
	# unknown op -> treat as 0
	return 0

def main():
	lines = read_lines()
	grid, groups = find_column_groups(lines)
	total = 0
	for s, e in groups:
		total += parse_and_eval_group(grid, s, e)
	print(total)

if __name__ == "__main__":
	main()