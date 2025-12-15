import sys

def read_points(path=None):
	# read from file path or stdin
	if path:
		with open(path, 'r') as f:
			lines = [ln.strip() for ln in f if ln.strip()]
	else:
		lines = [ln.strip() for ln in sys.stdin if ln.strip()]
	points = []
	for ln in lines:
		parts = ln.split(',')
		if len(parts) != 2:
			continue
		try:
			x, y = map(int, parts)
		except ValueError:
			continue
		points.append((x, y))
	return points

def max_rectangle_area(points):
	n = len(points)
	if n < 2:
		return 0
	max_area = 0
	# brute-force all unordered pairs (sufficient for typical input sizes)
	for i in range(n):
		x1, y1 = points[i]
		for j in range(i + 1, n):
			x2, y2 = points[j]
			if x1 == x2 or y1 == y2:
				continue
			area = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
			if area > max_area:
				max_area = area
	return max_area

def main():
	path = sys.argv[1] if len(sys.argv) > 1 else None
	points = read_points(path)
	print(max_rectangle_area(points))

if __name__ == "__main__":
	main()
