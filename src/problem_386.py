# Problem: https://projecteuler.net/problem=386
import os
from concurrent.futures import ProcessPoolExecutor
from functools import lru_cache
from tqdm import tqdm

def fill_sieve(size):
    if size < 2:
        return []
    half = size // 2
    sieve = [True] * (half + 1)
    sieve[0] = False
    for i in range(1, int(half**0.5) + 1):
        if sieve[i]:
            start = 2 * i * (i + 1)
            step = 2 * i + 1
            for j in range(start, half + 1, step):
                sieve[j] = False
    primes = [2]
    for i in range(1, half + 1):
        if sieve[i] and 2 * i + 1 <= size:
            primes.append(2 * i + 1)
    return primes

@lru_cache(maxsize=None)
def antichain(exps, target):
    if target < 0:
        return 0
    if not exps:
        return 1 if target == 0 else 0
    if sum(exps) < target:
        return 0
    if len(exps) == 1:
        return 1 if 0 <= target <= exps[0] else 0
    result = 0
    first = exps[0]
    rest = exps[1:]
    for i in range(first + 1):
        result += antichain(rest, target - i)
    return result

cache = {}
def evaluate(factors):
    if not factors:
        return 1
    exponents = []
    count = 1
    for i in range(1, len(factors)):
        if factors[i] == factors[i - 1]:
            count += 1
        else:
            exponents.append(count)
            count = 1
    exponents.append(count)
    exponents.sort()
    key = tuple(exponents)
    if key in cache:
        return cache[key]
    total = len(factors)
    half = total // 2
    num = antichain(key, half)
    cache[key] = num
    return num

def search(limit, current, min_idx, factors):
    result = evaluate(factors)
    start_idx = min_idx
    for idx in range(start_idx, len(primes)):
        p = primes[idx]
        next_current = current * p
        if next_current > limit:
            break
        factors.append(p)
        result += search(limit, next_current, idx, factors)
        factors.pop()
    return result

def compute_chunk(start, end, limit):
    local_result = 0
    for idx in range(start, end):
        p = primes[idx]
        if p > limit:
            break
        local_factors = [p]
        local_result += search(limit, p, idx, local_factors)
    return local_result

def chunk_wrapper(args):
    return compute_chunk(*args)

def main():
    """
    Purpose
    -------
    Compute the sum of N(n) for 1 <= n <= 10^8, where N(n) is the maximum
    length of an antichain in the set of divisors of n.

    Method / Math Rationale
    ------------------------
    N(n) is the size of the largest rank in the divisor poset, which is the
    number of divisors d with Omega(d) = floor(Omega(n)/2), where Omega is
    the total number of prime factors with multiplicity. This is computed as
    the coefficient of x^{floor(Omega(n)/2)} in the generating function
    product over i (1 + x + ... + x^{e_i}) where e_i are the exponents in
    the prime factorization of n.
    We generate all n by recursively building their sorted list of prime
    factors (with multiplicity) using increasing primes, compute the sorted
    exponents, and add the precomputed antichain size using memoized
    recursion for the coefficient.

    Complexity
    ----------
    Time complexity is O(number of partial factorizations), empirically
    acceptable with parallelism (runs in seconds to minutes depending on
    hardware).

    References
    ----------
    https://projecteuler.net/problem=386
    """
    global primes
    limit = 100000000
    primes = fill_sieve(limit)
    total = 1  # for n=1
    num_cpus = os.cpu_count()
    num_primes = len(primes)
    chunk_size = (num_primes // num_cpus) + 1
    chunks = []
    for i in range(num_cpus):
        start = i * chunk_size
        end = min((i + 1) * chunk_size, num_primes)
        if start >= end:
            break
        chunks.append((start, end, limit))
    with ProcessPoolExecutor(max_workers=num_cpus) as executor:
        for res in tqdm(executor.map(chunk_wrapper, chunks),
                        total=len(chunks)):
            total += res
    print(total)

if __name__ == "__main__":
    main()