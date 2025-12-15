import sys
from collections import deque

def read_points(path=None):
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

def compress_coords(points):
	xs = set()
	ys = set()
	for x, y in points:
		xs.add(x)
		xs.add(x + 1)
		ys.add(y)
		ys.add(y + 1)
	minx = min(x for x, _ in points)
	maxx = max(x for x, _ in points)
	miny = min(y for _, y in points)
	maxy = max(y for _, y in points)
	# ensure outer boundary present
	xs.add(minx)
	xs.add(maxx + 1)
	ys.add(miny)
	ys.add(maxy + 1)
	xs_list = sorted(xs)
	ys_list = sorted(ys)
	x_to_i = {x: i for i, x in enumerate(xs_list)}
	y_to_j = {y: j for j, y in enumerate(ys_list)}
	cols = len(xs_list) - 1
	rows = len(ys_list) - 1
	return xs_list, ys_list, x_to_i, y_to_j, cols, rows

def build_allowed(points, xs_list, ys_list, x_to_i, y_to_j, cols, rows):
	# allowed compressed cells (row-major: rows x cols)
	allowed = [[False] * cols for _ in range(rows)]
	# mark red positions (map original points to compressed indices)
	red_comp = []
	for x, y in points:
		ix = x_to_i[x]
		jy = y_to_j[y]
		allowed[jy][ix] = True
		red_comp.append((ix, jy))
	# mark segments between consecutive points (wrapped)
	n = len(points)
	for k in range(n):
		x1, y1 = points[k]
		x2, y2 = points[(k + 1) % n]
		if x1 == x2:
			ix = x_to_i[x1]
			ylo = min(y1, y2)
			yhi = max(y1, y2)
			j0 = y_to_j[ylo]
			j1 = y_to_j[yhi]
			for j in range(j0, j1 + 1):
				allowed[j][ix] = True
		elif y1 == y2:
			jy = y_to_j[y1]
			xlo = min(x1, x2)
			xhi = max(x1, x2)
			i0 = x_to_i[xlo]
			i1 = x_to_i[xhi]
			for i in range(i0, i1 + 1):
				allowed[jy][i] = True
		else:
			# should not happen per problem statement
			raise ValueError("Adjacent points not aligned")
	return allowed, red_comp

def fill_interior(allowed, cols, rows):
	# BFS from boundary empty compressed cells to mark external reachable cells
	vis = [[False] * cols for _ in range(rows)]
	q = deque()
	for i in range(cols):
		if not allowed[0][i]:
			vis[0][i] = True
			q.append((0, i))
		if not allowed[rows - 1][i] and not vis[rows - 1][i]:
			vis[rows - 1][i] = True
			q.append((rows - 1, i))
	for j in range(rows):
		if not allowed[j][0] and not vis[j][0]:
			vis[j][0] = True
			q.append((j, 0))
		if not allowed[j][cols - 1] and not vis[j][cols - 1]:
			vis[j][cols - 1] = True
			q.append((j, cols - 1))
	dirs = [(1,0),(-1,0),(0,1),(0,-1)]
	while q:
		r, c = q.popleft()
		for dr, dc in dirs:
			nr, nc = r + dr, c + dc
			if 0 <= nr < rows and 0 <= nc < cols and not vis[nr][nc] and not allowed[nr][nc]:
				vis[nr][nc] = True
				q.append((nr, nc))
	# any compressed cell not visited and not allowed is interior -> becomes green (allowed)
	for r in range(rows):
		for c in range(cols):
			if not allowed[r][c] and not vis[r][c]:
				allowed[r][c] = True

def build_weighted_prefix(allowed, xs_list, ys_list, cols, rows):
	# ps has shape (rows+1) x (cols+1)
	ps = [[0] * (cols + 1) for _ in range(rows + 1)]
	for r in range(rows):
		for c in range(cols):
			if allowed[r][c]:
				width = xs_list[c + 1] - xs_list[c]
				height = ys_list[r + 1] - ys_list[r]
				area = width * height
			else:
				area = 0
			ps[r + 1][c + 1] = ps[r][c + 1] + ps[r + 1][c] - ps[r][c] + area
	return ps

def rect_area_allowed(ps, x0, y0, x1, y1):
	# inclusive compressed indices: cols x rows
	# x0..x1, y0..y1
	return ps[y1 + 1][x1 + 1] - ps[y0][x1 + 1] - ps[y1 + 1][x0] + ps[y0][x0]

def max_allowed_rectangle_area(points):
	if not points:
		return 0
	xs_list, ys_list, x_to_i, y_to_j, cols, rows = compress_coords(points)
	allowed, red_comp = build_allowed(points, xs_list, ys_list, x_to_i, y_to_j, cols, rows)
	fill_interior(allowed, cols, rows)
	ps = build_weighted_prefix(allowed, xs_list, ys_list, cols, rows)
	max_area = 0
	n = len(red_comp)
	for a in range(n):
		x1, y1 = red_comp[a]
		for b in range(a + 1, n):
			x2, y2 = red_comp[b]
			if x1 == x2 or y1 == y2:
				continue
			minx = min(x1, x2)
			maxx = max(x1, x2)
			miny = min(y1, y2)
			maxy = max(y1, y2)
			total_cells = (xs_list[maxx + 1] - xs_list[minx]) * (ys_list[maxy + 1] - ys_list[miny])
			allowed_area = rect_area_allowed(ps, minx, miny, maxx, maxy)
			if allowed_area == total_cells and allowed_area > max_area:
				max_area = allowed_area
	return max_area

def main():
	path = sys.argv[1] if len(sys.argv) > 1 else None
	points = read_points(path)
	print(max_allowed_rectangle_area(points))

if __name__ == "__main__":
	main()