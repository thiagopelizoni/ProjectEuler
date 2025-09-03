# Problem: https://projecteuler.net/problem=263
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from sympy.ntheory import isprime, factorint
from tqdm import tqdm

def is_practical(m):
    if m <= 1:
        return m == 1
    factors = factorint(m)
    primes = sorted(factors)
    s = 1
    for p in primes:
        if p > s + 1:
            return False
        a = factors[p]
        s *= (p ** (a + 1) - 1) // (p - 1)
    return True

def find_quadruplets_in_range(low, high):
    res = []
    p = low if low % 2 == 1 else low + 1
    if p < 5:
        p = 5
    for current_p in range(p, high, 2):
        if (isprime(current_p) and
            isprime(current_p + 6) and
            isprime(current_p + 12) and
            isprime(current_p + 18) and
            not isprime(current_p + 2) and
            not isprime(current_p + 4) and
            not isprime(current_p + 8) and
            not isprime(current_p + 10) and
            not isprime(current_p + 14) and
            not isprime(current_p + 16)):
            res.append(current_p)
    return res

paradises = []
current_upper = 100000
chunk_size = 1000000
start_low = 2
pbar = tqdm(desc="Processing ranges", unit="chunk")

while len(paradises) < 4:
    range_starts = list(range(start_low, current_upper, chunk_size))
    ranges = [(s, min(s + chunk_size, current_upper)) for s in range_starts]
    with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        futures = [executor.submit(find_quadruplets_in_range, low, high) for low, high in ranges]
        new_p = []
        for future in as_completed(futures):
            new_p.extend(future.result())
            pbar.update(1)
    new_p.sort()
    for p in new_p:
        n = p + 9
        to_check = [n - 8, n - 4, n, n + 4, n + 8]
        if all(is_practical(m) for m in to_check):
            paradises.append(n)
            if len(paradises) == 4:
                break
    start_low = current_upper
    current_upper *= 2

pbar.close()
print(sum(paradises))