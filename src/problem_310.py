# Problem: https://projecteuler.net/problem=310
import math
from tqdm import tqdm

def main():
    N = 100000
    max_k = int(math.sqrt(N)) + 1
    squares = [k * k for k in range(1, max_k + 1) if k * k <= N]
    g = [0] * (N + 1)
    for n in tqdm(range(1, N + 1)):
        reachable = set()
        for sq in squares:
            if sq > n:
                break
            reachable.add(g[n - sq])
        mex = 0
        while mex in reachable:
            mex += 1
        g[n] = mex
    max_g = max(g)
    G = max_g + 1
    prefix = [[0] * (N + 2) for _ in range(G)]
    for x in range(N + 1):
        gr = g[x]
        for gg in range(G):
            prefix[gg][x + 1] = prefix[gg][x]
        prefix[gr][x + 1] += 1
    suffix = [[0] * (N + 2) for _ in range(G)]
    for x in range(N, -1, -1):
        gr = g[x]
        for gg in range(G):
            suffix[gg][x] = suffix[gg][x + 1]
        suffix[gr][x] += 1
    total = 0
    for b in range(N + 1):
        gb = g[b]
        for ga in range(G):
            target = ga ^ gb
            if target > max_g:
                continue
            total += prefix[ga][b + 1] * suffix[target][b]
    print(total)

if __name__ == "__main__":
    main()