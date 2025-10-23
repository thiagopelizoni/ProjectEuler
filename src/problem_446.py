# Problem: https://projecteuler.net/problem=446
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm
from sympy.ntheory import factorint

def compute_sum(start, end, MOD):
    total = 0
    for k in range(start, end + 1):
        a = (k - 1) ** 2 + 1
        b = (k + 1) ** 2 + 1
        factors_a = factorint(a)
        factors_b = factorint(b)
        factors = {}
        all_primes = set(factors_a) | set(factors_b)
        for p in all_primes:
            factors[p] = factors_a.get(p, 0) + factors_b.get(p, 0)
        prod_mod = 1
        for p, exp in factors.items():
            pk_mod = pow(p, exp, MOD)
            one_plus = (1 + pk_mod) % MOD
            prod_mod = (prod_mod * one_plus) % MOD
        n_mod = (a % MOD * (b % MOD)) % MOD
        res = (prod_mod - n_mod + MOD) % MOD
        total = (total + res) % MOD
    return total

def main():
    """
    Purpose
    -------
    Computes the sum F(10^7) as defined in Project Euler problem 446, which is the sum of R(n) for n = k^4 + 4
    from k=1 to 10^7, modulo 1000000007, and prints the result.

    Method / Math Rationale
    -----------------------
    For each k, n = k^4 + 4 = ((k-1)^2 + 1) * ((k+1)^2 + 1). R(n) counts the retractions, derived as
    prod_{p^e || n} (1 + p^e) - n.
    Factorize the two quadratic terms using sympy.factorint, merge the factorizations, compute the product
    (1 + p^e) for each prime power modulo MOD, then subtract n modulo MOD, adjusting for modulo.
    Parallelizes the summation over k using ProcessPoolExecutor for efficiency.

    Complexity
    ----------
    Time: O(N * T), where N=10^7, T is average time for factorint on ~14-digit numbers; parallelism reduces wall time.
    Space: O(1) per process, minimal.

    References
    ----------
    https://projecteuler.net/problem=446
    """
    MOD = 1000000007
    N = 10**7
    num_processes = os.cpu_count() or 1
    num_chunks = num_processes * 10
    chunk_size = max(1, N // num_chunks)
    num_chunks = (N + chunk_size - 1) // chunk_size
    futures = []
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        for i in range(num_chunks):
            start = 1 + i * chunk_size
            end = min(N, start + chunk_size - 1)
            futures.append(executor.submit(compute_sum, start, end, MOD))
    total = 0
    with tqdm(total=num_chunks) as pbar:
        for future in as_completed(futures):
            total = (total + future.result()) % MOD
            pbar.update(1)
    print(total)

if __name__ == "__main__":
    main()