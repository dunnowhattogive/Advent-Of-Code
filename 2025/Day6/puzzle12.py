import sys
from functools import reduce
import operator

def read_lines():
	# ...existing code...
	if len(sys.argv) > 1:
		path = sys.argv[1]
		with open(path, 'r') as f:
			lines = [ln.rstrip('\n') for ln in f]
	else:
		lines = [ln.rstrip('\n') for ln in sys.stdin]
	return lines

def find_column_groups(lines):
	if not lines:
		return [], []
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
	# determine non-empty rows in this group's span
	row_has = [any(grid[r][c] != ' ' for c in range(start, end+1)) for r in range(len(grid))]
	non_empty_rows = [i for i, v in enumerate(row_has) if v]
	if not non_empty_rows:
		return 0
	op_row_idx = non_empty_rows[-1]
	op_row_segment = grid[op_row_idx][start:end+1]
	# find operator char
	op_char = None
	for ch in op_row_segment:
		if ch in '+*':
			op_char = ch
			break
	if op_char is None:
		strip = op_row_segment.strip()
		op_char = strip[0] if strip else '+'
	# collect numbers: for each column from right to left, gather digits from rows 0..op_row_idx-1 (top->bottom)
	nums = []
	for c in range(end, start - 1, -1):
		digits = ''.join(grid[r][c] for r in range(0, op_row_idx) if grid[r][c].isdigit())
		if digits:
			nums.append(int(digits))
	if not nums:
		return 0
	if op_char == '+':
		return sum(nums)
	if op_char == '*':
		return reduce(operator.mul, nums, 1)
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