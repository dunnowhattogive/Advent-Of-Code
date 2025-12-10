import sys

def count_accessible(grid):
	# grid: list of strings
	h = len(grid)
	if h == 0:
		return 0
	dirs = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
	count = 0
	for r, row in enumerate(grid):
		for c, ch in enumerate(row):
			if ch != '@':
				continue
			adj = 0
			for dr, dc in dirs:
				nr, nc = r + dr, c + dc
				if 0 <= nr < h and 0 <= nc < len(grid[nr]) and grid[nr][nc] == '@':
					adj += 1
					if adj >= 4:
						break
			if adj < 4:
				count += 1
	return count

def main():
	# read input from file (first arg) or stdin
	if len(sys.argv) > 1:
		path = sys.argv[1]
		with open(path, 'r') as f:
			lines = [line.rstrip('\n') for line in f]
	else:
		lines = [line.rstrip('\n') for line in sys.stdin]
	# ignore empty trailing/leading lines
	lines = [ln for ln in lines if ln != '']
	print(count_accessible(lines))

if __name__ == "__main__":
	main()
