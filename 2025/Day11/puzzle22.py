import sys
from collections import defaultdict


def parse(text):
    g = defaultdict(list)
    for line in text.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        if ':' not in line:
            continue
        left, right = line.split(':', 1)
        src = left.strip()
        toks = [t for t in right.strip().split() if t]
        g[src].extend(toks)
    return g


def count_paths_with_both(graph, start='svr', goal='out', a='dac', b='fft'):
    memo = {}
    visiting = set()

    def dfs(u, saw_a, saw_b):
        key = (u, saw_a, saw_b)
        if key in memo:
            return memo[key]
        if u == goal:
            # count only if both seen
            return 1 if (saw_a and saw_b) else 0
        if u in visiting:
            return 0
        visiting.add(u)
        total = 0
        for v in graph.get(u, []):
            total += dfs(v, saw_a or (v == a), saw_b or (v == b))
        visiting.remove(u)
        memo[key] = total
        return total

    # starting node may itself be a or b
    start_saw_a = (start == a)
    start_saw_b = (start == b)
    return dfs(start, start_saw_a, start_saw_b)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            inp = f.read()
    else:
        inp = sys.stdin.read()
    g = parse(inp)
    print(count_paths_with_both(g))
