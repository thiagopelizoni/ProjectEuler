# Problem: https://projecteuler.net/problem=347
import bisect
import math

from sympy import primerange
from tqdm import tqdm

def main():
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