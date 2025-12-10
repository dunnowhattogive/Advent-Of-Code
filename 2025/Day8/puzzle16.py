import sys

def read_points(path=None):
	if path:
		with open(path, 'r') as f:
			lines = [ln.strip() for ln in f if ln.strip() != '']
	else:
		lines = [ln.strip() for ln in sys.stdin if ln.strip() != '']
	points = []
	for ln in lines:
		parts = ln.split(',')
		if len(parts) != 3:
			continue
		try:
			x, y, z = map(int, parts)
		except ValueError:
			continue
		points.append((x, y, z))
	return points

class DSU:
	def __init__(self, n):
		self.parent = list(range(n))
		self.size = [1] * n
	def find(self, a):
		p = self.parent
		while p[a] != a:
			p[a] = p[p[a]]
			a = p[a]
		return a
	def union(self, a, b):
		ra = self.find(a)
		rb = self.find(b)
		if ra == rb:
			return False
		if self.size[ra] < self.size[rb]:
			ra, rb = rb, ra
		self.parent[rb] = ra
		self.size[ra] += self.size[rb]
		self.size[rb] = 0
		return True

def main():
	path = sys.argv[1] if len(sys.argv) > 1 else '/home/vikasv/projects/AOC/2025/Day8/input.txt'
	points = read_points(path)
	n = len(points)
	if n < 2:
		print(0)
		return
	# build all pair distances (squared)
	pairs = []
	for i in range(n):
		x1, y1, z1 = points[i]
		for j in range(i + 1, n):
			x2, y2, z2 = points[j]
			dx = x1 - x2
			dy = y1 - y2
			dz = z1 - z2
			dsq = dx*dx + dy*dy + dz*dz
			pairs.append((dsq, i, j))
	pairs.sort(key=lambda t: (t[0], t[1], t[2]))
	dsu = DSU(n)
	components = n
	for _, a, b in pairs:
		if dsu.union(a, b):
			components -= 1
			if components == 1:
				# product of X coordinates of the pair that connected the final components
				print(points[a][0] * points[b][0])
				return
	# if never connected into one component
	print(0)

if __name__ == "__main__":
	main()
