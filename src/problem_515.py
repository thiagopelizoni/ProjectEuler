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