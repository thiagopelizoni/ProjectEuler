# Problem: https://projecteuler.net/problem=350
import numba
import numpy as np
from math import gcd
from tqdm import tqdm

def compute_divisors(max_val):
    divisors = [[] for _ in range(max_val + 1)]
    for i in range(1, max_val + 1):
        for j in range(i, max_val + 1, i):
            divisors[j].append(i)
    return divisors

def compute_mu(max_val):
    mu = [0] * (max_val + 1)
    visited = [False] * (max_val + 1)
    primes = []
    mu[1] = 1
    for i in range(2, max_val + 1):
        if not visited[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if p * i > max_val:
                break
            visited[p * i] = True
            if i % p == 0:
                mu[p * i] = 0
                break
            else:
                mu[p * i] = -mu[i]
    return mu

@numba.jit(nopython=True)
def compute_sum_for_s(s, G, L, h_np, mod):
    result = 0
    high = L // s
    if high < G:
        return 0
    i = G
    while i <= high:
        q = L // (i * s)
        j = L // (q * s)
        if j > high:
            j = high
        count = j - i + 1
        result = (result + count * h_np[q]) % mod
        i = j + 1
    return result

def main():
    """
    Purpose
    -------
    Solves Project Euler problem 350 by computing the number of lists of size 10^18 with GCD >= 10^6
    and LCM <= 10^12, modulo 101^4.

    Method / Math Rationale
    -----------------------
    For a sequence of length N=10^18, count sequences with GCD >= G=10^6 and LCM <= L=10^12.
    Using Mobius inversion, transform to count sequences with GCD=1 and LCM <= k for k up to L/G.
    Compute h(k) as the number of sequences with GCD=1 and LCM=k using the divisor function and
    Mobius function. Sum contributions over square-free s using segmented sums for efficiency,
    optimized with Numba for fast arithmetic.

    Complexity
    ----------
    O(M log M + sum square-free s sqrt(L / s)) ~ O(10^6 log 10^6 + 10^6 * 10^3) = O(10^9)
    operations, with Numba optimization for numerical loops.

    References
    ----------
    https://projecteuler.net/problem=350
    """
    N = 10**18
    G = 10**6
    L = 10**12
    max_k = L // G
    mod = 101**4
    divisors = compute_divisors(max_k)
    mu = compute_mu(max_k)
    h = [0] * (max_k + 1)
    for k in range(1, max_k + 1):
        count = 0
        for d in divisors[k]:
            if mu[d] == 0:
                continue
            count = (count + mu[d] * pow(len(divisors[d]), N, mod)) % mod
        h[k] = count
    h_np = np.array(h, dtype=np.int64)
    result = 0
    for s in tqdm(range(1, max_k + 1), desc="Processing square-free s"):
        if mu[s] == 0:
            continue
        sum_s = compute_sum_for_s(s, G, L, h_np, mod)
        result = (result + mu[s] * sum_s) % mod
    print(result)

if __name__ == "__main__":
    main()