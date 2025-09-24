# Problem: https://projecteuler.net/problem=347
import bisect
import math

from sympy import primerange
from tqdm import tqdm

def main():
    """
    Purpose
    -------
    Computes the sum of the largest integers <= 10^7 that are divisible only
    by exactly two distinct primes p < q.

    Method / Math Rationale
    ------------------------
    Generates all primes up to 10^7 / 2 using sympy.primerange. Iterates over
    small primes p <= sqrt(10^7), for each p finds subsequent primes q > p
    with p*q <= 10^7, and for each pair (p,q) computes the maximum p^a * q^b
    <= 10^7 by starting with a=1, b=1 and greedily maximizing b for each
    increasing a until p^a * q > limit. Sums all such maximum values.

    Complexity
    ----------
    Time: O(number of pairs * log N) where number of pairs is approximately
    (N log log N)/log N, so overall O(N log log N), efficient for N=10^7.

    References
    ----------
    https://projecteuler.net/problem=347
    """
    limit = 10000000
    max_prime_needed = limit // 2 + 1
    primes = list(primerange(2, max_prime_needed))
    total_sum = 0
    sqrt_limit = math.isqrt(limit) + 1
    small_primes = [p for p in primes if p <= sqrt_limit]
    for p in tqdm(small_primes):
        idx = bisect.bisect_right(primes, p)
        for q_idx in range(idx, len(primes)):
            q = primes[q_idx]
            if p * q > limit:
                break
            max_product = 0
            product = p * q
            while product <= limit:
                current = product
                while current * q <= limit:
                    current *= q
                if current > max_product:
                    max_product = current
                product *= p
            total_sum += max_product
    print(total_sum)

if __name__ == "__main__":
    main()