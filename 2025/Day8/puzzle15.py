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
	def component_sizes(self):
		return [s for s in self.size if s > 0]

def product_top3(nums):
	if not nums:
		return 1
	nums = sorted(nums, reverse=True)
	prod = 1
	for i in range(min(3, len(nums))):
		prod *= nums[i]
	# if fewer than 3 components, treat missing ones as 1 (no change)
	return prod

def main():
	# input path optional; default to Day8 input file
	path = sys.argv[1] if len(sys.argv) > 1 else '/home/vikasv/projects/AOC/2025/Day8/input.txt'
	points = read_points(path)
	n = len(points)
	if n == 0:
		print(1)
		return
	# build all pair distances (squared to avoid float)
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
	if not pairs:
		# only one point
		print(1)
		return
	pairs.sort(key=lambda t: (t[0], t[1], t[2]))
	K = min(1000, len(pairs))
	dsu = DSU(n)
	# connect the K closest pairs (even if union doesn't change components)
	for k in range(K):
		_, a, b = pairs[k]
		dsu.union(a, b)
	sizes = dsu.component_sizes()
	print(product_top3(sizes))

if __name__ == "__main__":
	main()
