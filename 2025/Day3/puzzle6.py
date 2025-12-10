import sys

def max_k_digits_from_line(s: str, k: int) -> int:
	# s: string of digits; return integer value of max k-digit subsequence (preserving order)
	n = len(s)
	if n < k:
		return 0
	pos = 0
	remaining = k
	digits = []
	while remaining > 0:
		# we must pick one digit from s[pos : n - remaining + 1] inclusive
		end = n - remaining
		# find max digit and its first index in the allowed window
		max_d = '-1'
		max_idx = pos
		for idx in range(pos, end + 1):
			ch = s[idx]
			if ch > max_d:
				max_d = ch
				max_idx = idx
				# early exit if we found '9'
				if ch == '9':
					break
		digits.append(max_d)
		pos = max_idx + 1
		remaining -= 1
	return int(''.join(digits))

def main():
	INPUT_K = 12
	# read input from file (first arg) or stdin
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
		total += max_k_digits_from_line(digits, INPUT_K)

	print(total)

if __name__ == "__main__":
	main()
