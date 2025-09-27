# Problem: https://projecteuler.net/problem=364
from tqdm import tqdm

def main():
    """
    Purpose
    -------
    Solves Project Euler problem 364 by computing T(1000000) modulo 100000007, where T(N) is the number of ways
    N seats are occupied by N people following the given rules.

    Method / Math Rationale
    -----------------------
    Uses the summation formula from OEIS A192008: T(n) = sum over v1,v2 in {0,1} and nonnegative m,k with
    2*m + 3*k = n-1 - v1 - v2 of (m+k+1)! * binom(m+k, m) * 2^k * (k + v1 + v2)! * (m+k)!. Equivalent form
    groups by v = v1 + v2 with multiplicity for v=1. Precomputes factorials modulo 100000007 and uses modular
    inverses for binomials.

    Complexity
    ----------
    O(N) time for precomputing factorials and iterating over possible m values; O(N) space for factorials.

    References
    ----------
    https://projecteuler.net/problem=364
    https://oeis.org/A192008
    """
    def mod_binom(p, q, mod):
        if q < 0 or q > p:
            return 0
        return fact[p] * pow(fact[q], mod - 2, mod) % mod * pow(fact[p - q], mod - 2, mod) % mod

    N = 1000000
    MOD = 100000007
    fact = [1] * (N + 2)
    for i in tqdm(range(1, N + 2)):
        fact[i] = fact[i - 1] * i % MOD
    r = 0
    for v in range(3):
        target = N - 1 - v
        mult = 1 + (1 if v == 1 else 0)
        for m in range(target // 2 + 1):
            temp = target - 2 * m
            if temp % 3 == 0:
                k = temp // 3
                if k >= 0:
                    term = fact[m + k + 1] * mod_binom(m + k, m, MOD) * pow(2, k, MOD) * fact[k + v] * fact[m + k] % MOD
                    r = (r + term * mult % MOD) % MOD
    print(r)

if __name__ == "__main__":
    main()