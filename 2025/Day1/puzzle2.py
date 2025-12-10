#!/usr/bin/env python3
"""Part 2: count every time needle passes over/lands on 0 (method 0x434C49434B)."""
import sys


def count_zeros_all_clicks(lines):
	pos = 50
	zeros = 0
	for raw in lines:
		line = raw.strip()
		if not line:
			continue
		dirc = line[0].upper()
		try:
			dist = int(line[1:])
		except Exception:
			continue

		if dirc == 'L':
			k0 = pos % 100
		else:
			k0 = (-pos) % 100

		k_first = k0 if k0 != 0 else 100
		if k_first <= dist:
			zeros += 1 + (dist - k_first) // 100

		if dirc == 'L':
			pos = (pos - dist) % 100
		else:
			pos = (pos + dist) % 100

	return zeros


def main(argv=None):
	argv = argv if argv is not None else sys.argv[1:]
	if len(argv) >= 1:
		path = argv[0]
		with open(path, 'r') as f:
			lines = f.readlines()
	else:
		lines = sys.stdin.readlines()

	print(count_zeros_all_clicks(lines))


if __name__ == '__main__':
	main()

