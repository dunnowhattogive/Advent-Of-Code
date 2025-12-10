import sys
from collections import deque

def read_lines():
	if len(sys.argv) > 1:
		path = sys.argv[1]
		with open(path, 'r') as f:
			lines = [ln.rstrip('\n') for ln in f]
	else:
		lines = [ln.rstrip('\n') for ln in sys.stdin]
	return lines

def find_start(grid):
	for r, row in enumerate(grid):
		c = row.find('S')
		if c != -1:
			return r, c
	return None, None

def quantum_timelines(grid):
	h = len(grid)
	if h == 0:
		return 0, 0
	w = len(grid[0])
	sr, sc = find_start(grid)
	# ensure both start row and column are found before using sc
	if sr is None or sc is None or sr + 1 >= h:
		return 0, 0
	# counts of histories entering current row (start at row sr+1)
	curr = [0] * w
	curr[sc] = 1
	for r in range(sr + 1, h):
		# work on a mutable list for this row
		row_counts = curr[:]  # counts at columns entering this row
		# cascade: process any counts that are currently on a splitter '^'
		q = deque([c for c in range(w) if row_counts[c] > 0 and grid[r][c] == '^'])
		visited_in_queue = [False] * w
		for c in q:
			visited_in_queue[c] = True
		while q:
			c = q.popleft()
			visited_in_queue[c] = False
			cnt = row_counts[c]
			if cnt == 0:
				continue
			if grid[r][c] != '^':
				continue
			# beam(s) hitting splitter stop here and spawn left/right on same row
			row_counts[c] = 0
			if c - 1 >= 0:
				row_counts[c - 1] += cnt
				# if newly landed on a splitter, schedule it
				if grid[r][c - 1] == '^' and not visited_in_queue[c - 1]:
					q.append(c - 1)
					visited_in_queue[c - 1] = True
			if c + 1 < w:
				row_counts[c + 1] += cnt
				if grid[r][c + 1] == '^' and not visited_in_queue[c + 1]:
					q.append(c + 1)
					visited_in_queue[c + 1] = True
		# remaining row_counts are beams that will continue downward into next row
		curr = row_counts
	# after last row processed:
	total_multiplicity = sum(curr)               # total timelines (counting merged multiplicities)
	distinct_exits = sum(1 for v in curr if v > 0)  # number of distinct exit columns
	return total_multiplicity, distinct_exits

def main():
	lines = read_lines()
	if not lines:
		print(0)
		return
	width = max(len(ln) for ln in lines)
	grid = [ln.ljust(width) for ln in lines]

	# simple CLI mode: --mode=multiplicity (default), --mode=distinct, --mode=both
	mode = 'multiplicity'
	for a in sys.argv[1:]:
		if a.startswith('--mode='):
			mode = a.split('=', 1)[1].strip().lower()

	total, distinct = quantum_timelines(grid)
	if mode == 'distinct':
		print(distinct)
	elif mode == 'both':
		# print both values so you can compare
		print(f"multiplicity:{total}")
		print(f"distinct:{distinct}")
	else:
		print(total)

if __name__ == "__main__":
	main()
