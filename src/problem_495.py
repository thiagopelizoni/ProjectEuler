# Problem: https://projecteuler.net/problem=495
import numpy as np
import numba
from collections import Counter
from tqdm import tqdm
from math import factorial as math_factorial

@numba.njit
def add_series(dp, s, MOD, MAX_E):
    for j in range(s, MAX_E + 1):
        dp[j] = (dp[j] + dp[j - s]) % MOD

def get_primes(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    return [i for i in range(2, n + 1) if is_prime[i]]

def get_exponents(primes, n):
    exponents = []
    for p in primes:
        e = 0
        pp = p
        while pp <= n:
            e += n // pp
            pp *= p
        exponents.append(e)
    return exponents

def generate_partitions(n):
    def rec(remaining, max_part, current):
        if remaining == 0:
            yield current[:]
        else:
            for part in range(1, min(max_part, remaining) + 1):
                current.append(part)
                yield from rec(remaining - part, part, current)
                current.pop()

    return list(rec(n, n, []))

def main():
    """
    Purpose
    -------
    Computes W(10000!, 30) modulo 1000000007, where W(n, k) is the number of ways to
    write n as the product of k distinct positive integers (order does not matter).

    Method / Math Rationale
    -----------------------
    Uses inclusion-exclusion derived from counting ordered tuples with distinct factors
    and dividing by k!. Groups by integer partitions of k=30, computes scalar contribution
    and product over primes of coefficients in the generating function prod_s (1 - x^s)^(-m_s),
    where m_s is the multiplicity of part s.

    Complexity
    ----------
    O(p(k) * k * max_e) ≈ 1.7e9 operations (p(30)=5604 partitions, k=30, max_e=10000),
    accelerated with Numba JIT.

    References
    ----------
    https://projecteuler.net/problem=495
    """
    MOD = 1000000007
    K = 30
    N = 10000
    MAX_E = 10000

    fact = [1]
    for i in range(1, K + 1):
        fact.append(fact[-1] * i % MOD)

    primes = get_primes(N)
    exponents = get_exponents(primes, N)

    all_parts = generate_partitions(K)

    total = 0
    for part_list in tqdm(all_parts):
        m_dict = Counter(part_list)
        exp_sum = sum((s + 1) * m_dict[s] for s in m_dict)
        sign = 1 if exp_sum % 2 == 0 else MOD - 1

        denom = 1
        for s, m in m_dict.items():
            denom = denom * pow(s, m, MOD) % MOD
            denom = denom * fact[m] % MOD

        inv_denom = pow(denom, MOD - 2, MOD)
        scalar = sign * inv_denom % MOD

        dp = np.zeros(MAX_E + 1, dtype=np.int64)
        dp[0] = 1
        for s, m in m_dict.items():
            for _ in range(m):
                add_series(dp, s, MOD, MAX_E)

        prod_p = 1
        for e in exponents:
            if e > MAX_E:
                prod_p = 0
                break
            prod_p = prod_p * dp[e] % MOD

        total = (total + scalar * prod_p) % MOD

    print(total)

if __name__ == "__main__":
    main()