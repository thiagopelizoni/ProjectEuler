# Problem: https://projecteuler.net/problem=427
from tqdm import tqdm

MOD = 1000000009
N = 7500000

def main():
    """
    Purpose
    -------
    Computes the sum of the lengths of the longest contiguous subsequences with the same value
    over all sequences of length n with elements in [1, n], modulo 1000000009, for n=7500000.

    Method / Math Rationale
    -----------------------
    Computes f(n) = n^{n+1} - sum_{k=1}^n g(k) mod MOD, where g(k) is the number of sequences
    with maximum run length <k. g(k) = solve(n,k) - solve(n-k,k), where solve(nn,k) =
    sum_{i=0}^{floor(nn/k)} (1-n)^i * n^{nn - i k} * binom(nn - i (k-1), i) % MOD.
    This is derived from inclusion-exclusion on the number of ways to place i disjoint blocks
    of k identical symbols, with the subtraction adjusting for boundary cases.

    Complexity
    ----------
    O(n log n) due to precomputing factorials and inverses in O(n), and the main loop over
    k=1 to n with inner sums of total length sum_k floor(n/k) = O(n log n).

    References
    ----------
    https://projecteuler.net/problem=427
    """
    n = N
    mod = MOD

    fac = [0] * (n + 1)
    inv = [0] * (n + 1)
    ifac = [0] * (n + 1)

    fac[0] = 1
    for i in range(1, n + 1):
        fac[i] = fac[i - 1] * i % mod

    inv[1] = 1
    for i in range(2, n + 1):
        inv[i] = (mod - mod // i) * inv[mod % i] % mod

    ifac[0] = 1
    for i in range(1, n + 1):
        ifac[i] = ifac[i - 1] * inv[i] % mod

    def binom(nn, mm):
        if nn < mm or nn < 0 or mm < 0:
            return 0
        return fac[nn] * ifac[mm] % mod * ifac[nn - mm] % mod

    def solve(nn, k):
        if k == 0 or nn < 0:
            return 0
        res = 0
        p1 = pow(n, nn, mod)
        p2 = 1
        lim = nn // k
        for i in range(lim + 1):
            res = (res + p1 * p2 % mod * binom(nn - i * k + i, i) % mod) % mod
            p1 = p1 * pow(inv[n], k, mod) % mod if n != 0 else 0
            p2 = p2 * (1 - n) % mod
        return res

    ans = pow(n, n + 1, mod)
    for i in tqdm(range(1, n + 1)):
        ans = (ans + solve(n - i, i) - solve(n, i) + mod) % mod

    print(ans)

if __name__ == "__main__":
    main()