import sys

def count_removable(grid):
	# grid: list of list of chars
	h = len(grid)
	if h == 0:
		return 0
	dirs = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
	total_removed = 0
	while True:
		to_remove = []
		for r in range(h):
			row = grid[r]
			for c in range(len(row)):
				if row[c] != '@':
					continue
				adj = 0
				for dr, dc in dirs:
					nr, nc = r + dr, c + dc
					if 0 <= nr < h and 0 <= nc < len(grid[nr]) and grid[nr][nc] == '@':
						adj += 1
						if adj >= 4:
							break
				if adj < 4:
					to_remove.append((r, c))
		if not to_remove:
			break
		for r, c in to_remove:
			grid[r][c] = '.'
		total_removed += len(to_remove)
	return total_removed

def main():
	# read input from file (first arg) or stdin
	if len(sys.argv) > 1:
		path = sys.argv[1]
		with open(path, 'r') as f:
			lines = [line.rstrip('\n') for line in f]
	else:
		lines = [line.rstrip('\n') for line in sys.stdin]
	# ignore empty lines
	lines = [ln for ln in lines if ln != '']
	# convert to mutable grid
	grid = [list(ln) for ln in lines]
	print(count_removable(grid))

if __name__ == "__main__":
	main()
