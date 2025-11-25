import numpy as np
from numba import njit, prange

@njit(fastmath=True, cache=True)
def power(a: int, b: int, m: int) -> int:
    res = 1
    a %= m
    while b > 0:
        if b % 2 == 1:
            res = (res * a) % m
        a = (a * a) % m
        b //= 2
    return res

@njit(fastmath=True, cache=True)
def inverse(n: int, m: int) -> int:
    return power(n, m - 2, m)

@njit(parallel=True, fastmath=True, cache=True)
def compute_sum_pure(n: int, mod: int, fact: np.ndarray, invFact: np.ndarray) -> int:
    terms = np.zeros(n, dtype=np.int64)
    fact_n = fact[n]
    for k in prange(2, n - 1):
        inv_k = (invFact[k] * fact[k - 1]) % mod
        coeff = (fact_n * invFact[n - k]) % mod
        coeff = (coeff * inv_k) % mod
        base = n - k - 1
        exponent = n - k
        p_val = power(base, exponent, mod)
        terms[k] = (coeff * p_val) % mod
    total_sum = terms.sum() % mod
    return total_sum

@njit(fastmath=True, cache=True)
def solve(n: int, mod: int) -> int:
    fact = np.empty(n + 1, dtype=np.int64)
    invFact = np.empty(n + 1, dtype=np.int64)
    fact[0] = 1
    for i in range(1, n + 1):
        fact[i] = (fact[i - 1] * i) % mod
    invFact[n] = inverse(fact[n], mod)
    for i in range(n - 1, -1, -1):
        invFact[i] = (invFact[i + 1] * (i + 1)) % mod
    sum_pure = compute_sum_pure(n, mod, fact, invFact)
    term1 = (n * (n - 1)) % mod
    if n > 2:
        p1 = power(n - 2, n - 1, mod)
        term1 = (term1 * p1) % mod
    else:
        term1 = 0
    total = (term1 + sum_pure) % mod
    return total

def main():
    n = 12344321
    mod = 135707531
    result = solve(n, mod)
    print(result)

if __name__ == "__main__":
    main()