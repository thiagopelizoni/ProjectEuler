# Problem: https://projecteuler.net/problem=537
import numpy as np
from numba import njit, prange

@njit(fastmath=True, cache=True)
def get_primes(n):
    limit = int(n * 1.3 * np.log(n)) + 100
    s = np.ones(limit, dtype=np.bool_)
    s[0] = s[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if s[i]:
            s[i*i::i] = False
    return np.flatnonzero(s)

@njit(parallel=True, fastmath=True, cache=True)
def poly_mul_mod(A, B, k_max, m):
    nA, nB = len(A), len(B)
    sz = min(k_max + 1, nA + nB - 1)
    C = np.zeros(sz, dtype=np.int64)
    
    for i in prange(sz):
        start = max(0, i - nB + 1)
        end = min(i + 1, nA)
        acc = 0
        for j in range(start, end):
            term = (A[j] * B[i - j]) % m
            acc = (acc + term)
            if acc >= m:
                acc -= m
        C[i] = acc
    return C

@njit(cache=True)
def solve(N, mod):
    primes = get_primes(N + 10)
    P = np.zeros(N + 1, dtype=np.int64)
    P[0] = 1
    for k in range(1, N + 1):
        P[k] = (primes[k] - primes[k-1]) % mod
        
    res = np.zeros(1, dtype=np.int64)
    res[0] = 1
    base = P
    exp = N
    
    while exp > 0:
        if exp % 2 == 1:
            res = poly_mul_mod(res, base, N, mod)
        base = poly_mul_mod(base, base, N, mod)
        exp //= 2
        
    return res[N]

def main():
    N = 20000
    MOD = 1004535809
    result = solve(N, MOD)
    print(result)

if __name__ == "__main__":
    main()