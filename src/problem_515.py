# Problem: https://projecteuler.net/problem=515
import sys
from math import isqrt
from tqdm import tqdm


def generate_primes_up_to(n):
    if n < 2:
        return []
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, isqrt(n) + 1):
        if sieve[i]:
            for j in range(i * i, n + 1, i):
                sieve[j] = False
    return [i for i in range(2, n + 1) if sieve[i]]


def segmented_sieve(L, R):
    limit = isqrt(R) + 1
    small_primes = generate_primes_up_to(limit)
    is_prime = [True] * (R - L)
    for q in tqdm(small_primes, file=sys.stderr):
        if q * q >= R:
            break
        start = max(q * q, ((L + q - 1) // q) * q)
        for i in range(start, R, q):
            if i >= L:
                is_prime[i - L] = False
    primes = [L + i for i in range(R - L) if is_prime[i]]
    return primes


def main():
    """
    Purpose
    -------
    Computes and prints the value of D(10^9, 10^5, 10^5) as defined in Project Euler Problem 515.

    Method / Math Rationale
    ------------------------
    The function generates all primes p in [10^9, 10^9 + 10^5) using segmented sieve.
    For each such prime, computes the modular inverse of (10^5 - 1) modulo p using Fermat's Little Theorem.
    Sums these inverses and prints the total.
    This is based on the derivation that d(p, p-1, k) mod p = (k-1)^{-1} mod p,
    obtained from expressing the iterated sum using binomial coefficients and evaluating the polynomial sum modulo p.

    Complexity
    ----------
    Time: O(sqrt(10^9) + 10^5 log log 10^5) for sieving, plus O(number of primes * log(10^9)) for inverses,
    where number of primes is approximately 10^5 / ln(10^9) ≈ 4800.

    References
    ----------
    https://projecteuler.net/problem=515
    """
    a = 1000000000
    b = 100000
    k = 100000
    primes = segmented_sieve(a, a + b)
    total = 0
    m = k - 1
    for p in primes:
        inv = pow(m, p - 2, p)
        total += inv
    print(total)


if __name__ == "__main__":
    main()