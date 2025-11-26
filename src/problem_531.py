# Problem: https://projecteuler.net/problem=531
import numpy as np
from numba import njit, prange

@njit(fastmath=True, cache=True)
def get_phis(n):
    phi = np.arange(n, dtype=np.int64)
    for i in range(2, n):
        if phi[i] == i:
            for j in range(i, n, i):
                phi[j] -= phi[j] // i
    return phi

@njit(fastmath=True, cache=True)
def egcd_coeff(a, b):
    r0, r1 = a, b
    t0, t1 = 1, 0
    while r1:
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        t0, t1 = t1, t0 - q * t1
    return r0, t0

@njit(parallel=True, fastmath=True, cache=True)
def solve_kernel(start, limit):
    phis = get_phis(limit)
    partials = np.zeros(limit - start, dtype=np.int64)
    for n in prange(start, limit):
        row_sum = 0
        a = phis[n]
        for m in range(n + 1, limit):
            b = phis[m]
            diff = b - a
            g, inv = egcd_coeff(n, m)            
            if diff % g != 0:
                continue
            m_g = m // g
            diff_g = diff // g
            k = (inv * diff_g) % m_g
            x = a + n * k
            row_sum += x
        partials[n - start] = row_sum
        
    return partials

def main():
    START = 1_000_000
    LIMIT = 1_005_000
    partials = solve_kernel(START, LIMIT)
    total = sum(int(x) for x in partials)
    print(total)

if __name__ == "__main__":
    main()