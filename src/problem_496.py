# Problem: https://projecteuler.net/problem=496
import numpy as np
from math import sqrt
from numba import jit, int64
from numba import types
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor
import os
from functools import partial

def compute_mu(maxn):
    mu = np.zeros(maxn + 1, dtype=np.int64)
    prime = np.full(maxn + 1, True, dtype=bool)
    prime[0] = prime[1] = False
    mu[1] = 1
    for i in range(2, maxn + 1):
        if prime[i]:
            mu[i] = -1
            for j in range(i * 2, maxn + 1, i):
                prime[j] = False
                if (j // i) % i == 0:
                    mu[j] = 0
                else:
                    mu[j] = -mu[j // i]
    return mu

MAX = 50000
mu = compute_mu(MAX)

@jit(int64(int64, types.Array(types.int64, 1, 'C')))
def sum_square_free(N, mu):
    if N <= 0:
        return 0
    sn = int(sqrt(N))
    res = 0
    for d in range(1, sn + 1):
        if mu[d] == 0:
            continue
        m = N // (d * d)
        res += mu[d] * d * d * m * (m + 1) // 2
    return res

@jit(int64(int64))
def S(M):
    if M < 6:
        return 0
    res = 0
    sm = int(sqrt(M)) + 1
    for l in range(1, sm + 1):
        low = l + 1
        high = min(2 * l - 1, M // l)
        if low > high:
            continue
        sum_s = high * (high + 1) // 2 - (low - 1) * low // 2
        res += l * sum_s
    return res

def main():
    """
    Purpose
    -------
    Solves Project Euler problem 496 by computing F(10^9), the sum of BC for all integer sided triangles
    satisfying the condition with BC <= 10^9.

    Method / Math Rationale
    ----------------------
    The condition leads to the parametrization where the sides are b = t * l^2, a = t * l * s,
    c = t * (s^2 - l^2) with 1 <= l, l+1 <= s <= 2*l - 1, t square free, a <= L.
    Then F(L) = sum t * l * s over those with t * l * s <= L.
    Using directory trick for floor functions and inclusion-exclusion for sum of square free * t.

    Complexity
    ----------
    O(sqrt(L) * sqrt(L)) = O(L) ~10^9 operations, optimized with numba for speed.

    References
    ----------
    https://projecteuler.net/problem=496
    """
    L = 10**9
    segments = []
    i = 1
    while i <= L:
        q = L // i
        j = L // q
        segments.append((i, j, q))
        i = j + 1

    total = 0
    for seg in tqdm(segments):
        i, j, q = seg
        sum_t = sum_square_free(j, mu) - sum_square_free(i - 1, mu)
        s_val = S(q)
        total += sum_t * s_val
    print(total)

if __name__ == "__main__":
    main()