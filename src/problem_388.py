# Problem: https://projecteuler.net/problem=388
from functools import lru_cache
from tqdm import tqdm
import math

def linear_mobius_sieve(limit):
    mu = [0] * (limit + 1)
    is_prime = [True] * (limit + 1)
    primes = []
    mu[1] = 1
    for i in range(2, limit + 1):
        if is_prime[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if i * p > limit:
                break
            is_prime[i * p] = False
            if i % p == 0:
                mu[i * p] = 0
                break
            else:
                mu[i * p] = -mu[i]
    M = [0] * (limit + 1)
    for i in range(1, limit + 1):
        M[i] = M[i - 1] + mu[i]
    return mu, M

PRELIMIT = 1000000
_, preM = linear_mobius_sieve(PRELIMIT)

@lru_cache(maxsize=None)
def M(x):
    if x < 0:
        return 0
    if x <= PRELIMIT:
        return preM[x]
    s = 0
    l = 2
    while l <= x:
        k = x // l
        r = min(x, x // k)
        s += (r - l + 1) * M(k)
        l = r + 1
    return 1 - s

def main():
    """
    Purpose
    -------
    Solves Project Euler problem 388: Compute D(10^10), the number of distinct lines from the origin to
    lattice points in [0, N]^3 excluding the origin, and outputs the first nine digits followed by the
    last nine digits.

    Method / Math Rationale
    ------------------------
    D(N) = sum_{d=1}^N mu(d) * [ (floor(N/d) + 1)^3 - 1 ]
    Use segmented summation with Mertens function M(x) for efficient computation. M(x) is computed
    recursively with memoization using the relation sum_{m=1}^x M(floor(x/m)) = 1.
    Precompute M(x) for x <= 10^6 using linear sieve.

    Complexity
    ----------
    Time: O(N^{2/3}) for the recursive M(x) computations due to memoization and segment grouping.

    References
    ----------
    https://projecteuler.net/problem=388
    """
    N = 10**10
    s = 0
    l = 1
    pbar = tqdm(total=math.isqrt(N) * 2)
    while l <= N:
        k = N // l
        r = min(N, N // k)
        m = k + 1
        s += (M(r) - M(l - 1)) * (m**3 - 1)
        pbar.update(r - l + 1)
        l = r + 1
    pbar.close()
    d_str = str(s)
    print(d_str[:9] + d_str[-9:])

if __name__ == "__main__":
    main()