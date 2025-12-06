# Problem: https://projecteuler.net/problem=549
import numpy as np
from numba import njit, prange
import math

@njit(fastmath=True, cache=True)
def get_s_prime_power(p, e):
    if e == 1:
        return p
    cnt = 0
    m = 0
    while cnt < e:
        m += p
        temp = m
        while temp % p == 0:
            cnt += 1
            temp //= p
    return m

@njit(fastmath=True, parallel=True, cache=True)
def sieve_and_solve(limit):
    S = np.zeros(limit + 1, dtype=np.int64)
    is_prime = np.ones(limit + 1, dtype=np.bool_)
    is_prime[0] = False
    is_prime[1] = False
    sqrt_limit = int(math.sqrt(limit))
    for i in range(2, sqrt_limit + 1):
        if is_prime[i]:
            is_prime[i*i : limit+1 : i] = False
    count = 0
    for i in range(2, limit + 1):
        if is_prime[i]:
            count += 1
    primes = np.empty(count, dtype=np.int64)
    idx = 0
    for i in range(2, limit + 1):
        if is_prime[i]:
            primes[idx] = i
            idx += 1
    split_idx = 0
    for i in range(count):
        if primes[i] > sqrt_limit:
            split_idx = i
            break
    small_primes = primes[:split_idx]
    large_primes = primes[split_idx:]
    chunk_size = 65536
    num_chunks = (limit + chunk_size) // chunk_size
    for c in prange(num_chunks):
        start = c * chunk_size
        end = start + chunk_size
        if end > limit + 1:
            end = limit + 1
        if start < 2:
            start = 2
        for p in small_primes:
            q = p
            e = 1
            while q < end:
                cost = get_s_prime_power(p, e)
                k_start = (start + q - 1) // q
                first_idx = k_start * q
                if first_idx < start: 
                    first_idx += q
                if first_idx < end:
                    for i in range(first_idx, end, q):
                        if cost > S[i]:
                            S[i] = cost
                if q > limit // p:
                    break
                q *= p
                e += 1
                if q >= end:
                    break
    for i in prange(len(large_primes)):
        p = large_primes[i]
        for mult in range(p, limit + 1, p):
            S[mult] = p
    total_sum = 0
    for x in S:
        total_sum += x
    return total_sum

def main():
    LIMIT = 10**8
    result = sieve_and_solve(LIMIT)
    print(result)

if __name__ == "__main__":
    main()