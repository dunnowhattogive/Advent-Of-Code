#!/usr/bin/env python3
"""Find and sum the largest two-digit numbers from lines of input."""

import sys

def max_two_digit_from_line(s: str) -> int:
	if len(s) < 2:
		return 0
	max_val = 0
	for i in range(len(s) - 1):
		a = ord(s[i]) - 48
		for j in range(i + 1, len(s)):
			b = ord(s[j]) - 48
			val = 10 * a + b
			if val > max_val:
				max_val = val
	return max_val

def main():
	if len(sys.argv) > 1:
		path = sys.argv[1]
		with open(path, 'r') as f:
			lines = [line.strip() for line in f]
	else:
		lines = [line.strip() for line in sys.stdin]

	total = 0
	for line in lines:
		if not line:
			continue
		digits = ''.join(ch for ch in line if ch.isdigit())
		if not digits:
			continue
		total += max_two_digit_from_line(digits)

	print(total)

if __name__ == "__main__":
	main()
