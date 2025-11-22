# Problem: https://projecteuler.net/problem=454
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed
from numba import jit
import math

@jit(nopython=True)
def sum_floors(n: int, a: int, b: int) -> int:
    res = 0
    while a <= b:
        val = n // a
        r = n // val if val != 0 else b
        r = min(b, r)
        res += val * (r - a + 1)
        a = r + 1
    return res

def compute_mu(max_m: int):
    mu = [0] * (max_m + 1)
    mu[1] = 1
    is_prime = [True] * (max_m + 1)
    primes = []
    for i in range(2, max_m + 1):
        if is_prime[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if i * p > max_m:
                break
            is_prime[i * p] = False
            if i % p == 0:
                mu[i * p] = 0
                break
            else:
                mu[i * p] = -mu[i]
    return mu

def compute_divisors(max_m: int):
    divs = [[] for _ in range(max_m + 1)]
    for i in range(1, max_m + 1):
        for j in range(i, max_m + 1, i):
            divs[j].append(i)
    return divs

L = 10**12
max_m = int((2 * L)**0.5) + 10
mu = compute_mu(max_m)
divs = compute_divisors(max_m)

def compute_for_m(m: int) -> int:
    low = m // 2 + 1
    high = m - 1
    s = 0
    for d in divs[m]:
        mud = mu[d]
        if mud == 0:
            continue
        A = (low + d - 1) // d
        B = high // d
        if A > B:
            continue
        p = m * d
        N = L // p
        temp = sum_floors(N, A, B)
        s += mud * temp
    return s

def compute_chunk(start: int, end: int) -> int:
    res = 0
    for m in range(start, end + 1):
        res += compute_for_m(m)
    return res

def main():
    result = 0
    futures = []
    with ProcessPoolExecutor() as executor:
        num_workers = executor._max_workers
        chunk_size = (max_m - 2) // (num_workers * 4) + 1
        m_start = 3
        while m_start <= max_m:
            m_end = min(m_start + chunk_size - 1, max_m)
            futures.append(executor.submit(compute_chunk, m_start, m_end))
            m_start = m_end + 1
        for future in tqdm(as_completed(futures), total=len(futures)):
            result += future.result()
    print(result)

if __name__ == "__main__":
    main()