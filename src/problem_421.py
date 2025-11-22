# Problem: https://projecteuler.net/problem=421
from math import gcd
from sympy.ntheory import primerange, primitive_root
from tqdm import tqdm

def main():
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