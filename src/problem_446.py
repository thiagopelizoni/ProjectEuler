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