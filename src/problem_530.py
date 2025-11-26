# Problem: https://projecteuler.net/problem=530
import numpy as np
from numba import njit, prange
import math

@njit(fastmath=True, cache=True)
def get_phi(n):
    phi = np.arange(n + 1, dtype=np.int64)
    for i in range(2, n + 1):
        if phi[i] == i:
            phi[i::i] -= phi[i::i] // i
    return phi

@njit(fastmath=True, cache=True)
def divisor_sum(n):
    r = int(math.sqrt(n))
    s = 0
    for i in range(1, r + 1):
        s += n // i
    return 2 * s - r * r

@njit(parallel=True, fastmath=True, cache=True)
def solve(L):
    limit_sqrt = int(math.sqrt(L))
    phi = get_phi(limit_sqrt)
    total = 0
    
    for k in prange(1, limit_sqrt + 1):
        term = L // (k * k)
        if term > 0:
            ds = divisor_sum(term)
            total += phi[k] * ds
            
    return total

def main():
    L = 10**15
    result = solve(L)
    print(result)

if __name__ == "__main__":
    main()