# Problem: https://projecteuler.net/problem=365
from itertools import combinations
from math import comb
from tqdm import tqdm
from sympy.ntheory import primerange

def lucas_binom(n, k, p, fact, invfact):
    if k > n:
        return 0
    res = 1
    while n or k:
        n1 = n % p
        k1 = k % p
        if k1 > n1:
            return 0
        res = res * fact[n1] * invfact[k1] * invfact[n1 - k1] % p
        n //= p
        k //= p
    return res

def compute(triple, n, k, p_to_data):
    p, q, r = triple
    fact_p, invfact_p = p_to_data[p]
    fact_q, invfact_q = p_to_data[q]
    fact_r, invfact_r = p_to_data[r]
    ap = lucas_binom(n, k, p, fact_p, invfact_p)
    aq = lucas_binom(n, k, q, fact_q, invfact_q)
    ar = lucas_binom(n, k, r, fact_r, invfact_r)
    m = p * q * r
    M1 = q * r
    M2 = p * r
    M3 = p * q
    y1 = pow(M1 % p, p - 2, p)
    y2 = pow(M2 % q, q - 2, q)
    y3 = pow(M3 % r, r - 2, r)
    x = (ap * M1 * y1 + aq * M2 * y2 + ar * M3 * y3) % m
    return x

def main():
    """
    Purpose
    -------
    Solves Project Euler problem 365 by computing the sum of binom(10^18, 10^9) mod (p*q*r) over all primes
    1000 < p < q < r < 5000.

    Method / Math Rationale
    -----------------------
    Uses Lucas' theorem to compute binom(n, k) mod prime s as the product of binomials on base s digits.
    Precomputes factorial and inverse factorial mod each prime for fast modular binomial coefficients.
    For each triple of primes, computes the binomial mod each prime, then combines using the Chinese
    Remainder Theorem to get mod pqr. Uses sequential computation with progress bar for visibility.

    Complexity
    ----------
    O( (number of primes choose 3) * (log n / log min_prime) ) for main computations, approximately
    O(500^3 * 6) ~ 4e8 operations.

    References
    ----------
    https://projecteuler.net/problem=365
    """
    n = 10**18
    k = 10**9
    primes = list(primerange(1001, 5000))
    p_to_data = {}
    for p in primes:
        fact = [1] * p
        for i in range(1, p):
            fact[i] = fact[i - 1] * i % p
        invfact = [0] * p
        invfact[p - 1] = pow(fact[p - 1], p - 2, p)
        for i in range(p - 2, -1, -1):
            invfact[i] = invfact[i + 1] * (i + 1) % p
        p_to_data[p] = (fact, invfact)
    total_triples = comb(len(primes), 3)
    total = 0
    for triple in tqdm(combinations(primes, 3), total=total_triples):
        total += compute(triple, n, k, p_to_data)
    print(total)

if __name__ == "__main__":
    main()