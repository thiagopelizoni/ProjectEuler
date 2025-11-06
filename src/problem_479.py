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
    """
    Purpose
    -------
    Computes S(10^6) modulo 1,000,000,007 for Project Euler problem 479, where S(n) is the sum over p=1 to n
    and k=1 to n of (a_k + b_k)^p (b_k + c_k)^p (c_k + a_k)^p, with a_k, b_k, c_k being the roots of the given
    equation.

    Method / Math Rationale
    ----------------------
    The expression (a_k + b_k)^p (b_k + c_k)^p (c_k + a_k)^p simplifies to (1 - k^2)^p for each k and p.
    For each fixed k, the sum over p=1 to n of r^p, where r = 1 - k^2, is a geometric series computed as
    r * (1 - r^n) / (1 - r), with 1 - r = k^2.
    Computations are performed modulo MOD using modular exponentiation and inverses.
    The sum over k is parallelized across multiple processes for performance.

    Complexity
    ----------
    O(n log n) time due to n modular exponentiations each O(log n), parallelized over available CPU cores.
    O(1) space per process.

    References
    ----------
    https://projecteuler.net/problem=479
    """
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