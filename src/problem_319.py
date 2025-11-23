# Problem: https://projecteuler.net/problem=319
import numpy as np
from numba import njit

TARGET = 10 ** 10
MOD = 10 ** 9

@njit(fastmath=True, cache=True)
def power(a, b, m):
    res = 1
    a %= m
    while b > 0:
        if b % 2 == 1:
            res = (res * a) % m
        a = (a * a) % m
        b //= 2
    return res

@njit(fastmath=True, cache=True)
def sum_geometric_3(n, mod):
    mod2 = 2 * mod
    p3 = power(3, n, mod2)
    num = (3 * (p3 - 1)) % mod2
    return num // 2

@njit(fastmath=True, cache=True)
def sum_geometric_2(n, mod):
    p2 = power(2, n, mod)
    return (2 * (p2 - 1)) % mod

@njit(fastmath=True, cache=True)
def get_S_range_sum(L, R, mod):
    if L == R:
        return 0
    s3 = (sum_geometric_3(R, mod) - sum_geometric_3(L, mod) + mod) % mod
    s2 = (sum_geometric_2(R, mod) - sum_geometric_2(L, mod) + mod) % mod
    s1 = (R - L) % mod
    res = (s3 - s2 - s1 + mod + mod) % mod
    return res

@njit(parallel=False, fastmath=True, cache=True)
def precompute_mertens(limit):
    mu = np.zeros(limit + 1, dtype=np.int8)
    mu[1] = 1
    primes = np.zeros(limit // 2, dtype=np.int32)
    cnt = 0
    is_prime = np.ones(limit + 1, dtype=np.bool_)
    for i in range(2, limit + 1):
        if is_prime[i]:
            primes[cnt] = i
            cnt += 1
            mu[i] = -1
        for j in range(cnt):
            p = primes[j]
            if i * p > limit:
                break
            is_prime[i * p] = False
            if i % p == 0:
                mu[i * p] = 0
                break
            else:
                mu[i * p] = -mu[i]
    M = np.zeros(limit + 1, dtype=np.int32)
    curr = 0
    for i in range(1, limit + 1):
        curr += mu[i]
        M[i] = curr
    return M

@njit(fastmath=True, cache=True)
def solve():
    n = TARGET
    limit = 5_000_000
    M_small = precompute_mertens(limit)
    K_max = n // limit
    M_large = np.zeros(K_max + 1, dtype=np.int32)
    for k in range(K_max, 0, -1):
        val = n // k
        sum_m = 0
        l = 1
        while l < val:
            q = val // (l + 1)
            if q == 0:
                r = val
            else:
                r = val // q
            if q <= limit:
                m_val = M_small[q]
            else:
                idx = n // q
                m_val = M_large[idx]
            count = r - l
            sum_m += count * m_val
            l = r
        M_large[k] = 1 - sum_m
    total_sum = 0
    l = 0
    while l < n:
        k = n // (l + 1)
        if k == 0:
            r = n
        else:
            r = n // k
        if k <= limit:
            m_val = M_small[k]
        else:
            idx = n // k
            m_val = M_large[idx]
        if m_val != 0:
            term = get_S_range_sum(l, r, MOD)
            term = (term * m_val) % MOD
            total_sum = (total_sum + term) % MOD
        l = r
    final_ans = (total_sum + 1 + MOD) % MOD
    return final_ans

def main():
    result = solve()
    print(result)

if __name__ == "__main__":
    main()