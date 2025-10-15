# Problem: https://projecteuler.net/problem=421
from math import gcd
from sympy.ntheory import primerange, primitive_root
from tqdm import tqdm

def main():
    """
    Purpose
    -------
    Solves Project Euler problem 421 by computing the sum over n=1 to 10^11 of s(n, 10^8), where s(n,m) is the sum
    of distinct prime factors <=m of n^15 +1.
    No parameters.
    Prints the result.
    
    Method / Math Rationale
    -----------------------
    The sum is reformulated as sum_{p prime <=10^8} p * (number of n<=10^11 with p | n^15 +1).
    For each such p, the count is computed using the number of residues mod p satisfying the condition, which is
    d = gcd(15, p-1) for odd p, and exactly calculated with floor and remainder adjustment by counting satisfying
    residues <= N % p.
    The satisfying residues are obtained by negating the elements of the subgroup of order d in the multiplicative
    group mod p.
    
    Complexity
    ----------
    O(pi(M) * D * log M), where M=10^8, pi(M)~5*10^6, D=15, log M ~20 for pow, so about 5e6 * 300 ~ 1.5e9
    operations, but in practice less, runnable in Python.
    
    References
    ----------
    https://projecteuler.net/problem=421
    """
    N = 10**11
    M = 10**8
    total = 0
    # Handle p=2 separately
    p = 2
    rem = N % p
    q = N // p
    c = 1 if 1 <= rem else 0
    count = q * 1 + c
    total += p * count
    # Generate odd primes <= M
    primes = list(primerange(3, M + 1))
    for p in tqdm(primes):
        m = p - 1
        d = gcd(15, m)
        g = primitive_root(p)
        h = pow(g, m // d, p)
        roots_1 = []
        current = 1
        for _ in range(d):
            roots_1.append(current)
            current = (current * h) % p

        roots = [p - r for r in roots_1]
        rem = N % p
        c = sum(1 for r in roots if r <= rem)
        q = N // p
        count = q * d + c
        total += p * count
    print(total)

if __name__ == "__main__":
    main()