# Problem: https://projecteuler.net/problem=441
import numba
import numpy as np
import math
import os
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor

@numba.njit
def compute_contrib(d: int, mu, H, N: int) -> float:
    if mu[d] == 0:
        return 0.0
    M = (N - 1) // d
    high = N // d
    sum_m = 0.0
    for m in range(1, M + 1):
        p = d * m
        low = m + 1
        if low > high:
            break
        k0 = (N - p + d - 1) // d
        left_high = min(k0 - 1, high)
        right_low = max(low, k0)
        sum1 = 0.0
        if left_high >= low:
            sum1 = (p + 1) * (H[left_high] - H[low - 1])
        sum2 = 0.0
        if right_low <= high:
            sum2 = (N + 1) * (H[high] - H[right_low - 1]) - d * (high - right_low + 1.0)
        sum_m += (sum1 + sum2) / m
    return mu[d] * sum_m / (d * d)

@numba.njit
def compute_chunk(start: int, end: int, mu, H, N: int) -> float:
    s = 0.0
    for d in range(start, end + 1):
        s += compute_contrib(d, mu, H, N)
    return s

def compute_mobius(n: int):
    mu = np.zeros(n + 1, dtype=np.int64)
    is_prime = np.ones(n + 1, dtype=bool)
    primes = []
    mu[1] = 1
    for i in range(2, n + 1):
        if is_prime[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if i * p > n:
                break
            is_prime[i * p] = False
            if i % p == 0:
                mu[i * p] = 0
                break
            else:
                mu[i * p] = -mu[i]
    return mu

mu = None
H = None
the_N = 0

def init_worker():
    global mu, H, the_N
    the_N = 10000000
    mu = compute_mobius(the_N)
    H = np.zeros(the_N + 2, dtype=np.float64)
    H[1:] = np.cumsum(1.0 / np.arange(1, the_N + 2))

def chunk_func(ch):
    start, end = ch
    return compute_chunk(start, end, mu, H, the_N)

def main():
    """
    Purpose
    -------
    Computes S(10^7) as defined in Project Euler problem 441 and prints it rounded to four decimal places.

    Method / Math Rationale
    -----------------------
    Utilizes Mobius inversion to filter coprime pairs, precomputes the Mobius function using a linear sieve and
    harmonic numbers via cumulative sums. Contributions are calculated by iterating over possible d values
    (from Mobius inversion) and for each, summing over m to accumulate the weighted sums derived from the
    reformulated expression of S(N) using piecewise harmonic sums for efficiency.

    Complexity
    ----------
    O(N log N) time complexity, dominated by the nested loops over d and m, where the total iterations are
    proportional to sum_{d=1}^N N/d ≈ N log N. Space is O(N) for precomputed arrays.

    References
    https://projecteuler.net/problem=441
    """
    N = 10000000
    num_chunks = (os.cpu_count() or 8) * 5
    bounds = [1]
    last = 1
    for i in range(1, num_chunks):
        val = round(math.exp(math.log(N + 1) * (i / num_chunks)))
        if val > last:
            bounds.append(val)
            last = val

    bounds.append(N + 1)
    chunks = [(bounds[i], bounds[i + 1] - 1) for i in range(len(bounds) - 1)]
    with ProcessPoolExecutor(initializer=init_worker) as executor:
        partial_sums = list(tqdm(executor.map(chunk_func, chunks), total=len(chunks)))

    S = sum(partial_sums)
    print("%.4f" % S)

if __name__ == "__main__":
    main()