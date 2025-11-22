# Problem: https://projecteuler.net/problem=437
import numpy as np
from concurrent.futures import ProcessPoolExecutor
from sympy.ntheory import factorint
from sympy.ntheory.residue_ntheory import sqrt_mod
from tqdm import tqdm

def get_primes(n):
    sieve = np.ones(n, dtype=bool)
    sieve[:2] = False
    for i in range(2, int(np.sqrt(n)) + 1):
        if sieve[i]:
            sieve[i * i :: i] = False
    return [int(p) for p in np.where(sieve)[0]]

def check(p):
    s = sqrt_mod(5, p)
    inv2 = pow(2, p - 2, p)
    g1 = ((1 + s) * inv2) % p
    g2 = ((1 + (p - s)) * inv2) % p
    n = p - 1
    factors = factorint(n)
    qs = list(factors.keys())
    for g in [g1, g2]:
        if g == 0:
            continue
        is_prim = True
        for q in qs:
            if pow(g, n // q, p) == 1:
                is_prim = False
                break
        if is_prim:
            return True
    return False

def main():
    N = 100000000
    primes = get_primes(N)
    candidates = [p for p in primes if p == 5 or p % 5 in (1, 4)]
    with ProcessPoolExecutor() as executor:
        results = list(tqdm(executor.map(check, candidates), total=len(candidates)))
    total_sum = sum(p for p, res in zip(candidates, results) if res)
    print(total_sum)

if __name__ == "__main__":
    main()