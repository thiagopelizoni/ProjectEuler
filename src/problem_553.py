# Problem: https://projecteuler.net/problem=553
import numpy as np
from numba import njit, prange

MOD = 1_000_000_007

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
def inverse(n, m):
    return power(n, m - 2, m)

@njit(fastmath=True, cache=True)
def precompute_factorials(n, mod):
    fact = np.empty(n + 1, dtype=np.int64)
    inv_fact = np.empty(n + 1, dtype=np.int64)
    fact[0] = 1
    inv_fact[0] = 1
    for i in range(1, n + 1):
        fact[i] = (fact[i - 1] * i) % mod
    inv_fact[n] = inverse(fact[n], mod)
    for i in range(n - 1, 0, -1):
        inv_fact[i] = (inv_fact[i + 1] * (i + 1)) % mod
    return fact, inv_fact

@njit(fastmath=True, cache=True)
def nCr_mod(n, r, fact, inv_fact, mod):
    if r < 0 or r > n:
        return 0
    num = fact[n]
    den = (inv_fact[r] * inv_fact[n - r]) % mod
    return (num * den) % mod

@njit(parallel=True, fastmath=True, cache=True)
def poly_mul_mod_trunc(A, B, limit, fact, inv_fact, mod):
    size_a = min(len(A), limit + 1)
    size_b = min(len(B), limit + 1)
    C = np.zeros(limit + 1, dtype=np.int64)
    for n in prange(limit + 1):
        start_k = max(0, n - size_b + 1)
        end_k = min(n, size_a - 1)
        if start_k > end_k:
            continue
        sum_val = 0
        n_fact = fact[n]
        for k in range(start_k, end_k + 1):
            coeff = (inv_fact[k] * inv_fact[n - k]) % mod
            term = (A[k] * B[n - k]) % mod
            term = (term * coeff) % mod
            sum_val = (sum_val + term) % mod
        C[n] = (sum_val * n_fact) % mod
    return C

@njit(fastmath=True, cache=True)
def poly_pow_mod(A, k, limit, fact, inv_fact, mod):
    base = A.copy()
    res_poly = np.zeros(limit + 1, dtype=np.int64)
    res_poly[0] = 1
    exp = k
    while exp > 0:
        if exp % 2 == 1:
            res_poly = poly_mul_mod_trunc(res_poly, base, limit, fact, inv_fact, mod)
        if exp > 1:
            base = poly_mul_mod_trunc(base, base, limit, fact, inv_fact, mod)
        exp //= 2
    return res_poly

@njit(parallel=True, fastmath=True, cache=True)
def get_a_coefficients(limit, fact, inv_fact, mod):
    G = np.empty(limit + 1, dtype=np.int64)
    mod_phi = mod - 1
    for n in prange(limit + 1):
        if n == 0:
            G[n] = 1
        else:
            e = (power(2, n, mod_phi) - 1 + mod_phi) % mod_phi
            G[n] = power(2, e, mod)
    a = np.zeros(limit + 1, dtype=np.int64)
    a[0] = 0
    for n in range(limit):
        sum_val = 0
        n_fact = fact[n]
        for k in range(n):
            term = (G[n - k] * a[k + 1]) % mod
            coeff = (inv_fact[k] * inv_fact[n - k]) % mod
            term = (term * coeff) % mod
            sum_val = (sum_val + term) % mod
        sum_val = (sum_val * n_fact) % mod
        diff = (G[n + 1] - G[n]) % mod
        if diff < 0:
            diff += mod
        res = (diff - sum_val) % mod
        if res < 0:
            res += mod
        a[n + 1] = res
    return a

@njit(fastmath=True, cache=True)
def solve_problem_553(limit_n, k_target):
    fact, inv_fact = precompute_factorials(limit_n, MOD)
    a_coeffs = get_a_coefficients(limit_n, fact, inv_fact, MOD)
    p_coeffs = poly_pow_mod(a_coeffs, k_target, limit_n, fact, inv_fact, MOD)
    inv_k_fact = inv_fact[k_target]
    for i in range(len(p_coeffs)):
        p_coeffs[i] = (p_coeffs[i] * inv_k_fact) % MOD
    n = limit_n
    ans = 0
    n_fact = fact[n]
    for j in range(n + 1):
        term = p_coeffs[j]
        binom = (n_fact * inv_fact[j]) % MOD
        binom = (binom * inv_fact[n - j]) % MOD
        term = (term * binom) % MOD
        ans = (ans + term) % MOD
    return ans

def main():
    LIMIT = 10000
    K = 10
    print(solve_problem_553(LIMIT, K))

if __name__ == "__main__":
    main()