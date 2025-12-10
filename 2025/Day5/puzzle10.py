import sys

def parse_ranges_section(lines):
	# split at first blank line
	sep = None
	for i, ln in enumerate(lines):
		if ln.strip() == '':
			sep = i
			break
	if sep is None:
		section = [ln.strip() for ln in lines if ln.strip() != '']
	else:
		section = [ln.strip() for ln in lines[:sep] if ln.strip() != '']
	return section

def parse_intervals(lines):
	ints = []
	for ln in lines:
		if '-' not in ln:
			continue
		a, b = ln.split('-', 1)
		try:
			s = int(a)
			e = int(b)
		except ValueError:
			continue
		if s > e:
			s, e = e, s
		ints.append((s, e))
	return ints

def merge_intervals(intervals):
	if not intervals:
		return []
	intervals.sort()
	merged = []
	cs, ce = intervals[0]
	for s, e in intervals[1:]:
		if s <= ce + 1:
			if e > ce:
				ce = e
		else:
			merged.append((cs, ce))
			cs, ce = s, e
	merged.append((cs, ce))
	return merged

def main():
	if len(sys.argv) > 1:
		path = sys.argv[1]
		with open(path, 'r') as f:
			lines = [ln.rstrip('\n') for ln in f]
	else:
		lines = [ln.rstrip('\n') for ln in sys.stdin]
	ranges_lines = parse_ranges_section(lines)
	intervals = parse_intervals(ranges_lines)
	merged = merge_intervals(intervals)
	total = sum(e - s + 1 for s, e in merged)
	print(total)

if __name__ == "__main__":
	main()
