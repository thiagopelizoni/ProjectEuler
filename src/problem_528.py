# Problem: https://projecteuler.net/problem=528
import numpy as np
from numba import njit, prange

MOD = 1000000007

@njit(fastmath=True, cache=True)
def mod_pow(base, exp):
    res = 1
    base %= MOD
    while exp > 0:
        if exp % 2 == 1:
            res = (res * base) % MOD
        base = (base * base) % MOD
        exp //= 2
    return res

@njit(fastmath=True, cache=True)
def mod_inverse(a):
    return mod_pow(a, MOD - 2)

@njit(fastmath=True, cache=True)
def combinations_large_n(n, k, fact_k_inv):
    if n < k:
        return 0
    n_mod = n % MOD
    numerator = 1
    for i in range(k):
        numerator = (numerator * (n_mod - i)) % MOD
    return (numerator * fact_k_inv) % MOD

@njit(fastmath=True, cache=True)
def compute_mask_contribution(mask, count, exponents, n, k, fact_k_inv):
    sum_e = 0
    set_bits = 0
    for i in range(count):
        if (mask >> i) & 1:
            sum_e += exponents[i]
            set_bits += 1
    if sum_e > n:
        return 0
    term = combinations_large_n(n - sum_e + k, k, fact_k_inv)
    if set_bits % 2 == 1:
        return -term
    else:
        return term

@njit(parallel=True, fastmath=True, cache=True)
def solve(k):
    n = 10 ** k
    exponents = np.empty(k + 2, dtype=np.int64)
    count = 0
    for i in range(1, k + 1):
        val = (k ** i) + 1
        if val <= n:
            exponents[count] = val
            count += 1
        else:
            break
    fact_k = 1
    for i in range(1, k + 1):
        fact_k = (fact_k * i) % MOD
    fact_k_inv = mod_inverse(fact_k)
    limit_mask = 1 << count
    total = 0
    for mask in prange(limit_mask):
        val = compute_mask_contribution(mask, count, exponents, n, k, fact_k_inv)
        total += val
    return (total % MOD + MOD) % MOD

def main():
    total_sum = 0
    for k in range(10, 16):
        term_val = solve(k)
        total_sum = (total_sum + term_val) % MOD
    print(total_sum)

if __name__ == "__main__":
    main()