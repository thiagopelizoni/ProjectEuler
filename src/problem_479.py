# Problem: https://projecteuler.net/problem=479
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm

def compute_sum_chunk(start, end, n, MOD):
    s = 0
    for k in range(start, end + 1):
        r = 1 - k * k
        r_mod = r % MOD
        rn = pow(r_mod, n, MOD)
        one_minus_rn = (1 - rn) % MOD
        num = (r_mod * one_minus_rn) % MOD
        den = (k * k) % MOD
        den_inv = pow(den, MOD - 2, MOD) if den != 0 else 0
        contrib = (num * den_inv) % MOD
        s = (s + contrib) % MOD
    return s

def main():
    MOD = 1000000007
    n = 1000000
    num_workers = os.cpu_count() or 1
    chunk_size = (n // num_workers) + 1
    chunks = []
    for i in range(num_workers):
        start = i * chunk_size + 1
        end = min((i + 1) * chunk_size, n)
        if start > end:
            break
        chunks.append((start, end))

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(compute_sum_chunk, start, end, n, MOD) for start, end in chunks]
        total = 0
        for future in tqdm(as_completed(futures), total=len(futures)):
            partial = future.result()
            total = (total + partial) % MOD

    print(total)

if __name__ == "__main__":
    main()