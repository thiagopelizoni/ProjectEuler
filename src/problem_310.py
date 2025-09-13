# Problem: https://projecteuler.net/problem=310
import math
from tqdm import tqdm

def main():
    """
    Purpose
    Solve Project Euler problem 310 by counting the number of losing positions for the next player
    in Nim Square with heap sizes 0 <= a <= b <= c <= 100000.

    Args
    None

    Returns
    None

    Method / Math Rationale
    Compute Grundy numbers g(n) = mex { g(n - k^2) for k >= 1, k^2 <= n } for n = 0 to N.
    A position (a, b, c) is losing if g(a) ^ g(b) ^ g(c) == 0. Precompute prefix[gr][x+1] as count
    of y <= x with g(y) == gr, and suffix[gr][x] as count of y >= x with g(y) == gr. For each b,
    sum over ga the prefix[ga][b+1] * suffix[ga ^ g(b)][b], which gives the count of a <= b <= c
    with the xor condition.

    Complexity
    O(N sqrt N) for Grundy numbers + O(N G) for prefix/suffix and counting, where G is max Grundy
    value + 1.

    References
    https://projecteuler.net/problem=310
    """
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