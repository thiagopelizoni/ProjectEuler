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
    """
    Purpose
    -------
    Computes the sum of all primes less than 100,000,000 that have at least one Fibonacci primitive root.
    
    Method / Math Rationale
    -----------------------
    A Fibonacci primitive root for a prime p is a primitive root g modulo p satisfying g^2 ≡ g + 1 (mod p),
    i.e., g is a root of x^2 - x - 1 ≡ 0 (mod p). Such roots exist for p = 5 or when p ≡ 1 or 4 (mod 5),
    as these make 5 a quadratic residue modulo p. For each such prime p, compute the roots using the modular
    square root of 5, then check if either root is a primitive root by verifying that g^{(p-1)/q} ≠ 1 (mod p)
    for all prime factors q of p-1.
    
    Complexity
    ----------
    Time: O(N log log N) for sieving primes + O(π(N) * time for factoring p-1 and modular operations per prime).
    Space: O(N) for the sieve.

    References
    ----------
    https://projecteuler.net/problem=437
    """
    N = 100000000
    primes = get_primes(N)
    candidates = [p for p in primes if p == 5 or p % 5 in (1, 4)]
    with ProcessPoolExecutor() as executor:
        results = list(tqdm(executor.map(check, candidates), total=len(candidates)))
    total_sum = sum(p for p, res in zip(candidates, results) if res)
    print(total_sum)

if __name__ == "__main__":
    main()