#!/usr/bin/env python3
"""Sum invalid product IDs: numbers made of a sequence of digits repeated twice.

Input: a single line containing comma-separated ranges like
  11-22,95-115,998-1012,...

For each range inclusive, find all numbers that are of the form XX where
X is a block of digits (no leading zeros in either the full number or the block),
e.g. 55 (5 twice), 6464 (64 twice), 123123 (123 twice).

Output: print the sum of all invalid IDs found.
"""
import sys
import re
import argparse


def iter_ranges_from_line(line):
	parts = [p.strip() for p in line.strip().split(',') if p.strip()]
	for part in parts:
		if '-' not in part:
			continue
		a, b = part.split('-', 1)
		try:
			lo = int(a)
			hi = int(b)
		except Exception:
			continue
		if lo > hi:
			lo, hi = hi, lo
		yield lo, hi


def is_double_repeat(n: int) -> bool:
	s = str(n)
	L = len(s)
	# must be even length and non-zero
	if L % 2 != 0:
		return False
	half = L // 2
	a = s[:half]
	b = s[half:]
	# No leading zero allowed for the number; since n is int, leading zeros not present.
	# Also block should not have leading zero.
	if a[0] == '0':
		return False
	return a == b


def sum_invalid_in_range(lo: int, hi: int) -> int:
	total = 0
	# Instead of scanning every number in large ranges, generate double-repeat numbers
	# of even length and test if they fall into range.
	# Determine min and max lengths to consider
	min_len = len(str(lo))
	max_len = len(str(hi))
	# ensure even lengths only
	for L in range(min_len, max_len + 1):
		if L % 2 != 0:
			continue
		half = L // 2
		# first half cannot have leading zero; so first digit 1-9
		start = 10 ** (half - 1)
		end = 10 ** half - 1
		for first in range(start, end + 1):
			s = str(first) + str(first)
			val = int(s)
			if val < lo:
				continue
			if val > hi:
				break
			total += val
	return total


def solve_ranges_line(line: str) -> int:
	total = 0
	for lo, hi in iter_ranges_from_line(line):
		total += sum_invalid_in_range(lo, hi)
	return total


def main(argv=None):
	parser = argparse.ArgumentParser(description='Sum invalid double-repeat IDs from ranges')
	parser.add_argument('input_file', nargs='?', help='path to input file (default: stdin)')
	args = parser.parse_args(argv)

	if args.input_file:
		with open(args.input_file, 'r') as f:
			content = f.read()
	else:
		content = sys.stdin.read()

	# The ranges may be wrapped across lines; combine into one string
	content = content.replace('\n', ',')
	content = content.strip()
	if not content:
		print(0)
		return
	result = solve_ranges_line(content)
	print(result)


if __name__ == '__main__':
	main()

