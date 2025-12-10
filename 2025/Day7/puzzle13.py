import sys

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

def simulate(grid):
	h = len(grid)
	if h == 0:
		return 0
	w = len(grid[0])
	sr, sc = find_start(grid)
	if sr is None:
		return 0
	# Use presence set for beams (merge multiple beams into one)
	beams = set()
	if sr + 1 >= h:
		return 0
	beams.add(sc)
	split_count = 0
	for r in range(sr + 1, h):
		if not beams:
			break
		next_beams = set()
		for c in beams:
			if not (0 <= c < w):
				continue
			if grid[r][c] == '^':
				# one split for this column (merged beams count as one)
				split_count += 1
				if c - 1 >= 0:
					next_beams.add(c - 1)
				if c + 1 < w:
					next_beams.add(c + 1)
			else:
				# beam continues downward (merged)
				next_beams.add(c)
		beams = next_beams
	return split_count

def main():
	lines = read_lines()
	if not lines:
		print(0)
		return
	width = max(len(ln) for ln in lines)
	# pad lines to uniform width with spaces
	grid = [ln.ljust(width) for ln in lines]
	print(simulate(grid))

if __name__ == "__main__":
	main()