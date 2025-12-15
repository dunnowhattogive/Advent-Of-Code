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


def count_paths(graph, start='you', goal='out'):
    memo = {}
    visiting = set()

    def dfs(u):
        if u == goal:
            return 1
        if u in memo:
            return memo[u]
        if u in visiting:
            # cycle detected; avoid infinite recursion — treat as 0
            return 0
        visiting.add(u)
        total = 0
        for v in graph.get(u, []):
            total += dfs(v)
        visiting.remove(u)
        memo[u] = total
        return total

    return dfs(start)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            inp = f.read()
    else:
        inp = sys.stdin.read()
    graph = parse(inp)
    print(count_paths(graph))
