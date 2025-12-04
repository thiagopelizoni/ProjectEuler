# Problem: https://projecteuler.net/problem=545
import numpy as np
from numba import njit, prange

TARGET_INDEX = 100000
BASE_MULTIPLIER = 308
LIMIT_X = 3_000_000 
MAX_PRIME_SEARCH = BASE_MULTIPLIER * LIMIT_X + 1000

@njit(fastmath=True, cache=True)
def gcd_scalar(a, b):
    while b:
        a, b = b, a % b
    return a

@njit(parallel=True, fastmath=True, cache=True)
def sieve_primes(n):
    sieve = np.ones(n + 1, dtype=np.bool_)
    sieve[0] = False
    sieve[1] = False
    limit = int(n**0.5) + 1
    for i in range(2, limit):
        if sieve[i]:
            sieve[i*i : n+1 : i] = False
    return np.flatnonzero(sieve)

@njit(parallel=True, fastmath=True, cache=True)
def compute_valid_mask(limit_x, primes):
    bad_mask = np.zeros(limit_x + 1, dtype=np.bool_)
    target_primes = np.array([2, 3, 5, 23, 29], dtype=np.int64)
    num_primes = len(primes)
    for i in prange(num_primes):
        p = primes[i]
        is_target = False
        for tp in target_primes:
            if p == tp:
                is_target = True
                break
        if is_target:
            continue
        p_minus_1 = p - 1
        g = gcd_scalar(p_minus_1, BASE_MULTIPLIER)
        m = p_minus_1 // g
        if m <= limit_x:
            bad_mask[m::m] = True
    return bad_mask

@njit(fastmath=True, cache=True)
def find_nth_valid(bad_mask, n):
    count = 0
    for x in range(1, len(bad_mask)):
        if not bad_mask[x]:
            count += 1
            if count == n:
                return x
    return -1

def main():
    primes = sieve_primes(MAX_PRIME_SEARCH)
    bad_mask = compute_valid_mask(LIMIT_X, primes)
    x = find_nth_valid(bad_mask, TARGET_INDEX)
    if x == -1:
        pass
    else:
        result = x * BASE_MULTIPLIER
        print(result)

if __name__ == "__main__":
    main()