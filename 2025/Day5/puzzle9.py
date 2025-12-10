import sys
from bisect import bisect_right

def parse_sections(lines):
	# split at first blank line into ranges_section and ids_section
	sep = 0
	for i, ln in enumerate(lines):
		if ln.strip() == '':
			sep = i
			break
	if sep == 0:
		return lines, []
	ranges = [ln.strip() for ln in lines[:sep] if ln.strip() != '']
	ids = [ln.strip() for ln in lines[sep+1:] if ln.strip() != '']
	return ranges, ids

def parse_ranges(range_lines):
	ranges = []
	for ln in range_lines:
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
		ranges.append((s, e))
	return ranges

def merge_intervals(intervals):
	if not intervals:
		return []
	intervals.sort()
	merged = []
	cur_s, cur_e = intervals[0]
	for s, e in intervals[1:]:
		if s <= cur_e + 1:
			if e > cur_e:
				cur_e = e
		else:
			merged.append((cur_s, cur_e))
			cur_s, cur_e = s, e
	merged.append((cur_s, cur_e))
	return merged

def count_fresh(ids, merged):
	# Use binary search on interval start points
	if not merged:
		return 0
	starts = [s for s, _ in merged]
	count = 0
	for id_str in ids:
		try:
			x = int(id_str)
		except ValueError:
			continue
		# find rightmost interval whose start <= x
		i = bisect_right(starts, x) - 1
		if i >= 0 and merged[i][0] <= x <= merged[i][1]:
			count += 1
	return count

def main():
	if len(sys.argv) > 1:
		path = sys.argv[1]
		with open(path, 'r') as f:
			lines = [ln.rstrip('\n') for ln in f]
	else:
		lines = [ln.rstrip('\n') for ln in sys.stdin]
	ranges_section, ids_section = parse_sections(lines)
	intervals = parse_ranges(ranges_section)
	merged = merge_intervals(intervals)
	print(count_fresh(ids_section, merged))

if __name__ == "__main__":
	main()
