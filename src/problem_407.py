# Problem: https://projecteuler.net/problem=407
import numpy as np
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing
from tqdm import tqdm
import numba

@numba.njit
def search(n, largest_prime_arr):
    if n == 1:
        return 0
    p = largest_prime_arr[n]
    if p == n:
        return 1
    start = n - (n % p)
    x = start
    while x >= p:
        next_ = x + 1
        if (next_ * next_) % n == next_:
            return next_
        if (x * x) % n == x:
            return x
        x -= p
    return 1

def init_largest_prime(lim):
    global largest_prime
    largest_prime = np.full(lim + 1, 1, dtype=np.int64)
    for i in range(2, lim + 1):
        if largest_prime[i] > 1:
            continue
        for j in range(i, lim + 1, i):
            largest_prime[j] = i
        j = i * i
        while j <= lim:
            largest_prime[j] = j
            j *= i

def partial_sum(start, end):
    global largest_prime
    s = 0
    for n in range(start, end + 1):
        s += search(n, largest_prime)
    return s

def main():
    """
    Purpose
    -------
    Computes the sum of M(n) for 1 <= n <= 10^7, where M(n) is the largest a < n such that
    a^2 ≡ a mod n, and prints the result.

    Method / Math Rationale:
    -----------------------
    Precomputes an array where for each n, the value is n if n is a prime power (including
    primes), else the largest prime factor of n.
    For each n:
    - If n=1, M(n)=0
    - If the array value == n (prime power), M(n)=1
    - Else, p = largest prime factor, iterate x from n down to p in steps of -p (multiples
      of p), check if x+1 or x satisfies a^2 % n == a (with a possibly >n, but check fails
      naturally if so), return the largest such a.
    This efficiently finds the maximum idempotent <n by checking candidates where a ≡ 0 or
    1 mod p, leveraging that p divides a or a-1 for any idempotent a.

    Complexity
    ----------
    Precomputation: O(N log log N) for sieve-like pass.
    Computation: For each n, O(n / p) operations where p is largest prime factor; total
    empirically acceptable for N=10^7 (runs in seconds with parallelism).

    References
    ----------
    https://projecteuler.net/problem=407
    """
    limit = 10000000
    num_workers = multiprocessing.cpu_count()
    num_chunks = num_workers * 10
    chunk_size = (limit + num_chunks - 1) // num_chunks
    with ProcessPoolExecutor(max_workers=num_workers, initializer=init_largest_prime,
                             initargs=(limit,)) as executor:
        futures = []
        current = 1
        while current <= limit:
            end = min(current + chunk_size - 1, limit)
            futures.append(executor.submit(partial_sum, current, end))
            current = end + 1
        total = 0
        for future in tqdm(as_completed(futures), total=len(futures)):
            total += future.result()
    print(total)

if __name__ == "__main__":
    main()